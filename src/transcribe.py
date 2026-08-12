import os
import sys
import json
import argparse


def _transcribe_faster_whisper(video_path, model_size, device, compute_type):
    """CUDA/CPU path via faster-whisper (original behaviour)."""
    from faster_whisper import WhisperModel
    print(f"Loading faster-whisper '{model_size}' on {device} ({compute_type})...")
    try:
        model = WhisperModel(model_size, device=device, compute_type=compute_type)
    except Exception as e:
        print(f"Failed on {device}/{compute_type}, falling back to CPU/int8. Error: {e}")
        model = WhisperModel(model_size, device="cpu", compute_type="int8")

    segments, info = model.transcribe(video_path, language="bg", vad_filter=True, beam_size=5)
    print(f"Detected language: {info.language} (p={info.language_probability:.2f})")
    out = []
    for seg in segments:
        print(f"[{seg.start:.1f}s -> {seg.end:.1f}s]: {seg.text}")
        out.append({"start": round(seg.start, 2), "end": round(seg.end, 2),
                    "text": seg.text.strip()})
    return out


def _transcribe_mlx_whisper(video_path, model_size, language="bg"):
    """Apple-Silicon path via mlx-whisper (Metal)."""
    import mlx_whisper
    # Map plain sizes to MLX-community hub repos; a hub id / local path passes through.
    repo_map = {
        "large-v3": "mlx-community/whisper-large-v3-mlx",
        "large-v3-turbo": "mlx-community/whisper-large-v3-turbo",
        "medium": "mlx-community/whisper-medium-mlx",
        "small": "mlx-community/whisper-small-mlx",
    }
    repo = repo_map.get(model_size, model_size)
    print(f"Transcribing with mlx-whisper (Metal), model repo: {repo} ...")
    result = mlx_whisper.transcribe(
        video_path, path_or_hf_repo=repo, language=language,
        word_timestamps=False, verbose=False,
        # A lecture recording contains the class break, and a long stretch of
        # near-silence sends Whisper into a repetition loop: it emits a filler
        # caption ("Абонирайте се!"), conditions on its own output, and never
        # escapes. Lecture 13 lost 46 minutes this way — the audio was fine
        # (post-break RMS -36.1 dBFS against -36.3 pre-break), the decoder was
        # not. Turning conditioning off costs a little cross-sentence context
        # and buys immunity to the trap.
        condition_on_previous_text=False,
        temperature=(0.0, 0.2, 0.4, 0.6, 0.8, 1.0),
        compression_ratio_threshold=2.4,
        no_speech_threshold=0.6,
    )
    out = []
    for seg in result.get("segments", []):
        print(f"[{seg['start']:.1f}s -> {seg['end']:.1f}s]: {seg['text']}")
        out.append({"start": round(seg["start"], 2), "end": round(seg["end"], 2),
                    "text": seg["text"].strip()})
    return out


def transcribe_audio(video_path, output_path, model_size="large-v3", device="auto",
                     compute_type="int8_float16", backend="auto", language="bg"):
    """
    Device-aware transcription.
      backend "auto": mlx-whisper on metal, faster-whisper on cuda/cpu.
    """
    from backends import resolve_device
    dev = resolve_device(device)
    if backend == "auto":
        backend = "mlx-whisper" if dev == "metal" else "faster-whisper"

    print(f"ASR backend: {backend} (device={dev})")
    if backend == "mlx-whisper":
        transcript = _transcribe_mlx_whisper(video_path, model_size, language=language)
    elif backend == "nemo-canary":
        transcript = _transcribe_nemo_canary(video_path, model_size, language=language)
    else:  # faster-whisper
        fw_device = "cuda" if dev == "cuda" else "cpu"
        transcript = _transcribe_faster_whisper(video_path, model_size, fw_device, compute_type)

    check_hallucination(transcript)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(transcript, f, ensure_ascii=False, indent=2)
    print(f"Transcription complete ({len(transcript)} segments). Saved to {output_path}")
    return transcript


def check_hallucination(transcript, window_min=10, min_distinct=0.5):
    """Warn when a stretch of transcript collapses into repeated filler.

    Whisper's failure mode here is not a crash and not garbage text — it emits
    a small set of plausible captions over and over. The result parses fine,
    has sane timestamps, and reads as a normal transcript unless you count
    distinct strings. Lecture 13 sat in the repo for months with 46 minutes
    replaced by "Абонирайте се!" before anyone noticed.

    Healthy speech runs ~0.8-1.0 distinct segments per segment. A window below
    `min_distinct` is almost certainly a loop.
    """
    if not transcript:
        print("WARNING: empty transcript")
        return []
    bad = []
    end = max(s["end"] for s in transcript)
    step = window_min * 60
    lo = 0.0
    while lo < end:
        win = [s for s in transcript if lo <= s["start"] < lo + step]
        if len(win) >= 20:
            ratio = len({s["text"].strip() for s in win}) / len(win)
            if ratio < min_distinct:
                bad.append((lo / 60, (lo + step) / 60, ratio, len(win)))
        lo += step
    for a, b, r, n in bad:
        print(f"WARNING: minutes {a:.0f}-{b:.0f} look hallucinated "
              f"({r:.0%} distinct over {n} segments) — check the audio and "
              f"re-run that span with condition_on_previous_text=False")
    if not bad:
        print("hallucination check: no repetition loops detected")
    return bad


def _transcribe_nemo_canary(video_path, model_size, language="bg"):
    """CUDA-only path via NVIDIA NeMo Canary-1b-v2 (highest accuracy)."""
    from nemo.collections.asr.models import EncDecMultiTaskModel
    model_id = model_size if "/" in model_size else "nvidia/canary-1b-v2"
    print(f"Loading NeMo Canary: {model_id} (CUDA)...")
    m = EncDecMultiTaskModel.from_pretrained(model_id)
    hyps = m.transcribe([video_path], source_lang=language, target_lang=language,
                        timestamps=True)
    out = []
    for h in hyps:
        for seg in getattr(h, "timestamp", {}).get("segment", []):
            out.append({"start": round(seg["start"], 2), "end": round(seg["end"], 2),
                        "text": seg["segment"].strip()})
    return out


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Stage 1: Audio Transcription (device-aware)")
    parser.add_argument("--video", type=str, required=True)
    parser.add_argument("--output", type=str, default="audio/transcript.json")
    parser.add_argument("--model", type=str, default="large-v3", help="Whisper size / hub id / local path")
    parser.add_argument("--device", type=str, default="auto", choices=["auto", "metal", "cuda", "cpu"])
    parser.add_argument("--backend", type=str, default="auto",
                        choices=["auto", "mlx-whisper", "faster-whisper", "nemo-canary"])
    parser.add_argument("--compute_type", type=str, default="int8_float16")
    parser.add_argument("--language", type=str, default="bg")
    args = parser.parse_args()

    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    transcribe_audio(args.video, args.output, args.model, args.device,
                     args.compute_type, args.backend, args.language)
