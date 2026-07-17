import os
os.environ["PADDLE_PDX_ENABLE_MKLDNN_BYDEFAULT"] = "0"
os.environ["FLAGS_use_mkldnn"] = "0"
import sys
import json
import argparse
import re
import gc
import cv2
import numpy as np
import torch
from PIL import Image
from difflib import SequenceMatcher

def is_cyrillic(text):
    """
    Returns True if the text contains Cyrillic characters (Bulgarian speech/text indicator).
    """
    return bool(re.search(r'[\u0400-\u04FF]', text))

def has_math_symbols(text):
    """
    Returns True if the text contains common math operators, symbols, or LaTeX-like patterns.
    """
    math_chars = set('∫∑∏√±=<>{}^_\\')
    if any(ch in math_chars for ch in text):
        return True
    # Check for LaTeX-like command patterns (e.g. \frac, \alpha)
    if re.search(r'\\[a-zA-Z]+', text):
        return True
    return False

def compute_iou(boxA, boxB):
    """
    Computes Intersection over Union (IoU) of two axis-aligned bounding boxes.
    Each box is represented by [xmin, ymin, xmax, ymax].
    """
    xA = max(boxA[0], boxB[0])
    yA = max(boxA[1], boxB[1])
    xB = min(boxA[2], boxB[2])
    yB = min(boxA[3], boxB[3])
    
    inter_area = max(0, xB - xA) * max(0, yB - yA)
    boxA_area = (boxA[2] - boxA[0]) * (boxA[3] - boxA[1])
    boxB_area = (boxB[2] - boxB[0]) * (boxB[3] - boxB[1])
    
    union_area = boxA_area + boxB_area - inter_area
    if union_area == 0:
        return 0.0
    return inter_area / union_area

def get_rect(bbox):
    """
    Converts 4-point bounding box [[x1, y1], [x2, y2], [x3, y3], [x4, y4]] to [xmin, ymin, xmax, ymax].
    """
    xs = [p[0] for p in bbox]
    ys = [p[1] for p in bbox]
    return [min(xs), min(ys), max(xs), max(ys)]

def sort_bounding_boxes(items):
    """
    Sorts 2D bounding boxes in natural reading order (top-to-bottom, left-to-right).
    """
    if not items:
        return []
        
    # Convert bboxes to [ymin, xmin, ymax, xmax] for sorting
    prepared = []
    for item in items:
        rect = get_rect(item["bbox"])
        prepared.append({
            "ymin": rect[1], "xmin": rect[0],
            "ymax": rect[3], "xmax": rect[2],
            "item": item
        })
        
    # Sort primarily by ymin
    prepared.sort(key=lambda x: x["ymin"])
    
    # Group items into lines based on vertical overlap
    lines = []
    for it in prepared:
        placed = False
        for line in lines:
            line_ymin = min(x["ymin"] for x in line)
            line_ymax = max(x["ymax"] for x in line)
            line_h = line_ymax - line_ymin
            overlap = min(it["ymax"], line_ymax) - max(it["ymin"], line_ymin)
            
            # If overlap is more than 40% of either box height, group them in the same line
            if overlap > 0.4 * min(it["ymax"] - it["ymin"], line_h):
                line.append(it)
                placed = True
                break
        if not placed:
            lines.append([it])
            
    # Sort lines by y-coordinate, and items within lines by x-coordinate
    sorted_items = []
    lines.sort(key=lambda line: min(x["ymin"] for x in line))
    for line in lines:
        line.sort(key=lambda x: x["xmin"])
        for it in line:
            sorted_items.append(it["item"])
            
    return sorted_items

def run_ocr_pipeline(board_states_path, output_dir, use_gpu=True):
    """
    Loads models, runs OCR layout/recognition on board states, and tracks evolution.
    """
    # Import late to avoid startup delays or missing package errors on initial import
    from paddleocr import PaddleOCR
    from pix2tex.cli import LatexOCR
    
    print("Initializing PaddleOCR...")
    ocr_device = "gpu" if use_gpu else "cpu"
    paddle_ocr = PaddleOCR(use_textline_orientation=True, lang='bg', device=ocr_device, enable_mkldnn=False)
    
    print("Initializing pix2tex (LatexOCR)...")
    latex_ocr = LatexOCR()
    
    with open(board_states_path, "r", encoding="utf-8") as f:
        board_states = json.load(f)
        
    os.makedirs(output_dir, exist_ok=True)
    
    prev_items = []
    
    for idx, state in enumerate(board_states):
        image_name = state["image"]
        timestamp = state["timestamp"]
        image_path = os.path.join(os.path.dirname(board_states_path), "board", image_name)
        
        if not os.path.exists(image_path):
            # Try loading directly if folder is structured differently
            image_path = os.path.join(os.path.dirname(board_states_path), image_name)
            
        # Check if output JSON already exists to support resume
        base_name, _ = os.path.splitext(image_name)
        state_output_path = os.path.join(output_dir, f"{base_name}.json")
        if os.path.exists(state_output_path):
            print(f"Board state {idx+1}/{len(board_states)} already processed. Resuming from cache...")
            try:
                with open(state_output_path, "r", encoding="utf-8") as f:
                    cached_data = json.load(f)
                    prev_items = cached_data.get("items", [])
                continue
            except Exception as e:
                print(f"Failed to read cache for {image_name}: {e}. Re-processing...")
            
        print(f"\nProcessing board state {idx+1}/{len(board_states)}: {image_name} at {timestamp}s...")
        
        if not os.path.exists(image_path):
            print(f"Error: Image path {image_path} does not exist.")
            continue
            
        img = cv2.imread(image_path)
        if img is None:
            print(f"Error: Failed to read image {image_path}. Skipping.")
            continue
        h, w = img.shape[:2]
        
        # Step 1: Run PaddleOCR layout detector/reader
        print("Running text/line detection...")
        ocr_result = paddle_ocr.ocr(
            image_path,
            use_doc_orientation_classify=False,
            use_doc_unwarping=False
        )
        
        # Convert new PaddleX OCRResult objects to legacy list-of-lists format
        legacy_result = []
        if ocr_result:
            for page in ocr_result:
                if hasattr(page, "get") or isinstance(page, dict):
                    polys = page.get("rec_polys", [])
                    texts = page.get("rec_texts", [])
                    scores = page.get("rec_scores", [])
                    
                    page_lines = []
                    for poly, text, score in zip(polys, texts, scores):
                        if hasattr(poly, "tolist"):
                            poly = poly.tolist()
                        page_lines.append([poly, (text, score)])
                    legacy_result.append(page_lines)
                else:
                    legacy_result.append(page)
        ocr_result = legacy_result
        
        raw_items = []
        
        if ocr_result and ocr_result[0]:
            for line in ocr_result[0]:
                bbox = line[0]  # [[x1, y1], [x2, y2], [x3, y3], [x4, y4]]
                if hasattr(bbox, "tolist"):
                    bbox = bbox.tolist()
                text, conf = line[1]
                
                # Heuristic categorization
                # If text contains Cyrillic AND no math symbols, classify as text
                # If text has math symbols, or is short pure Latin/digits (likely a variable), classify as equation
                if is_cyrillic(text) and not has_math_symbols(text):
                    item_type = "text"
                    content = text
                else:
                    # Equation: either has math symbols, short Latin/digit token, or fallback
                    item_type = "equation"
                    rect = get_rect(bbox)
                    
                    # Add slight padding to the crop for better LaTeX OCR
                    pad_x = int((rect[2] - rect[0]) * 0.05)
                    pad_y = int((rect[3] - rect[1]) * 0.1)
                    
                    xmin = max(0, int(rect[0]) - pad_x)
                    ymin = max(0, int(rect[1]) - pad_y)
                    xmax = min(w, int(rect[2]) + pad_x)
                    ymax = min(h, int(rect[3]) + pad_y)
                    
                    crop = img[ymin:ymax, xmin:xmax]
                    
                    if crop.size > 0:
                        # Convert CV2 image to PIL Image
                        crop_pil = Image.fromarray(cv2.cvtColor(crop, cv2.COLOR_BGR2RGB))
                        try:
                            # Run pix2tex
                            content = latex_ocr(crop_pil)
                            print(f"  -> Equation OCR: {content}")
                        except Exception as e:
                            print(f"  -> pix2tex failed: {e}. Fallback to PaddleOCR result: {text}")
                            content = text
                    else:
                        content = text
                        
                raw_items.append({
                    "type": item_type,
                    "content": content,
                    "bbox": bbox
                })
                
        # Sort items in reading order
        current_items = sort_bounding_boxes(raw_items)
        
        # Step 2: Stage 5 - Board Evolution Tracking
        # Compare current_items with prev_items to find added and removed items
        added_items = []
        removed_items = []
        
        matched_prev_indices = set()
        matched_curr_indices = set()
        
        # 1. Match based on spatial overlap (IoU) and content
        for curr_idx, curr_item in enumerate(current_items):
            curr_rect = get_rect(curr_item["bbox"])
            
            best_match_idx = -1
            best_score = -1.0
            
            for prev_idx, prev_item in enumerate(prev_items):
                if prev_idx in matched_prev_indices:
                    continue
                    
                prev_rect = get_rect(prev_item["bbox"])
                iou = compute_iou(curr_rect, prev_rect)
                
                # Calculate text similarity using fuzzy matching
                text_sim = SequenceMatcher(None, curr_item["content"], prev_item["content"]).ratio()
                
                # Combine spatial and text similarity
                # A high IoU is a strong indicator of the same physical item
                # A matching content with moderate IoU is also a good indicator
                score = 0.7 * iou + 0.3 * text_sim
                
                if score > best_score:
                    best_score = score
                    best_match_idx = prev_idx
                    
            # Threshold to determine if it is indeed the same item
            if best_match_idx != -1 and best_score > 0.3:
                matched_prev_indices.add(best_match_idx)
                matched_curr_indices.add(curr_idx)
                
        # 2. Additions are current items that weren't matched
        for curr_idx, curr_item in enumerate(current_items):
            if curr_idx not in matched_curr_indices:
                added_items.append({
                    "type": curr_item["type"],
                    "content": curr_item["content"]
                })
                
        # 3. Removals are previous items that weren't matched
        for prev_idx, prev_item in enumerate(prev_items):
            if prev_idx not in matched_prev_indices:
                removed_items.append({
                    "type": prev_item["type"],
                    "content": prev_item["content"]
                })
                
        # Save output for this board state
        base_name, _ = os.path.splitext(image_name)
        state_output_path = os.path.join(output_dir, f"{base_name}.json")
        
        state_result = {
            "timestamp": timestamp,
            "image": image_name,
            "added": added_items,
            "removed": removed_items,
            "items": current_items
        }
        
        with open(state_output_path, "w", encoding="utf-8") as f:
            json.dump(state_result, f, ensure_ascii=False, indent=2)
            
        print(f"Saved OCR details to {state_output_path} (+{len(added_items)} added, -{len(removed_items)} removed)")
        
        # Propagate current state as previous for next iteration
        prev_items = current_items
        
        # Free VRAM/RAM caches after each board state to avoid leaks and OOM
        gc.collect()
        if torch.cuda.is_available():
            torch.cuda.empty_cache()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Stage 4 & 5: OCR and Whiteboard Evolution Tracking")
    parser.add_argument("--board-states", type=str, default="board_states.json", help="Path to board states JSON")
    parser.add_argument("--output-dir", type=str, default="ocr", help="Directory to save individual board state JSONs")
    parser.add_argument("--cpu", action="store_true", help="Force CPU usage for PaddleOCR")
    
    args = parser.parse_args()
    run_ocr_pipeline(args.board_states, args.output_dir, use_gpu=(not args.cpu))
