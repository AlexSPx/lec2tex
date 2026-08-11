# Lec2LaTeX Pipeline

Converts lecture videos (Bulgarian audio + handwritten whiteboard) into clean,
compilable **Bulgarian** LaTeX notes. Instead of a frame-by-frame transcript it
aligns spoken content with whiteboard states, reads the board with a
vision-language model, verifies the math, and runs a self-correcting LaTeX
compile loop.

The pipeline is **local-first** and **dual-backend**: every model-using stage can
run on-device or in the cloud, on either an Apple-Silicon (Metal) machine or a
CUDA/Linux box, and each stage is switched independently.

## Architecture

```
Video
 ├─ Stage 1  Transcribe (device-aware ASR)              → audio/transcript.json
 ├─ Stage 2  Board detection (rectify optional)         → board_corners.json
 ├─ Stage 3  Board keyframes (dual-SSIM)                → board/*.png, board_states.json
 ├─ Stage 4  VLM whole-board OCR (→ text + LaTeX)       → ocr/*.json
 ├─ Stage 5  Temporal alignment (speech ↔ board state)  → ir/lecture_ir.json
 ├─ Stage 6  Math verification (SymPy + reasoning LLM)  → ir/lecture_ir.json (+report)
 └─ Stage 7  Generation + Tectonic self-correct loop    → latex/lecture.{tex,pdf}
```

Stage 4 replaces the former PaddleOCR + pix2tex + IoU-evolution stage (which was
unreliable on handwriting): one VLM call reads the whole board into structured
`{text|equation}` items. Stage 6 is new. Compilation uses **Tectonic** (a single
cross-platform binary) with a Docker/`pdflatex` fallback.

## Setup

### Common
- Python 3.11, FFmpeg, `yt-dlp` (optional, for pulling lecture videos)
- `tectonic` for compilation: `brew install tectonic` (macOS) / see tectonic docs (Linux)

```bash
python3.11 -m venv --system-site-packages .venv
.venv/bin/pip install --upgrade pip
```

### Metal profile (Apple Silicon)
```bash
.venv/bin/pip install opencv-python-headless scikit-image sympy antlr4-python3-runtime \
                      mlx-whisper mlx-vlm
# local text LLM (verify/gen) via either:
#   * mlx_lm.server  (serves an MLX model at http://localhost:8080/v1), or
#   * Ollama         (http://localhost:11434/v1)
```
Local model store defaults to `/Users/g8row/models` (override with
`LEC2TEX_MODELS_DIR`). A `--*-model` that names a directory there is used directly.

### CUDA profile (Linux)
```bash
.venv/bin/pip install faster-whisper opencv-python-headless scikit-image sympy \
                      antlr4-python3-runtime
# ASR: faster-whisper (cuda) or NVIDIA NeMo Canary-1b-v2 (--asr-backend nemo-canary)
# LLM/VLM local: vLLM or llama.cpp exposing an OpenAI-compatible endpoint
```

## Running

```bash
# Fully local on Metal (ASR local; OCR/verify/gen point at local servers):
.venv/bin/python src/main.py --video lecture.mp4 --device metal --mode local

# Local-first with cloud OCR (no local VLM installed):
.venv/bin/python src/main.py --video lecture.mp4 --device metal \
    --mode local --ocr-mode cloud --ocr-provider agy

# Everything in the cloud via Antigravity:
.venv/bin/python src/main.py --video lecture.mp4 --mode cloud --provider agy
```

### Per-step backend switching
Each model stage has its own `--<step>-mode {local,cloud}`, `--<step>-model`,
`--<step>-base-url`, and `--<step>-provider`, where `<step>` ∈ `asr | ocr | verify | gen`.
`--mode` sets the default for all steps; `--device {auto,metal,cuda,cpu}` picks the
local runtime. Example — local ASR + cloud OCR + local verify/gen against a
local MLX server:

```bash
.venv/bin/python src/main.py --video lecture.mp4 --device metal --mode local \
    --ocr-mode cloud --ocr-provider agy \
    --verify-base-url http://localhost:11434/v1 --verify-model qwen3:4b \
    --gen-base-url http://localhost:8080/v1
```

### Recommended local runtime per role (2026)
| Stage | Metal (M1) | CUDA (Linux) |
|---|---|---|
| ASR | `mlx-whisper` large-v3 | `faster-whisper` / NeMo Canary-1b-v2 |
| Board VLM | MLX-VLM (`qwen*-vl`) | vLLM |
| Verify / Gen | `mlx_lm.server` or Ollama | vLLM / llama.cpp |
| Compile | Tectonic | Tectonic |

### Key flags
- `--no-rectify` — skip perspective correction; feed the full frame to the VLM (VLMs tolerate skew).
- `--asr-backend {auto,mlx-whisper,faster-whisper,nemo-canary}`
- `--skip-{transcription,detection,tracking,ocr,alignment,verification,generation}`
- `--ssim-threshold` / `--stability-threshold` — keyframe sensitivity.
- `--align-window` — speech↔board alignment window (s).
- `--compiler {pdflatex,lualatex}` — used by the Docker/local fallback (Tectonic ignores it).
- `--main-font` — Cyrillic-capable Unicode font for the preamble. Tectonic uses XeTeX, so notes compile via `fontspec` (`\setmainfont`), **not** `T2A/inputenc/babel` (Tectonic doesn't bundle the cm-super metrics that route needs). Default: `Times New Roman` on macOS, `DejaVu Serif` on Linux. Pass another installed font if you prefer.

## Notes on RAM (Apple Silicon)
On a 32GB machine, avoid loading a >16GB model concurrently with other stages.
Run stages sequentially (the orchestrator does), and prefer a small local
reasoner (e.g. `qwen3:4b` via Ollama) for verification, or a cloud provider for
OCR/generation, when memory is tight.
