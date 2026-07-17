import os
import sys
import argparse
import subprocess

def run_stage(command, stage_name):
    """
    Helper function to run a stage command and print its status.
    """
    print(f"\n==========================================")
    print(f"RUNNING: {stage_name}")
    print(f"COMMAND: {' '.join(command)}")
    print(f"==========================================\n")
    
    res = subprocess.run(command)
    if res.returncode != 0:
        print(f"\n[ERROR] {stage_name} failed with exit code {res.returncode}.")
        sys.exit(res.returncode)
    print(f"\n[SUCCESS] {stage_name} completed.\n")

def main():
    parser = argparse.ArgumentParser(description="lecture2latex: Convert lecture videos to structured LaTeX notes")
    parser.add_argument("--video", type=str, required=True, help="Path to input lecture video")
    parser.add_argument("--provider", type=str, default="agy", choices=["gemini", "openai", "agy"], help="LLM provider for note generation")
    parser.add_argument("--api-key", type=str, default=None, help="LLM API key (or set environment variable)")
    parser.add_argument("--model", type=str, default=None, help="LLM model name")
    parser.add_argument("--compiler", type=str, default="pdflatex", choices=["pdflatex", "lualatex"], help="LaTeX compiler to use")
    
    # Skipping options
    parser.add_argument("--skip-transcription", action="store_true", help="Skip Stage 1 (Audio Transcription)")
    parser.add_argument("--skip-detection", action="store_true", help="Skip Stage 2 (Whiteboard Corner Detection)")
    parser.add_argument("--skip-tracking", action="store_true", help="Skip Stage 3 (Whiteboard Change Tracking)")
    parser.add_argument("--skip-ocr", action="store_true", help="Skip Stage 4 & 5 (OCR and Board Evolution)")
    parser.add_argument("--skip-alignment", action="store_true", help="Skip Stage 6 & 7 (Temporal Alignment & IR)")
    parser.add_argument("--skip-generation", action="store_true", help="Skip Stage 8 & 9 (LLM Note Generation & Compile)")
    
    # Path settings
    parser.add_argument("--transcript-path", type=str, default="audio/transcript.json", help="Path to transcript.json")
    parser.add_argument("--corners-path", type=str, default="board_corners.json", help="Path to board corners JSON")
    parser.add_argument("--rectified-path", type=str, default="rectified_board.png", help="Path to rectified board template image")
    parser.add_argument("--board-dir", type=str, default="board", help="Directory to store board state images")
    parser.add_argument("--ocr-dir", type=str, default="ocr", help="Directory to store board state OCR results")
    parser.add_argument("--ir-path", type=str, default="ir/lecture_ir.json", help="Path to intermediate representation JSON")
    parser.add_argument("--latex-dir", type=str, default="latex", help="Directory to store final LaTeX files")
    
    # Heuristics
    parser.add_argument("--ssim-threshold", type=float, default=0.97, help="SSIM threshold for board change detection")
    parser.add_argument("--stability-threshold", type=float, default=0.98, help="SSIM threshold for board stability checking")
    parser.add_argument("--align-window", type=float, default=30.0, help="Speech alignment window (seconds)")
    
    # Whisper settings
    parser.add_argument("--whisper-model", type=str, default="large-v3", help="Whisper model size for transcription")
    parser.add_argument("--whisper-compute-type", type=str, default="int8_float16", help="Whisper compute type (float16, int8_float16, int8)")
    
    args = parser.parse_args()
    
    # Locate our virtualenv python interpreter
    venv_python = ".venv/bin/python"
    if not os.path.exists(venv_python):
        # Fall back to system python if venv isn't found
        venv_python = sys.executable

    # Ensure output directories exist
    os.makedirs(os.path.dirname(args.transcript_path), exist_ok=True)
    os.makedirs(args.board_dir, exist_ok=True)
    os.makedirs(args.ocr_dir, exist_ok=True)
    os.makedirs(os.path.dirname(args.ir_path), exist_ok=True)
    os.makedirs(args.latex_dir, exist_ok=True)

    # ------------------ Stage 1: Audio Transcription ------------------
    if not args.skip_transcription:
        cmd = [
            venv_python, "src/transcribe.py",
            "--video", args.video,
            "--output", args.transcript_path,
            "--model", args.whisper_model,
            "--compute_type", args.whisper_compute_type
        ]
        run_stage(cmd, "Stage 1: Audio Transcription (Faster-Whisper)")
    else:
        print("[INFO] Skipping Stage 1: Audio Transcription.")

    # ------------------ Stage 2: Whiteboard Detection ------------------
    if not args.skip_detection:
        cmd = [
            venv_python, "src/board_detection.py",
            "--video", args.video,
            "--output-json", args.corners_path,
            "--output-rectified", args.rectified_path
        ]
        run_stage(cmd, "Stage 2: Whiteboard Corner Detection & Rectification")
    else:
        print("[INFO] Skipping Stage 2: Whiteboard Detection.")

    # ------------------ Stage 3: Whiteboard State Tracking ------------------
    if not args.skip_tracking:
        cmd = [
            venv_python, "src/board_tracking.py",
            "--video", args.video,
            "--corners", args.corners_path,
            "--output-dir", args.board_dir,
            "--threshold", str(args.ssim_threshold),
            "--stability", str(args.stability_threshold)
        ]
        run_stage(cmd, "Stage 3: Whiteboard State Change Tracking (SSIM)")
    else:
        print("[INFO] Skipping Stage 3: Whiteboard State Tracking.")

    # ------------------ Stage 4 & 5: OCR and Board Evolution ------------------
    if not args.skip_ocr:
        # Note: We need to pass the board_states.json which is saved in the parent of board-dir
        board_states_json = os.path.join(os.path.dirname(args.board_dir), "board_states.json")
        cmd = [
            venv_python, "src/ocr_pipeline.py",
            "--board-states", board_states_json,
            "--output-dir", args.ocr_dir
        ]
        run_stage(cmd, "Stage 4 & 5: Layout OCR and Board Evolution Tracking")
    else:
        print("[INFO] Skipping Stage 4 & 5: OCR and Board Evolution.")

    # ------------------ Stage 6 & 7: Temporal Alignment & IR ------------------
    if not args.skip_alignment:
        board_states_json = os.path.join(os.path.dirname(args.board_dir), "board_states.json")
        cmd = [
            venv_python, "src/temporal_alignment.py",
            "--transcript", args.transcript_path,
            "--board-states", board_states_json,
            "--ocr-dir", args.ocr_dir,
            "--output-ir", args.ir_path,
            "--window", str(args.align_window)
        ]
        run_stage(cmd, "Stage 6 & 7: Temporal Alignment and Intermediate Representation")
    else:
        print("[INFO] Skipping Stage 6 & 7: Temporal Alignment & IR.")

    # ------------------ Stage 8 & 9: Note Generation & Validation ------------------
    if not args.skip_generation:
        cmd = [
            venv_python, "src/note_generation.py",
            "--ir", args.ir_path,
            "--output-dir", args.latex_dir,
            "--provider", args.provider,
            "--compiler", args.compiler
        ]
        if args.api_key:
            cmd.extend(["--api-key", args.api_key])
        if args.model:
            cmd.extend(["--model", args.model])
            
        run_stage(cmd, "Stage 8 & 9: LLM Note Generation & LaTeX Compilation")
    else:
        print("[INFO] Skipping Stage 8 & 9: LLM Note Generation & Compile.")

    print("\n==========================================")
    print("lecture2latex pipeline completed successfully!")
    print("==========================================\n")

if __name__ == "__main__":
    main()
