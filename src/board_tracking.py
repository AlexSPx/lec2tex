import os
import sys
import json
import argparse
import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim

def track_board_states(video_path, corners_path, output_dir, time_interval=1.0, ssim_threshold=0.97, stability_threshold=0.98):
    """
    Tracks changes on the whiteboard and saves unique states.
    Uses a dual-SSIM approach to capture stable, occlusion-free board states.
    """
    os.makedirs(output_dir, exist_ok=True)
    
    # Load corners
    with open(corners_path, "r") as f:
        corners_data = json.load(f)
    corners = np.array(corners_data["corners"], dtype="float32")
    
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError(f"Could not open video file: {video_path}")
        
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    if fps == 0:
        fps = 30.0
        
    duration = total_frames / fps
    print(f"Tracking board states. Duration: {duration:.2f}s, Interval: {time_interval}s")
    
    # Determine output dimensions for rectified board
    tl, tr, br, bl = corners
    width = int(max(np.linalg.norm(br - bl), np.linalg.norm(tr - tl)))
    height = int(max(np.linalg.norm(tr - br), np.linalg.norm(tl - bl)))
    
    # Target size for warped board (high-res for storage and OCR)
    target_w = 1280
    target_h = 720
    
    dst_pts = np.array([
        [0, 0],
        [target_w - 1, 0],
        [target_w - 1, target_h - 1],
        [0, target_h - 1]
    ], dtype="float32")
    
    M = cv2.getPerspectiveTransform(corners, dst_pts)
    
    board_states = []
    last_saved_gray = None
    prev_gray = None
    
    state_counter = 0
    
    # Calculate skip interval in frames
    frame_skip = int(time_interval * fps)
    if frame_skip < 1:
        frame_skip = 1
        
    print(f"Frame skip interval: {frame_skip} frames (equivalent to {time_interval}s)")
    
    frame_idx = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        if frame_idx % frame_skip == 0:
            t = frame_idx / fps
            
            # Warp the board region (high-res)
            warped = cv2.warpPerspective(frame, M, (target_w, target_h))
            # Convert to gray
            gray = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
            # Apply slight blur to reduce high-frequency noise
            gray_blurred = cv2.GaussianBlur(gray, (5, 5), 0)
            
            # Downsample specifically for fast SSIM calculation (320x180 is very fast and ignores pixel noise)
            gray_small = cv2.resize(gray_blurred, (320, 180), interpolation=cv2.INTER_AREA)
            
            if last_saved_gray is None:
                # First frame is always saved as initial state
                state_counter += 1
                img_name = f"board_{state_counter:03d}.png"
                img_path = os.path.join(output_dir, img_name)
                cv2.imwrite(img_path, warped)
                
                board_states.append({
                    "timestamp": round(t, 2),
                    "image": img_name
                })
                
                last_saved_gray = gray_small
                print(f"Saved initial board state at {t:.2f}s: {img_name}")
            else:
                # Compute SSIM on downsampled images
                sim_consec = ssim(gray_small, prev_gray)
                sim_saved = ssim(gray_small, last_saved_gray)
                
                # Check for stability and content change
                if sim_consec >= stability_threshold and sim_saved < ssim_threshold:
                    state_counter += 1
                    img_name = f"board_{state_counter:03d}.png"
                    img_path = os.path.join(output_dir, img_name)
                    cv2.imwrite(img_path, warped)
                    
                    board_states.append({
                        "timestamp": round(t, 2),
                        "image": img_name
                    })
                    
                    last_saved_gray = gray_small
                    print(f"Saved board state {state_counter} at {t:.2f}s: {img_name} (consec_sim={sim_consec:.3f}, saved_sim={sim_saved:.3f})")
                    
            prev_gray = gray_small
            
        frame_idx += 1
        
    cap.release()
    
    # Save the states list JSON
    states_json_path = os.path.join(os.path.dirname(output_dir), "board_states.json")
    with open(states_json_path, "w") as f:
        json.dump(board_states, f, indent=2)
        
    print(f"Finished board state tracking. Extracted {len(board_states)} board states.")
    return board_states

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Stage 3: Whiteboard State Tracking")
    parser.add_argument("--video", type=str, required=True, help="Path to input video")
    parser.add_argument("--corners", type=str, default="board_corners.json", help="Path to board corners JSON")
    parser.add_argument("--output-dir", type=str, default="board", help="Directory to save board state images")
    parser.add_argument("--interval", type=float, default=1.0, help="Sampling interval in seconds")
    parser.add_argument("--threshold", type=float, default=0.97, help="SSIM threshold for state change detection")
    parser.add_argument("--stability", type=float, default=0.98, help="SSIM threshold for stability checking")
    
    args = parser.parse_args()
    track_board_states(args.video, args.corners, args.output_dir, args.interval, args.threshold, args.stability)
