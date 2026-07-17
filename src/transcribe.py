import os
import sys
import json
import argparse
from faster_whisper import WhisperModel

def transcribe_audio(video_path, output_path, model_size="large-v3", device="cuda", compute_type="int8_float16"):
    """
    Transcribes the audio from the video file using faster-whisper.
    """
    print(f"Loading Whisper model '{model_size}' on {device} ({compute_type})...")
    # For a 4GB GPU, float16 or int8_float16 is highly recommended to avoid OOM
    try:
        model = WhisperModel(model_size, device=device, compute_type=compute_type)
    except Exception as e:
        print(f"Failed to load model on {device} with {compute_type}. Falling back to CPU/int8... Error: {e}")
        model = WhisperModel(model_size, device="cpu", compute_type="int8")

    print(f"Transcribing video: {video_path}...")
    segments, info = model.transcribe(
        video_path,
        language="bg",
        vad_filter=True,
        beam_size=5
    )

    print(f"Detected language: {info.language} with probability {info.language_probability:.2f}")
    
    transcript = []
    for segment in segments:
        print(f"[{segment.start:.1f}s -> {segment.end:.1f}s]: {segment.text}")
        transcript.append({
            "start": round(segment.start, 2),
            "end": round(segment.end, 2),
            "text": segment.text.strip()
        })

    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(transcript, f, ensure_ascii=False, indent=2)

    print(f"Transcription complete. Saved to {output_path}")
    return transcript

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Stage 1: Audio Transcription with Faster-Whisper")
    parser.add_argument("--video", type=str, required=True, help="Path to input lecture video")
    parser.add_argument("--output", type=str, default="audio/transcript.json", help="Path to output transcript.json")
    parser.add_argument("--model", type=str, default="large-v3", help="Whisper model size")
    parser.add_argument("--device", type=str, default="cuda", help="Device to run on (cuda or cpu)")
    parser.add_argument("--compute_type", type=str, default="int8_float16", help="Compute type (float16, int8_float16, int8)")

    args = parser.parse_args()
    transcribe_audio(args.video, args.output, args.model, args.device, args.compute_type)
