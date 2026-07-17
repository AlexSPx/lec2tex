import os
import sys
import json
import argparse

def perform_temporal_alignment(transcript_path, board_states_path, ocr_dir, output_ir_path, window_seconds=30):
    """
    Associates transcript speech segments with board states based on overlapping timestamps,
    and builds the Intermediate Representation (IR).
    """
    print(f"Reading transcript from {transcript_path}...")
    with open(transcript_path, "r", encoding="utf-8") as f:
        transcript = json.load(f)
        
    print(f"Reading board states from {board_states_path}...")
    with open(board_states_path, "r", encoding="utf-8") as f:
        board_states = json.load(f)
        
    # Determine the end of the transcript for bounding the last window
    transcript_end = 0.0
    for seg in transcript:
        seg_end = seg.get("end", seg.get("end_time", 0.0))
        if seg_end > transcript_end:
            transcript_end = seg_end

    # Pre-compute exclusive midpoint-based windows for each board state
    timestamps = [state["timestamp"] for state in board_states]

    ir_data = []
    
    for i, state in enumerate(board_states):
        timestamp = state["timestamp"]
        image_name = state["image"]
        base_name, _ = os.path.splitext(image_name)
        ocr_json_path = os.path.join(ocr_dir, f"{base_name}.json")
        
        # Load OCR results for this board state if they exist
        board_items = []
        if os.path.exists(ocr_json_path):
            try:
                with open(ocr_json_path, "r", encoding="utf-8") as f:
                    ocr_data = json.load(f)
                
                # We extract the current items on the board
                items = ocr_data.get("items", ocr_data.get("current_state", []))
                for item in items:
                    item_type = item.get("type", "text")
                    content = item.get("content", "")
                    
                    if item_type == "equation":
                        board_items.append({
                            "type": "equation",
                            "latex": content
                        })
                    else:
                        board_items.append({
                            "type": "text",
                            "text": content
                        })
            except Exception as e:
                print(f"Error loading OCR file {ocr_json_path}: {e}")
        else:
            print(f"Warning: OCR file {ocr_json_path} not found.")
            
        # Compute exclusive midpoint-based window for this board state
        # Window start: midpoint between previous state and current (0 for first)
        if i == 0:
            start_win = 0.0
        else:
            start_win = (timestamps[i - 1] + timestamps[i]) / 2.0

        # Window end: midpoint between current state and next (transcript end for last)
        if i == len(timestamps) - 1:
            end_win = transcript_end
        else:
            end_win = (timestamps[i] + timestamps[i + 1]) / 2.0
        
        overlapping_speech_parts = []
        for seg in transcript:
            seg_start = seg.get("start", seg.get("time", 0.0))
            seg_end = seg.get("end", seg.get("end_time", seg_start + 1.0))
            seg_text = seg.get("text", seg.get("content", ""))
            
            # Check overlap between [seg_start, seg_end] and [start_win, end_win)
            if max(seg_start, start_win) < min(seg_end, end_win):
                overlapping_speech_parts.append(seg_text.strip())
                
        # Concatenate overlapping speech
        speech_text = " ".join(overlapping_speech_parts)
        
        ir_data.append({
            "timestamp": timestamp,
            "image": image_name,
            "speech": speech_text,
            "board_items": board_items
        })
        
    # Ensure parent directory of output_ir_path exists
    os.makedirs(os.path.dirname(output_ir_path), exist_ok=True)
    
    with open(output_ir_path, "w", encoding="utf-8") as f:
        json.dump(ir_data, f, ensure_ascii=False, indent=2)
        
    print(f"Intermediate Representation saved to {output_ir_path} with {len(ir_data)} aligned states.")
    return ir_data

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Stage 6 & 7: Temporal Alignment and Intermediate Representation")
    parser.add_argument("--transcript", type=str, default="audio/transcript.json", help="Path to transcript JSON")
    parser.add_argument("--board-states", type=str, default="board_states.json", help="Path to board states JSON")
    parser.add_argument("--ocr-dir", type=str, default="ocr", help="Directory containing board OCR JSONs")
    parser.add_argument("--output-ir", type=str, default="ir/lecture_ir.json", help="Path to output lecture_ir.json")
    parser.add_argument("--window", type=float, default=30.0, help="Temporal window in seconds (T +/- window)")
    
    args = parser.parse_args()
    perform_temporal_alignment(args.transcript, args.board_states, args.ocr_dir, args.output_ir, args.window)
