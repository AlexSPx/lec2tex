"""
Stage 3: Whole-board OCR via a Vision-Language Model.

Replaces the old PaddleOCR + pix2tex + IoU-evolution pipeline. For each board
keyframe we make ONE VLM call that returns the whole board as structured
JSON — Bulgarian prose as `text`, math as LaTeX `equation` — in reading order.
The generation stage later merges duplicate/updated formulas across states, so
no explicit added/removed evolution tracking is needed here.

Output schema (unchanged for downstream `temporal_alignment.py`):
    { "timestamp": float, "image": str,
      "items": [ {"type": "text"|"equation", "content": str}, ... ] }
"""

import os
import sys
import json
import argparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from backends import VLMClient, add_backend_args

OCR_PROMPT = """You are transcribing a photo of a university lecture whiteboard/blackboard from a Bulgarian mathematics lecture.

Read EVERYTHING written on the board, in natural reading order (top-to-bottom, left-to-right).

Return ONLY a JSON object of this exact form, with no prose or markdown fences:
{
  "items": [
    {"type": "text", "content": "<Bulgarian words exactly as written>"},
    {"type": "equation", "content": "<the math as valid LaTeX, no $ delimiters>"}
  ]
}

Rules:
- Use "equation" for anything mathematical (formulas, expressions, single variables in a math context) and write it as valid LaTeX.
- Use "text" for prose/labels; keep the original Bulgarian, do not translate.
- Do NOT invent content that is not on the board. If the board is empty, return {"items": []}.
- Preserve the order in which items appear on the board.
Output the JSON object only."""


def _extract_json(raw):
    """Pull the first JSON object out of an LLM/VLM response."""
    raw = raw.strip()
    # strip ```json fences if present
    if "```" in raw:
        import re
        m = re.search(r"```(?:json)?\s*(.*?)```", raw, re.DOTALL)
        if m:
            raw = m.group(1).strip()
    start = raw.find("{")
    end = raw.rfind("}")
    if start != -1 and end != -1 and end > start:
        raw = raw[start:end + 1]
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        # VLMs often emit raw LaTeX (\frac, \Omega, ...) inside JSON strings, where
        # a lone backslash is illegal. Escape any backslash not starting a valid
        # JSON escape (\" \\ \/ \b \f \n \r \t \uXXXX), then retry.
        import re
        fixed = re.sub(r'\\(?!["\\/bfnrtu])', r'\\\\', raw)
        return json.loads(fixed)


def run_vlm_ocr(board_states_path, output_dir, client, board_dir=None):
    with open(board_states_path, "r", encoding="utf-8") as f:
        board_states = json.load(f)

    os.makedirs(output_dir, exist_ok=True)
    base_root = os.path.dirname(board_states_path)
    if board_dir is None:
        board_dir = os.path.join(base_root, "board")

    print(f"Board OCR backend: {client.describe()}")

    for idx, state in enumerate(board_states):
        image_name = state["image"]
        timestamp = state["timestamp"]
        base_name, _ = os.path.splitext(image_name)
        out_path = os.path.join(output_dir, f"{base_name}.json")

        # resume from cache
        if os.path.exists(out_path):
            print(f"[{idx+1}/{len(board_states)}] {image_name}: cached, skipping.")
            continue

        image_path = os.path.join(board_dir, image_name)
        if not os.path.exists(image_path):
            alt = os.path.join(base_root, image_name)
            image_path = alt if os.path.exists(alt) else image_path
        if not os.path.exists(image_path):
            print(f"[{idx+1}/{len(board_states)}] {image_name}: image missing, skipping.")
            continue

        print(f"[{idx+1}/{len(board_states)}] {image_name} @ {timestamp}s -> VLM ...")
        try:
            raw = client.read_image(image_path, OCR_PROMPT)
            parsed = _extract_json(raw)
            items = parsed.get("items", [])
            # normalise
            clean = []
            for it in items:
                t = it.get("type", "text")
                c = it.get("content", "")
                if not c:
                    continue
                clean.append({"type": "equation" if t == "equation" else "text",
                              "content": c})
        except Exception as e:
            print(f"  ! VLM/parse failed for {image_name}: {e}")
            clean = []

        with open(out_path, "w", encoding="utf-8") as f:
            json.dump({"timestamp": timestamp, "image": image_name, "items": clean},
                      f, ensure_ascii=False, indent=2)
        print(f"  -> {len(clean)} item(s) saved to {out_path}")


def main():
    p = argparse.ArgumentParser(description="Stage 3: VLM whole-board OCR")
    p.add_argument("--board-states", default="board_states.json")
    p.add_argument("--output-dir", default="ocr")
    p.add_argument("--board-dir", default=None, help="Dir with board_*.png (default: <states dir>/board)")
    p.add_argument("--device", default="auto", choices=["auto", "metal", "cuda", "cpu"])
    add_backend_args(p, "ocr")
    args = p.parse_args()

    client = VLMClient(
        mode=args.ocr_mode or "local",
        model=args.ocr_model,
        base_url=args.ocr_base_url,
        provider=args.ocr_provider or "agy",
        device=args.device,
    )
    run_vlm_ocr(args.board_states, args.output_dir, client, board_dir=args.board_dir)


if __name__ == "__main__":
    main()
