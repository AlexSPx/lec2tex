# Lec2LaTeX Pipeline

A multi-stage pipeline designed to convert lecture videos (Bulgarian audio + whiteboard content) into clean, well-formatted, and compilable LaTeX notes. 

Rather than a simple frame-by-frame transcript, this pipeline aligns spoken Bulgarian content with whiteboard changes, translates the spoken explanations into professional academic English, reconstructs mathematical equations using specialized OCR (`pix2tex`), tracks whiteboard additions/erasures, and runs a self-correcting LaTeX compilation validation loop.

## Architecture Overview

```
Video Input
 │
 ├── Stage 1: Audio Transcription (Faster-Whisper large-v3)
 │
 ├── Stage 2: Whiteboard Corner Detection & Homography Rectification (OpenCV)
 │
 ├── Stage 3: Whiteboard Change Tracking (SSIM-based keyframe extraction)
 │
 ├── Stage 4 & 5: Layout OCR & Evolution Tracking (PaddleOCR + pix2tex + IoU Matching)
 │
 ├── Stage 6 & 7: Temporal Alignment & Intermediate Representation (IR Output)
 │
 ├── Stage 8: LLM-Based Note Generation (Gemini / OpenAI translation & structuring)
 │
 └── Stage 9: Validation & Self-Correction Loop (Docker-based compilation & LLM correction)
```

## Repository Structure

```
lecture2latex/
│
├── audio/                  # Outputs from Stage 1
│   └── transcript.json
│
├── board/                  # Outputs from Stage 2 & 3
│   ├── board_001.png
│   ├── board_002.png
│   └── ...
│
├── ocr/                    # Outputs from Stage 4 & 5
│   ├── board_001.json
│   ├── board_002.json
│   └── ...
│
├── ir/                     # Outputs from Stage 6 & 7
│   └── lecture_ir.json
│
├── latex/                  # Outputs from Stage 8 & 9
│   ├── lecture.tex
│   └── lecture.pdf
│
├── src/                    # Pipeline source code
│   ├── main.py             # Orchestrator entrypoint
│   ├── transcribe.py       # Stage 1
│   ├── board_detection.py  # Stage 2
│   ├── board_tracking.py   # Stage 3
│   ├── ocr_pipeline.py     # Stage 4 & 5
│   ├── temporal_alignment.py # Stage 6 & 7
│   └── note_generation.py  # Stage 8 & 9
│
├── .gitignore              # Ignores outputs, virtual environments, and media
└── README.md
```

## Setup Instructions

### Prerequisites
- Python 3.10+
- FFMPEG
- Docker (for LaTeX compilation container `texlive/texlive:latest`)

### Installation
1. Initialize the virtual environment and install core dependencies:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install --upgrade pip
   pip install faster-whisper opencv-python-headless scikit-image pix2tex
   pip install paddlepaddle paddleocr
   ```

2. Pull the LaTeX compilation Docker image:
   ```bash
   docker pull texlive/texlive:latest
   ```

## Running the Pipeline

### Simple Run (No API Keys Required)
By default, the pipeline uses the local `agy` CLI in headless mode for all LLM queries, which is already authenticated and installed on your machine. No API keys are required.

To run the pipeline on the GPU, you must first export the correct library paths (which maps the CUDA 13 libraries in `.venv` and falls back to CUDA 12 libraries in `math-env` for `faster-whisper`):

```bash
export LD_LIBRARY_PATH=$(.venv/bin/python -c 'import os, sys; paths = []; nd1 = os.path.join(".venv", "lib", f"python{sys.version_info.major}.{sys.version_info.minor}", "site-packages", "nvidia"); paths.extend([os.path.abspath(os.path.join(nd1, d, "lib")) for d in os.listdir(nd1) if os.path.isdir(os.path.join(nd1, d))]) if os.path.exists(nd1) else None; nd2 = "/home/alexspx/Documents/transcribe/math-env/lib/python3.13/site-packages/nvidia"; paths.extend([os.path.abspath(os.path.join(nd2, d, "lib")) for d in os.listdir(nd2) if os.path.isdir(os.path.join(nd2, d))]) if os.path.exists(nd2) else None; print(":".join([p for p in paths if os.path.exists(p)]))'):$LD_LIBRARY_PATH

.venv/bin/python src/main.py --video path/to/lecture.mp4
```

### Alternative Run (External LLMs)
If you prefer to use an external API via an API key:

```bash
# Setup CUDA environment (as above)
export LD_LIBRARY_PATH=$(.venv/bin/python -c 'import os, sys; paths = []; nd1 = os.path.join(".venv", "lib", f"python{sys.version_info.major}.{sys.version_info.minor}", "site-packages", "nvidia"); paths.extend([os.path.abspath(os.path.join(nd1, d, "lib")) for d in os.listdir(nd1) if os.path.isdir(os.path.join(nd1, d))]) if os.path.exists(nd1) else None; nd2 = "/home/alexspx/Documents/transcribe/math-env/lib/python3.13/site-packages/nvidia"; paths.extend([os.path.abspath(os.path.join(nd2, d, "lib")) for d in os.listdir(nd2) if os.path.isdir(os.path.join(nd2, d))]) if os.path.exists(nd2) else None; print(":".join([p for p in paths if os.path.exists(p)]))'):$LD_LIBRARY_PATH

export GEMINI_API_KEY="your_api_key_here"
.venv/bin/python src/main.py --video path/to/lecture.mp4 --provider gemini
```

### Skipping Completed Stages
If you have already processed part of the video and want to tweak subsequent stages (e.g. adjust alignment window, or regenerate notes without re-running transcription/OCR):

```bash
.venv/bin/python src/main.py --video path/to/lecture.mp4 \
    --skip-transcription \
    --skip-detection \
    --skip-tracking \
    --skip-ocr
```

### Parameter Reference

- `--video`: (Required) Path to the input MP4/MKV video.
- `--provider`: Choose `agy` (default, keyless), `gemini`, or `openai` for LLM notes generation.
- `--api-key`: API key for external LLM providers (ignored for `agy`, falls back to env variables for others).
- `--model`: Custom LLM model name.
- `--compiler`: LaTeX compiler command run inside Docker (`pdflatex` or `lualatex`).
- `--ssim-threshold`: SSIM similarity threshold (default `0.97`) to detect whiteboard changes.
- `--stability-threshold`: SSIM threshold (default `0.98`) to check if the lecturer has finished writing/moving.
- `--align-window`: Transcript alignment window in seconds (default `30.0`), mapping transcript segments to `board_timestamp ± window`.
- `--whisper-model`: Whisper model size (`large-v3`, `medium`, `small`, etc., default: `large-v3`).
- `--whisper-compute-type`: Compute precision (`int8_float16` for VRAM optimization, `float16` for full precision, default: `int8_float16`).
