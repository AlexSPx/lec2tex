#!/usr/bin/env python3
"""OCR the handwritten lecture notes in pesho-stat-1.pdf.

The source is 37 phone photos of a spiral notebook: Bulgarian cursive on
tinted ruled paper, shot at an angle, ~1536x2048 each. Ordinary OCR engines
are useless on this — it needs a vision-language model. What this script adds
around the model is the preprocessing that makes the difference:

  * crop away the desk, the facing page and the spiral binding
  * flatten the tint and the ruling lines, which otherwise compete with the
    ink for the model's attention
  * raise contrast so faint pen strokes survive downscaling to the model's
    input resolution

Usage:
    python3 scripts/ocr_pesho.py --prep-only            # write prepped PNGs
    python3 scripts/ocr_pesho.py --pages 1-4            # OCR a sample
    python3 scripts/ocr_pesho.py                        # OCR all 37 pages

Pages that already have output are skipped, so re-running resumes; --force
re-reads them. The agy CLI drops a connection now and then on a run this long,
hence the retry with backoff.

Backends (reuses src/backends.py, same flags as the video pipeline):
    --mode cloud --provider agy          (default; local CLI, no API key)
    --mode cloud --provider gemini       (needs GEMINI_API_KEY)
    --mode local --model mlx-community/Qwen2.5-VL-7B-Instruct-4bit
"""
import argparse
import json
import os
import sys
import time

import cv2
import numpy as np
import pymupdf

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))

SRC_PDF = os.path.join(ROOT, "pesho-stat-1.pdf")
OUT = os.path.join(ROOT, "run", "pesho")

PROMPT = """Транскрибирай тази снимка на ръкописни лекционни записки по теория на вероятностите и статистика. Текстът е на български, писан на ръка с курсив.

Върни САМО JSON обект със следната форма, без коментар и без markdown:
{
  "items": [
    {"type": "text", "content": "<българският текст както е написан>"},
    {"type": "equation", "content": "<математиката като валиден LaTeX, без $ разделители>"}
  ]
}

Правила:
- "equation" за всичко математическо (формули, изрази, отделни означения като \\Omega, A^c, \\bigcup_{i=1}^n A_i).
- "text" за проза и заглавия; запази българския, не превеждай.
- Спазвай реда отгоре-надолу.
- Ако нещо е нечетливо, постави [?] на негово място. НЕ измисляй съдържание.
Върни само JSON обекта."""


def prep(img):
    """Crop to the written page, kill the ruling/tint, boost the ink."""
    g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # --- locate the page: the paper is much brighter than the desk ---------
    blur = cv2.GaussianBlur(g, (9, 9), 0)
    _, m = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((25, 25), np.uint8))
    cnts, _ = cv2.findContours(m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if cnts:
        x, y, w, h = cv2.boundingRect(max(cnts, key=cv2.contourArea))
        # trim a little so the binding rings and the page edge fall away
        pad = int(0.012 * max(w, h))
        x, y = x + pad, y + pad
        w, h = max(w - 2 * pad, 1), max(h - 2 * pad, 1)
        img, g = img[y:y + h, x:x + w], g[y:y + h, x:x + w]

    # --- flatten the paper: divide out a heavy blur of itself --------------
    # Ruled lines and the yellow cast are low-frequency next to pen strokes,
    # so dividing by a large-kernel blur removes both and leaves the ink.
    bg = cv2.GaussianBlur(g, (0, 0), sigmaX=25, sigmaY=25)
    flat = cv2.divide(g, bg, scale=255)

    # --- stretch what is left ---------------------------------------------
    flat = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8)).apply(flat)
    lo, hi = np.percentile(flat, [2, 98])
    flat = np.clip((flat.astype(np.float32) - lo) * 255.0 / max(hi - lo, 1), 0, 255)
    return flat.astype(np.uint8)


def render(page_no, dpi=220):
    d = pymupdf.open(SRC_PDF)
    pm = d[page_no].get_pixmap(dpi=dpi)
    a = np.frombuffer(pm.samples, dtype=np.uint8).reshape(pm.height, pm.width, pm.n)
    return cv2.cvtColor(a[:, :, :3], cv2.COLOR_RGB2BGR)


def parse_pages(spec, total):
    if not spec:
        return list(range(total))
    out = []
    for part in spec.split(","):
        if "-" in part:
            a, b = part.split("-")
            out += list(range(int(a) - 1, int(b)))
        else:
            out.append(int(part) - 1)
    return [p for p in out if 0 <= p < total]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pages", default=None, help="e.g. 1-4 or 1,7,12")
    ap.add_argument("--prep-only", action="store_true")
    ap.add_argument("--dpi", type=int, default=220)
    ap.add_argument("--mode", default="cloud")
    ap.add_argument("--model", default=None)
    ap.add_argument("--provider", default="agy",
                    help="agy uses the local Antigravity CLI and needs no API key")
    ap.add_argument("--base-url", default=None)
    ap.add_argument("--retries", type=int, default=4)
    ap.add_argument("--force", action="store_true",
                    help="re-OCR pages that already have output")
    args = ap.parse_args()

    total = pymupdf.open(SRC_PDF).page_count
    pages = parse_pages(args.pages, total)
    os.makedirs(os.path.join(OUT, "prep"), exist_ok=True)
    os.makedirs(os.path.join(OUT, "ocr"), exist_ok=True)

    prepped = []
    for p in pages:
        img = prep(render(p, args.dpi))
        path = os.path.join(OUT, "prep", "page_%03d.png" % (p + 1))
        cv2.imwrite(path, img)
        prepped.append((p, path))
        print("prepped", path, img.shape)
    if args.prep_only:
        return

    from backends import VLMClient
    from vlm_ocr import _extract_json
    client = VLMClient(mode=args.mode, model=args.model,
                       provider=args.provider, base_url=args.base_url)
    failed = []
    for p, path in prepped:
        dest = os.path.join(OUT, "ocr", "page_%03d.json" % (p + 1))
        # Resume: a 37-page run is long enough that a transient network error
        # partway through should not cost the pages already read.
        if os.path.exists(dest) and not args.force:
            print("skip page %d (already done)" % (p + 1))
            continue
        data = None
        for attempt in range(1, args.retries + 1):
            try:
                raw = client.read_image(path, PROMPT)
                try:
                    data = _extract_json(raw)
                except Exception:
                    data = {"items": [], "raw": raw}
                break
            except Exception as e:
                wait = min(60, 5 * 2 ** (attempt - 1))
                print("page %d attempt %d/%d failed (%s)"
                      % (p + 1, attempt, args.retries, str(e)[:90]))
                if attempt < args.retries:
                    print("   retrying in %ds" % wait)
                    time.sleep(wait)
        if data is None:
            failed.append(p + 1)
            continue
        data["page"] = p + 1
        json.dump(data, open(dest, "w"), ensure_ascii=False, indent=1)
        print("ocr page %d -> %d items" % (p + 1, len(data.get("items", []))))
    if failed:
        print("FAILED pages (re-run to retry): %s"
              % ",".join(str(f) for f in failed))


if __name__ == "__main__":
    main()
