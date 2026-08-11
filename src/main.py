import os
import sys
import argparse
import subprocess


def run_stage(command, stage_name):
    print(f"\n==========================================")
    print(f"RUNNING: {stage_name}")
    print(f"COMMAND: {' '.join(command)}")
    print(f"==========================================\n")
    res = subprocess.run(command)
    if res.returncode != 0:
        print(f"\n[ERROR] {stage_name} failed with exit code {res.returncode}.")
        sys.exit(res.returncode)
    print(f"\n[SUCCESS] {stage_name} completed.\n")


def _mode_for(step_mode, global_mode):
    return step_mode or global_mode


def main():
    parser = argparse.ArgumentParser(description="lec2tex: lecture video -> LaTeX notes (dual-backend, local-first)")
    parser.add_argument("--video", type=str, required=True, help="Path to input lecture video")

    # Global backend controls
    parser.add_argument("--mode", choices=["local", "cloud"], default="local",
                        help="Default local/cloud mode for every model step (per-step flags override)")
    parser.add_argument("--device", choices=["auto", "metal", "cuda", "cpu"], default="auto",
                        help="Local acceleration backend")

    # Per-step mode + model + base-url + provider
    for step in ["asr", "ocr", "verify", "gen"]:
        parser.add_argument(f"--{step}-mode", choices=["local", "cloud"], default=None)
        parser.add_argument(f"--{step}-model", default=None)
        parser.add_argument(f"--{step}-base-url", default=None)
        parser.add_argument(f"--{step}-provider", default=None)

    # Cloud provider defaults (legacy compatibility for generation)
    parser.add_argument("--provider", type=str, default="agy", choices=["gemini", "openai", "agy"],
                        help="Cloud provider for note generation when gen runs in cloud mode")
    parser.add_argument("--api-key", type=str, default=None)
    parser.add_argument("--compiler", type=str, default="pdflatex", choices=["pdflatex", "lualatex"])

    # ASR
    parser.add_argument("--asr-backend", default="auto",
                        choices=["auto", "mlx-whisper", "faster-whisper", "nemo-canary"])
    parser.add_argument("--whisper-model", type=str, default="large-v3")
    parser.add_argument("--whisper-compute-type", type=str, default="int8_float16")

    # Board detection / tracking
    parser.add_argument("--no-rectify", action="store_true",
                        help="Skip perspective detection; feed the full frame to the VLM")
    parser.add_argument("--ssim-threshold", type=float, default=0.97)
    parser.add_argument("--stability-threshold", type=float, default=0.98)
    parser.add_argument("--align-window", type=float, default=30.0)

    # Skips
    parser.add_argument("--skip-transcription", action="store_true")
    parser.add_argument("--skip-detection", action="store_true")
    parser.add_argument("--skip-tracking", action="store_true")
    parser.add_argument("--skip-ocr", action="store_true")
    parser.add_argument("--skip-alignment", action="store_true")
    parser.add_argument("--skip-verification", action="store_true")
    parser.add_argument("--skip-generation", action="store_true")

    # Paths
    parser.add_argument("--transcript-path", type=str, default="audio/transcript.json")
    parser.add_argument("--corners-path", type=str, default="board_corners.json")
    parser.add_argument("--rectified-path", type=str, default="rectified_board.png")
    parser.add_argument("--board-dir", type=str, default="board")
    parser.add_argument("--ocr-dir", type=str, default="ocr")
    parser.add_argument("--ir-path", type=str, default="ir/lecture_ir.json")
    parser.add_argument("--latex-dir", type=str, default="latex")

    args = parser.parse_args()

    venv_python = ".venv/bin/python"
    if not os.path.exists(venv_python):
        venv_python = sys.executable

    os.makedirs(os.path.dirname(args.transcript_path), exist_ok=True)
    os.makedirs(args.board_dir, exist_ok=True)
    os.makedirs(args.ocr_dir, exist_ok=True)
    os.makedirs(os.path.dirname(args.ir_path), exist_ok=True)
    os.makedirs(args.latex_dir, exist_ok=True)

    board_states_json = os.path.join(os.path.dirname(args.board_dir), "board_states.json")

    def backend_flags(step):
        """Common --<step>-* passthrough for a substage."""
        mode = _mode_for(getattr(args, f"{step}_mode"), args.mode)
        flags = [f"--{step}-mode", mode]
        model = getattr(args, f"{step}_model")
        base = getattr(args, f"{step}_base_url")
        prov = getattr(args, f"{step}_provider")
        if model:
            flags += [f"--{step}-model", model]
        if base:
            flags += [f"--{step}-base-url", base]
        if prov:
            flags += [f"--{step}-provider", prov]
        return flags

    # ------------------ Stage 1: Transcription ------------------
    if not args.skip_transcription:
        cmd = [venv_python, "src/transcribe.py", "--video", args.video,
               "--output", args.transcript_path, "--model", args.whisper_model,
               "--device", args.device, "--backend", args.asr_backend,
               "--compute_type", args.whisper_compute_type]
        run_stage(cmd, "Stage 1: Audio Transcription")
    else:
        print("[INFO] Skipping Stage 1.")

    # ------------------ Stage 2: Board detection ------------------
    if not args.skip_detection:
        cmd = [venv_python, "src/board_detection.py", "--video", args.video,
               "--output-json", args.corners_path, "--output-rectified", args.rectified_path]
        if args.no_rectify:
            cmd.append("--no-rectify")
        run_stage(cmd, "Stage 2: Whiteboard Corner Detection")
    else:
        print("[INFO] Skipping Stage 2.")

    # ------------------ Stage 3: Keyframe tracking ------------------
    if not args.skip_tracking:
        cmd = [venv_python, "src/board_tracking.py", "--video", args.video,
               "--corners", args.corners_path, "--output-dir", args.board_dir,
               "--threshold", str(args.ssim_threshold), "--stability", str(args.stability_threshold)]
        run_stage(cmd, "Stage 3: Board Keyframe Extraction (SSIM)")
    else:
        print("[INFO] Skipping Stage 3.")

    # ------------------ Stage 4: VLM board OCR ------------------
    if not args.skip_ocr:
        cmd = [venv_python, "src/vlm_ocr.py", "--board-states", board_states_json,
               "--output-dir", args.ocr_dir, "--board-dir", args.board_dir,
               "--device", args.device] + backend_flags("ocr")
        run_stage(cmd, "Stage 4: VLM Whole-Board OCR")
    else:
        print("[INFO] Skipping Stage 4.")

    # ------------------ Stage 5: Temporal alignment ------------------
    if not args.skip_alignment:
        cmd = [venv_python, "src/temporal_alignment.py", "--transcript", args.transcript_path,
               "--board-states", board_states_json, "--ocr-dir", args.ocr_dir,
               "--output-ir", args.ir_path, "--window", str(args.align_window)]
        run_stage(cmd, "Stage 5: Temporal Alignment & IR")
    else:
        print("[INFO] Skipping Stage 5.")

    # ------------------ Stage 6: Math verification ------------------
    if not args.skip_verification:
        cmd = [venv_python, "src/verify_math.py", "--ir", args.ir_path,
               "--device", args.device] + backend_flags("verify")
        run_stage(cmd, "Stage 6: Math Verification (SymPy + LLM)")
    else:
        print("[INFO] Skipping Stage 6.")

    # ------------------ Stage 7: Generation + compile ------------------
    if not args.skip_generation:
        gen_mode = _mode_for(args.gen_mode, args.mode)
        cmd = [venv_python, "src/note_generation.py", "--ir", args.ir_path,
               "--output-dir", args.latex_dir, "--compiler", args.compiler,
               "--gen-mode", gen_mode, "--device", args.device]
        if gen_mode == "local":
            if args.gen_base_url:
                cmd += ["--gen-base-url", args.gen_base_url]
            if args.gen_model:
                cmd += ["--model", args.gen_model]
        else:
            cmd += ["--provider", args.gen_provider or args.provider]
            if args.api_key:
                cmd += ["--api-key", args.api_key]
            if args.gen_model:
                cmd += ["--model", args.gen_model]
        run_stage(cmd, "Stage 7: Note Generation & LaTeX Compile")
    else:
        print("[INFO] Skipping Stage 7.")

    print("\n==========================================")
    print("lec2tex pipeline completed successfully!")
    print("==========================================\n")


if __name__ == "__main__":
    main()
