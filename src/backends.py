"""
backends.py — unified, device-aware model backends for lec2tex.

Every model-using stage (ASR, board OCR/VLM, math verification, note generation)
goes through this module so that each stage can independently switch between a
*local* on-device backend and a *cloud* backend, on either an Apple-Silicon
(Metal) machine or a CUDA/Linux box.

Design:
  * `detect_device()`               -> "metal" | "cuda" | "cpu"
  * `resolve_model_path(name)`      -> prefer a model already on disk under
                                       /Users/g8row/models before treating the
                                       name as a hub id / Ollama tag.
  * `LLMClient`                     -> text chat. `local` talks to any
                                       OpenAI-compatible server (mlx_lm.server,
                                       llama-server, Ollama /v1, vLLM); `cloud`
                                       routes to agy (Antigravity) / Gemini /
                                       OpenAI.
  * `VLMClient`                     -> vision. `local` uses MLX-VLM directly (or
                                       an OpenAI-compatible server with image
                                       content parts); `cloud` uses agy / Gemini.

Nothing here is pipeline-stage-specific; the JSON schemas the stages exchange are
identical regardless of which backend produced them.
"""

import os
import sys
import json
import base64
import shutil
import tempfile
import subprocess

import requests

LOCAL_MODELS_DIR = os.environ.get("LEC2TEX_MODELS_DIR", "/Users/g8row/models")

# Default OpenAI-compatible endpoints for a *local* server, per device.
DEFAULT_LOCAL_BASE_URL = {
    "metal": os.environ.get("LEC2TEX_METAL_BASE_URL", "http://localhost:8080/v1"),
    "cuda": os.environ.get("LEC2TEX_CUDA_BASE_URL", "http://localhost:8000/v1"),
    "cpu": "http://localhost:8080/v1",
}


def detect_device():
    """Best-effort detection of the local acceleration backend."""
    forced = os.environ.get("LEC2TEX_DEVICE")
    if forced in ("metal", "cuda", "cpu"):
        return forced
    # CUDA?
    try:
        import torch  # noqa
        if torch.cuda.is_available():
            return "cuda"
    except Exception:
        pass
    # Apple Silicon / Metal?
    if sys.platform == "darwin":
        try:
            import platform
            if platform.machine() == "arm64":
                return "metal"
        except Exception:
            pass
    return "cpu"


def resolve_device(device):
    """Resolve a --device value ('auto'|'metal'|'cuda'|'cpu') to a concrete one."""
    if device in (None, "auto"):
        return detect_device()
    return device


def resolve_model_path(name):
    """
    If `name` matches a directory or file under LOCAL_MODELS_DIR, return the
    absolute path; otherwise return `name` unchanged (hub id / Ollama tag).
    """
    if not name:
        return name
    if os.path.isabs(name) and os.path.exists(name):
        return name
    candidate = os.path.join(LOCAL_MODELS_DIR, name)
    if os.path.exists(candidate):
        return candidate
    return name


# --------------------------------------------------------------------------- #
# Cloud helpers (shared by LLMClient and VLMClient)
# --------------------------------------------------------------------------- #

def _call_agy(prompt, timeout=600):
    """Call the Antigravity CLI in one-shot print mode. `prompt` may instruct it
    to read files (including images) by path."""
    cmd = ["agy", "--print", prompt, "--dangerously-skip-permissions"]
    res = subprocess.run(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        text=True, encoding="utf-8", timeout=timeout,
    )
    if res.returncode != 0:
        raise RuntimeError(f"agy CLI failed (exit {res.returncode}): {res.stderr}")
    return res.stdout


def _call_gemini(prompt, api_key, model, image_path=None, timeout=300):
    model = model or "gemini-2.5-flash"
    url = (
        f"https://generativelanguage.googleapis.com/v1beta/models/"
        f"{model}:generateContent?key={api_key}"
    )
    parts = [{"text": prompt}]
    if image_path:
        with open(image_path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode("ascii")
        mime = "image/png" if image_path.lower().endswith(".png") else "image/jpeg"
        parts.insert(0, {"inline_data": {"mime_type": mime, "data": b64}})
    payload = {"contents": [{"parts": parts}], "generationConfig": {"temperature": 0.1}}
    r = requests.post(url, json=payload, timeout=timeout)
    r.raise_for_status()
    data = r.json()
    return data["candidates"][0]["content"]["parts"][0]["text"]


def _call_openai_chat(base_url, api_key, model, messages, timeout=600,
                      temperature=0.1, max_tokens=8192):
    """One code path for every OpenAI-compatible chat endpoint (local or cloud).

    Note: some local servers (e.g. mlx_lm.server) expose chat at /chat/completions
    without a /v1 prefix and require `model` to be the exact loaded path — pass the
    base_url and model accordingly. A short default max_tokens truncates reasoning
    models mid-thought, so we request a generous budget."""
    url = base_url.rstrip("/") + "/chat/completions"
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    payload = {"model": model, "messages": messages, "temperature": temperature,
               "max_tokens": max_tokens}
    r = requests.post(url, headers=headers, json=payload, timeout=timeout)
    r.raise_for_status()
    data = r.json()
    return data["choices"][0]["message"]["content"]


def _data_url(image_path):
    with open(image_path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("ascii")
    mime = "image/png" if image_path.lower().endswith(".png") else "image/jpeg"
    return f"data:{mime};base64,{b64}"


# --------------------------------------------------------------------------- #
# Text LLM client
# --------------------------------------------------------------------------- #

class LLMClient:
    """
    Text chat client.

    mode == "local":  OpenAI-compatible server at base_url (mlx_lm.server,
                      llama-server, Ollama /v1, vLLM ...). `model` is the tag/path.
    mode == "cloud":  provider in {"agy", "gemini", "openai"}.
    """

    def __init__(self, mode="local", model=None, base_url=None, api_key=None,
                 provider="agy", device="auto"):
        self.mode = mode
        self.device = resolve_device(device)
        self.model = model
        self.base_url = base_url or DEFAULT_LOCAL_BASE_URL.get(self.device)
        self.provider = provider
        self.api_key = api_key or self._default_api_key(provider)

    @staticmethod
    def _default_api_key(provider):
        if provider == "gemini":
            return os.environ.get("GEMINI_API_KEY")
        if provider == "openai":
            return os.environ.get("OPENAI_API_KEY")
        return None

    def complete(self, prompt, system=None):
        if self.mode == "cloud":
            if self.provider == "agy":
                return _call_agy(prompt)
            if self.provider == "gemini":
                return _call_gemini(prompt, self.api_key, self.model)
            if self.provider == "openai":
                messages = []
                if system:
                    messages.append({"role": "system", "content": system})
                messages.append({"role": "user", "content": prompt})
                return _call_openai_chat(
                    "https://api.openai.com/v1", self.api_key,
                    self.model or "gpt-4o", messages,
                )
            raise ValueError(f"Unknown cloud provider: {self.provider}")

        # local: OpenAI-compatible server
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})
        # mlx_lm.server serves whichever model is loaded and ignores/echoes the
        # `model` field; send a non-empty placeholder when none was given.
        model = self.model or "local"
        return _call_openai_chat(self.base_url, self.api_key, model, messages)

    def describe(self):
        return f"LLM[{self.mode}/{self.provider if self.mode=='cloud' else self.base_url}:{self.model}]"


# --------------------------------------------------------------------------- #
# Vision-language client
# --------------------------------------------------------------------------- #

class VLMClient:
    """
    Vision client for reading a whiteboard image.

    mode == "local":
        backend == "mlx-vlm" (default on metal): run MLX-VLM in-process.
        backend == "openai":  OpenAI-compatible server with image content parts.
    mode == "cloud":
        provider in {"agy", "gemini"}.
    """

    def __init__(self, mode="local", model=None, base_url=None, api_key=None,
                 provider="agy", device="auto", backend=None):
        self.mode = mode
        self.device = resolve_device(device)
        self.model = model
        self.base_url = base_url or DEFAULT_LOCAL_BASE_URL.get(self.device)
        self.provider = provider
        self.api_key = api_key or LLMClient._default_api_key(provider)
        # default local backend: MLX-VLM on metal, else an OpenAI-compatible server
        self.backend = backend or ("mlx-vlm" if self.device == "metal" else "openai")
        self._mlx = None  # lazily-loaded (model, processor, config)

    # --- local MLX-VLM ----------------------------------------------------- #
    def _load_mlx(self):
        if self._mlx is not None:
            return self._mlx
        from mlx_vlm import load
        from mlx_vlm.utils import load_config
        model_id = resolve_model_path(self.model)
        model, processor = load(model_id)
        config = load_config(model_id)
        self._mlx = (model, processor, config)
        return self._mlx

    def _read_mlx(self, image_path, prompt, max_tokens=2048):
        from mlx_vlm import generate
        from mlx_vlm.prompt_utils import apply_chat_template
        model, processor, config = self._load_mlx()
        formatted = apply_chat_template(processor, config, prompt, num_images=1)
        out = generate(
            model, processor, formatted, [image_path],
            max_tokens=max_tokens, temperature=0.0, verbose=False,
        )
        # mlx_vlm.generate returns a str (older) or a GenerationResult (newer)
        return getattr(out, "text", out)

    # --- public ------------------------------------------------------------ #
    def read_image(self, image_path, prompt):
        if self.mode == "cloud":
            if self.provider == "agy":
                meta = (
                    f"Look at the image file at this absolute path: {os.path.abspath(image_path)}\n\n"
                    f"{prompt}\n\n"
                    "Do not write any files or run any commands; print ONLY the requested output to stdout."
                )
                return _call_agy(meta)
            if self.provider == "gemini":
                return _call_gemini(prompt, self.api_key, self.model, image_path=image_path)
            raise ValueError(f"Unknown cloud VLM provider: {self.provider}")

        # local
        if self.backend == "mlx-vlm":
            return self._read_mlx(image_path, prompt)
        # OpenAI-compatible vision server
        messages = [{
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {"url": _data_url(image_path)}},
            ],
        }]
        model = self.model or "local"
        return _call_openai_chat(self.base_url, self.api_key, model, messages)

    def describe(self):
        tgt = self.provider if self.mode == "cloud" else f"{self.backend}:{self.base_url}"
        return f"VLM[{self.mode}/{tgt}:{self.model}]"


# --------------------------------------------------------------------------- #
# CLI arg helpers (shared by stages + main.py)
# --------------------------------------------------------------------------- #

def add_backend_args(parser, step):
    """Add --<step>-mode / --<step>-model / --<step>-base-url to a stage parser."""
    parser.add_argument(f"--{step}-mode", choices=["local", "cloud"], default=None,
                        help=f"Where the {step} model runs (overrides --mode).")
    parser.add_argument(f"--{step}-model", default=None,
                        help=f"Model tag/path/hub-id for the {step} step.")
    parser.add_argument(f"--{step}-base-url", default=None,
                        help=f"OpenAI-compatible base URL for a local {step} server.")
    parser.add_argument(f"--{step}-provider", default=None,
                        help=f"Cloud provider for {step} (agy|gemini|openai).")
