import os
import sys
import json
import argparse
import cv2
import numpy as np

def get_median_frame(video_path, num_frames=15, max_check_seconds=300):
    """
    Samples frames from the video and computes the median frame
    to remove moving objects (like the lecturer) and get a clean whiteboard background.
    """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError(f"Could not open video file: {video_path}")
    
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps == 0:
        fps = 30.0
        
    duration = total_frames / fps
    print(f"Video duration: {duration:.2f} seconds ({total_frames} frames at {fps:.2f} fps)")
    
    # We sample frames from the first max_check_seconds (e.g. 5 minutes) of the video
    limit_time = min(duration, max_check_seconds)
    frame_indices = np.linspace(0, int(limit_time * fps) - 1, num_frames, dtype=int)
    
    sampled_frames = []
    for idx in frame_indices:
        cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
        ret, frame = cap.read()
        if ret:
            sampled_frames.append(frame)
            
    cap.release()
    
    if not sampled_frames:
        raise ValueError("Failed to extract any frames from the video.")
        
    print(f"Loaded {len(sampled_frames)} frames for median filtering.")
    median_frame = np.median(sampled_frames, axis=0).astype(np.uint8)
    return median_frame

def sort_corners(pts):
    """
    Sorts 4 corners in order: top-left, top-right, bottom-right, bottom-left.
    """
    pts = np.array(pts, dtype="float32").reshape(4, 2)
    # Sort by x-coordinate
    x_sorted = pts[np.argsort(pts[:, 0]), :]
    left_most = x_sorted[:2, :]
    right_most = x_sorted[2:, :]
    
    # Sort left-most by y-coordinate to get top-left and bottom-left
    left_most = left_most[np.argsort(left_most[:, 1]), :]
    tl, bl = left_most[0], left_most[1]
    
    # Sort right-most by y-coordinate to get top-right and bottom-right
    right_most = right_most[np.argsort(right_most[:, 1]), :]
    tr, br = right_most[0], right_most[1]
    
    return np.array([tl, tr, br, bl], dtype="float32")

def detect_whiteboard_corners(img):
    """
    Attempts to detect whiteboard corners using OpenCV contour detection.
    """
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Apply Gaussian blur to reduce noise and help with contour detection
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Adaptive thresholding to handle lighting variations
    thresh = cv2.adaptiveThreshold(
        blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV, 11, 2
    )
    
    # Find contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    print(f"Found {len(contours)} initial contours.")
    
    # Filter contours by size (should be a large portion of the frame)
    h, w = img.shape[:2]
    min_area = 0.15 * (w * h)  # Must cover at least 15% of the frame
    
    quad_contours = []
    for c in contours:
        area = cv2.contourArea(c)
        if area < min_area:
            continue
            
        # Approximate contour to polygon
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        
        # We are looking for a quadrilateral
        if len(approx) == 4 and cv2.isContourConvex(approx):
            quad_contours.append((area, approx))
            
    if quad_contours:
        # Sort by area descending and pick the largest
        quad_contours.sort(key=lambda x: x[0], reverse=True)
        best_contour = quad_contours[0][1]
        corners = best_contour.reshape(4, 2)
        print("Successfully detected whiteboard corners via contour analysis!")
        return sort_corners(corners)
        
    print("Whiteboard contour detection failed. Falling back to default heuristics.")
    # Fallback heuristic: assume whiteboard is centered, occupying 80% of the screen
    # or look for Hough lines (which can be noisy), so we return a default bounding box
    tl = [int(w * 0.1), int(h * 0.1)]
    tr = [int(w * 0.9), int(h * 0.1)]
    br = [int(w * 0.9), int(h * 0.9)]
    bl = [int(w * 0.1), int(h * 0.9)]
    return np.array([tl, tr, br, bl], dtype="float32")

def rectify_image(img, corners, target_width=None, target_height=None):
    """
    Applies perspective correction (homography) to warp the whiteboard area
    into a flat, front-facing rectangular image.
    """
    tl, tr, br, bl = corners
    
    # Compute the width of the new image
    width_a = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    width_b = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    max_width = max(int(width_a), int(width_b))
    
    # Compute the height of the new image
    height_a = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    height_b = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    max_height = max(int(height_a), int(height_b))
    
    if target_width is not None:
        max_width = target_width
    if target_height is not None:
        max_height = target_height
        
    dst = np.array([
        [0, 0],
        [max_width - 1, 0],
        [max_width - 1, max_height - 1],
        [0, max_height - 1]
    ], dtype="float32")
    
    M = cv2.getPerspectiveTransform(corners, dst)
    warped = cv2.warpPerspective(img, M, (max_width, max_height))
    return warped, M

def main():
    parser = argparse.ArgumentParser(description="Stage 2: Whiteboard Detection and Rectification")
    parser.add_argument("--video", type=str, required=True, help="Path to input video")
    parser.add_argument("--output-json", type=str, default="board_corners.json", help="Path to save corners JSON")
    parser.add_argument("--output-rectified", type=str, default="rectified_board.png", help="Path to save rectified board image")
    parser.add_argument("--manual-corners", type=str, default=None, help="Optional manual corners JSON path or raw list [[x,y],...]")
    args = parser.parse_args()
    
    # Get a clean background frame using median filter
    print("Generating median frame from video...")
    median_frame = get_median_frame(args.video)
    
    corners = None
    if args.manual_corners:
        try:
            if os.path.exists(args.manual_corners):
                with open(args.manual_corners, "r") as f:
                    data = json.load(f)
                    if "corners" in data:
                        corners = np.array(data["corners"], dtype="float32")
                    elif "x1" in data:
                        x1, y1, x2, y2 = data["x1"], data["y1"], data["x2"], data["y2"]
                        corners = np.array([[x1, y1], [x2, y1], [x2, y2], [x1, y2]], dtype="float32")
            else:
                pts = json.loads(args.manual_corners)
                corners = np.array(pts, dtype="float32")
            corners = sort_corners(corners)
            print("Loaded manual calibration corners.")
        except Exception as e:
            print(f"Error parsing manual corners: {e}. Running auto-detection instead.")
            
    if corners is None:
        corners = detect_whiteboard_corners(median_frame)
        
    # Get bounding box coordinates as requested
    x1 = int(np.min(corners[:, 0]))
    y1 = int(np.min(corners[:, 1]))
    x2 = int(np.max(corners[:, 0]))
    y2 = int(np.max(corners[:, 1]))
    
    corners_list = corners.tolist()
    
    output_data = {
        "x1": x1,
        "y1": y1,
        "x2": x2,
        "y2": y2,
        "corners": corners_list
    }
    
    # Save corners
    with open(args.output_json, "w") as f:
        json.dump(output_data, f, indent=2)
    print(f"Corners saved to {args.output_json}: bounding box [({x1}, {y1}), ({x2}, {y2})]")
    
    # Perform perspective correction and save rectified board
    print("Rectifying whiteboard perspective...")
    rectified_img, _ = rectify_image(median_frame, corners)
    cv2.imwrite(args.output_rectified, rectified_img)
    print(f"Rectified board saved to {args.output_rectified}")

if __name__ == "__main__":
    main()
