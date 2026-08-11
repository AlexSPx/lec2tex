#!/usr/bin/env bash
# Batch-process the remaining lectures (playlist items 2..15).
# 1x video, coarse keyframing (--interval 3.0), 1x mlx-whisper ASR (native
# timestamps), parallel cloud (agy) OCR, SymPy verify, cloud (agy) verbose gen.
# Fully resumable: every stage skips if its output already exists.
set -uo pipefail
cd /Users/g8row/Documents/lec2tex

PY=.venv/bin/python
POCR=/private/tmp/claude-501/-Users-g8row-Documents-lec2tex/bab9889a-7c7e-43d6-bfc2-a0133692cb55/scratchpad/parallel_ocr.py

# playlist_index:video_id  (item 1 already done)
LECTURES=(
  "02:RQSHAmIEfIw" "03:XM_pVeB1eRY" "04:cCsbGZM5wUw" "05:4r9wVpFZDo4"
  "06:KcDJVJTwZv8" "07:lnwCch8jkxA" "08:h-nB0-tuVok" "09:6mef5l5a8FA"
  "10:FX9JXSf8ohs" "11:nwAhkK625HE" "12:zeV2-9WcdWY" "13:X6Q62jwcrYQ"
  "14:UXMbftZ1cQA" "15:-apJjvlA07E"
)

for entry in "${LECTURES[@]}"; do
  NN="${entry%%:*}"; VID="${entry##*:}"
  OUT="run/lecture_${NN}"
  mkdir -p "$OUT/audio" "$OUT/ir"
  echo "================ LECTURE $NN ($VID) $(date '+%H:%M:%S') ================"

  if [ -f "$OUT/latex/lecture.pdf" ]; then echo "[$NN] already complete, skipping."; continue; fi

  # 1) download (1x) — retry with backoff to survive YouTube 403 rate-limiting
  if [ ! -f "$OUT/video.mp4" ]; then
    dl_ok=0
    for attempt in 1 2 3 4 5; do
      echo "[$NN] downloading (attempt $attempt)..."
      yt-dlp --no-warnings --retries 10 --fragment-retries 10 --sleep-requests 1.5 \
        -f "bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/best[height<=720]" \
        -o "$OUT/video.%(ext)s" "https://www.youtube.com/watch?v=$VID" >> "$OUT/pipeline.log" 2>&1 \
        && { dl_ok=1; break; }
      backoff=$((attempt*attempt*30))   # 30s,120s,270s,480s,750s
      echo "[$NN] download failed; cooling down ${backoff}s before retry..."
      sleep $backoff
    done
    [ "$dl_ok" = 1 ] || { echo "[$NN] DOWNLOAD FAILED after retries, skipping lecture."; continue; }
  fi

  # 2) ASR (1x, native timestamps)
  if [ ! -f "$OUT/audio/transcript.json" ]; then
    echo "[$NN] ASR..."
    $PY src/transcribe.py --video "$OUT/video.mp4" --output "$OUT/audio/transcript.json" \
      --device metal --backend mlx-whisper --model large-v3-turbo --language bg \
      >> "$OUT/pipeline.log" 2>&1 || { echo "[$NN] ASR FAILED"; continue; }
  fi

  # 3) board detection (full frame)
  if [ ! -f "$OUT/board_corners.json" ]; then
    echo "[$NN] detect..."
    $PY src/board_detection.py --video "$OUT/video.mp4" \
      --output-json "$OUT/board_corners.json" --output-rectified "$OUT/rectified.png" --no-rectify \
      >> "$OUT/pipeline.log" 2>&1 || { echo "[$NN] DETECT FAILED"; continue; }
  fi

  # 4) keyframes (coarse sampling ~= previous 3x behaviour)
  if [ ! -f "$OUT/board_states.json" ]; then
    echo "[$NN] track..."
    $PY src/board_tracking.py --video "$OUT/video.mp4" --corners "$OUT/board_corners.json" \
      --output-dir "$OUT/board" --interval 3.0 --stability 0.96 --threshold 0.965 \
      >> "$OUT/pipeline.log" 2>&1 || { echo "[$NN] TRACK FAILED"; continue; }
  fi
  NK=$(ls "$OUT/board"/*.png 2>/dev/null | wc -l | tr -d ' '); echo "[$NN] keyframes: $NK"

  # 5) parallel cloud OCR (resumable), then a serial pass to fill any failures
  echo "[$NN] OCR ($NK frames)..."
  $PY "$POCR" --board-states "$OUT/board_states.json" --board-dir "$OUT/board" \
    --out-dir "$OUT/ocr" --workers 3 >> "$OUT/pipeline.log" 2>&1
  $PY "$POCR" --board-states "$OUT/board_states.json" --board-dir "$OUT/board" \
    --out-dir "$OUT/ocr" --workers 1 >> "$OUT/pipeline.log" 2>&1
  NO=$(ls "$OUT/ocr"/*.json 2>/dev/null | wc -l | tr -d ' '); echo "[$NN] ocr json: $NO/$NK"

  # 6) align
  echo "[$NN] align..."
  $PY src/temporal_alignment.py --transcript "$OUT/audio/transcript.json" \
    --board-states "$OUT/board_states.json" --ocr-dir "$OUT/ocr" \
    --output-ir "$OUT/ir/lecture_ir.json" --window 30 >> "$OUT/pipeline.log" 2>&1 \
    || { echo "[$NN] ALIGN FAILED"; continue; }

  # 7) verify (SymPy only; zero RAM)
  echo "[$NN] verify..."
  $PY src/verify_math.py --ir "$OUT/ir/lecture_ir.json" --no-llm >> "$OUT/pipeline.log" 2>&1

  # 8) generate + compile (cloud agy, verbose)
  echo "[$NN] generate..."
  $PY src/note_generation.py --ir "$OUT/ir/lecture_ir.json" --output-dir "$OUT/latex" \
    --gen-mode cloud --provider agy --compiler pdflatex --max-retries 3 \
    >> "$OUT/pipeline.log" 2>&1
  if [ -f "$OUT/latex/lecture.pdf" ]; then echo "[$NN] DONE -> $OUT/latex/lecture.pdf"; else echo "[$NN] GEN did not produce PDF (see $OUT/pipeline.log)"; fi

  # If agy quota is exhausted, stop early rather than burning downloads with no OCR/gen.
  # Only treat it as a real quota stop when THIS lecture failed to produce a PDF AND
  # its OCR left frames unfilled (stale "quota reached" lines from a prior run linger
  # in the appended log, so a completed lecture must never trip this).
  if [ ! -f "$OUT/latex/lecture.pdf" ] && [ "${NO:-0}" -lt "${NK:-1}" ] \
       && grep -q "quota reached" "$OUT/pipeline.log" 2>/dev/null; then
    echo "[$NN] agy QUOTA REACHED — stopping batch. Re-run this script later to resume."; exit 3
  fi

  sleep 15   # brief pacing between lectures to ease YouTube rate-limiting
done
echo "================ BATCH COMPLETE $(date '+%H:%M:%S') ================"
