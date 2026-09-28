#!/usr/bin/env python3
"""
Generate slideshow frames showing the detection theory for top 3 images.
Perfect for GitHub README showcase!
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

import final_detection as fd
import functions as fn
import numpy as np
import cv2
import json
from pathlib import Path


def create_step_frames(img_path, img_num, output_dir, dice_score):
    """Create individual frames for each step of the detection process."""
    print(f"\n{'='*70}")
    print(f"Creating slideshow for: {img_path.name} (Dice: {dice_score:.1%})")
    print('='*70)

    img = cv2.imread(str(img_path))
    if img is None:
        return False

    original = img.copy()
    h, w = img.shape[:2]

    # Frame 1: Original Image
    frame1 = original.copy()
    cv2.putText(frame1, "Step 1: Original Hand-Drawn House", (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 2)
    cv2.putText(frame1, f"Dice Score: {dice_score:.1%}", (20, h - 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 200, 0), 2)
    cv2.imwrite(str(output_dir / f"frame1_original.jpg"), frame1)

    # Frame 2: Red Channel Extraction
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)[:, :, 2]
    frame2 = cv2.cvtColor(rgb, cv2.COLOR_GRAY2BGR)
    cv2.putText(frame2, "Step 2: Red Channel Extraction", (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 2)
    cv2.putText(frame2, "Houses drawn in red/dark colors stand out", (20, h - 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    cv2.imwrite(str(output_dir / f"frame2_red_channel.jpg"), frame2)

    # Frame 3: Sobel Edge Detection
    sobel = fn.sobel_image(rgb)
    frame3 = cv2.cvtColor(sobel, cv2.COLOR_GRAY2BGR)
    cv2.putText(frame3, "Step 3: Sobel Edge Detection", (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 2)
    cv2.putText(frame3, "Extract edges to find house outlines", (20, h - 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    cv2.imwrite(str(output_dir / f"frame3_sobel_edges.jpg"), frame3)

    # Frame 4: Connected Components
    cc_result = fn.connected_components(sobel)
    labels = cc_result['labels']
    stats = cc_result['stats']
    num_labels = cc_result['num_labels']

    label_hue = np.uint8(179 * labels / np.max(labels))
    blank_ch = 255 * np.ones_like(label_hue)
    labeled_img = cv2.merge([label_hue, blank_ch, blank_ch])
    labeled_img = cv2.cvtColor(labeled_img, cv2.COLOR_HSV2BGR)
    labeled_img[label_hue == 0] = 0

    frame4 = labeled_img.copy()
    cv2.putText(frame4, f"Step 4: Connected Components ({num_labels} regions)", (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2)
    cv2.putText(frame4, "Group edge pixels into regions", (20, h - 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    cv2.imwrite(str(output_dir / f"frame4_connected_components.jpg"), frame4)

    # Frame 5: Shape Classification
    frame5 = original.copy()

    shapes = []
    triangles = []
    rectangles = []
    pentagons = []

    for i in range(1, num_labels):
        x, y, w, h, area = stats[i]
        if area < 300 or w > 400 or h > 400:
            continue

        mask = np.where(labels == i, 255, 0).astype(np.uint8)
        mask = fn.dilation(mask, fn.kernel, 2)
        mask = fn.erosion(mask, fn.kernel, 2)

        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if not contours:
            continue

        contour = max(contours, key=cv2.contourArea)
        contour_area = cv2.contourArea(contour)
        if contour_area < 500:
            continue

        hull = cv2.convexHull(contour)
        x, y, w, h = cv2.boundingRect(hull)

        epsilon = 0.04 * cv2.arcLength(hull, True)
        approx = cv2.approxPolyDP(hull, epsilon, True)
        num_vertices = len(approx)

        if num_vertices == 5 and h >= 50:
            pentagons.append((approx, 'Pentagon'))
            cv2.drawContours(frame5, [approx], 0, (128, 0, 128), 3)

        if num_vertices > 4 and num_vertices <= 6:
            epsilon2 = 0.08 * cv2.arcLength(hull, True)
            approx2 = cv2.approxPolyDP(hull, epsilon2, True)
            if len(approx2) == 4:
                approx = approx2
                num_vertices = 4

        if num_vertices == 3:
            triangles.append(approx)
            cv2.drawContours(frame5, [approx], 0, (0, 0, 255), 2)
        elif num_vertices == 4:
            rectangles.append(approx)
            cv2.drawContours(frame5, [approx], 0, (255, 0, 0), 2)

    cv2.putText(frame5, "Step 5: Shape Classification", (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2)
    cv2.putText(frame5, f"{len(triangles)}T, {len(rectangles)}R, {len(pentagons)}P found", (20, h - 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    cv2.imwrite(str(output_dir / f"frame5_shapes.jpg"), frame5)

    # Frame 6: House Detection
    houses, labels, stats = fd.final_detect_houses(img, img_num - 1, debug=False)

    frame6 = original.copy()
    if houses:
        for house in houses:
            is_pentagon = getattr(house, '_is_pentagon', False)
            if is_pentagon:
                cv2.drawContours(frame6, [house.roof.approx], 0, (255, 0, 255), 4)
            else:
                cv2.drawContours(frame6, [house.roof.approx], 0, (0, 255, 0), 4)
                cv2.drawContours(frame6, [house.body.approx], 0, (0, 255, 0), 4)

        cv2.putText(frame6, f"Step 6: House Detection ({len(houses)} found)", (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2)
        cv2.putText(frame6, "Match triangles with rectangles", (20, h - 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    else:
        cv2.putText(frame6, "Step 6: House Detection (None found)", (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 2)

    cv2.imwrite(str(output_dir / f"frame6_detection.jpg"), frame6)

    # Frame 7: Final Result (Colored)
    frame7 = original.copy()
    if houses:
        # Create detection mask
        detection_mask = np.zeros(labels.shape, dtype=np.uint8)
        for house in houses:
            is_pentagon = getattr(house, '_is_pentagon', False)
            if is_pentagon:
                house_x = house.roof.x
                house_y = house.roof.y
                house_w = house.roof.w
                house_h = house.roof.h
            else:
                house_x = min(house.roof.x, house.body.x)
                house_y = house.roof.y
                house_w = max(house.roof.x + house.roof.w, house.body.x + house.body.w) - house_x
                house_h = (house.body.y + house.body.h) - house_y

            for i in range(1, labels.max() + 1):
                if i >= len(stats):
                    continue
                x, y, w, h, area = stats[i]
                if (x < house_x + house_w and x + w > house_x and
                    y < house_y + house_h and y + h > house_y):
                    detection_mask[labels == i] = 255

        # Paint with vibrant color
        color = (255, 100, 0)  # Electric orange
        overlay = frame7.copy()
        overlay[detection_mask > 0] = color
        frame7 = cv2.addWeighted(frame7, 0.6, overlay, 0.4, 0)

        # Darken edges
        sobel_edges = fn.sobel_image(rgb)
        edge_mask = sobel_edges > 0
        region_edges = np.logical_and(edge_mask, detection_mask > 0)
        frame7[region_edges] = frame7[region_edges] * 0.3

        cv2.putText(frame7, "Step 7: Final Colored Result", (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2)
        cv2.putText(frame7, f"SUCCESS! Dice Score: {dice_score:.1%}", (20, h - 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
    else:
        cv2.putText(frame7, "Step 7: No House Detected", (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 2)

    cv2.imwrite(str(output_dir / f"frame7_final.jpg"), frame7)

    # Frame 8: Home - Raw image with colored house using sobel edges from raw pixels
    frame8 = original.copy()
    if houses:
        # Use vibrant HSV-based colors like step 4 (fully saturated)
        import random
        # Generate vibrant colors using HSV (max saturation and value)
        hue_values = [0, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330]  # Different hues
        random_hue = random.choice(hue_values)
        # Create color in HSV then convert to BGR
        hsv_color = np.uint8([[[random_hue // 2, 255, 255]]])  # Hue/2 for OpenCV, max S and V
        frame8_color = cv2.cvtColor(hsv_color, cv2.COLOR_HSV2BGR)[0][0]
        frame8_color = tuple(int(x) for x in frame8_color)

        # Create detection mask
        detection_mask = np.zeros(labels.shape, dtype=np.uint8)
        for house in houses:
            is_pentagon = getattr(house, '_is_pentagon', False)
            if is_pentagon:
                house_x = house.roof.x
                house_y = house.roof.y
                house_w = house.roof.w
                house_h = house.roof.h
            else:
                house_x = min(house.roof.x, house.body.x)
                house_y = house.roof.y
                house_w = max(house.roof.x + house.roof.w, house.body.x + house.body.w) - house_x
                house_h = (house.body.y + house.body.h) - house_y

            for i in range(1, labels.max() + 1):
                if i >= len(stats):
                    continue
                x, y, w, h, area = stats[i]
                if (x < house_x + house_w and x + w > house_x and
                    y < house_y + house_h and y + h > house_y):
                    detection_mask[labels == i] = 255

        # Paint with vibrant color
        overlay = frame8.copy()
        overlay[detection_mask > 0] = frame8_color
        frame8 = cv2.addWeighted(frame8, 0.5, overlay, 0.5, 0)

        # Run sobel on the ORIGINAL grayscale pixels ONLY in the colored region
        gray_original = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
        # Apply sobel to original grayscale
        sobel_x = cv2.Sobel(gray_original, cv2.CV_64F, 1, 0, ksize=3)
        sobel_y = cv2.Sobel(gray_original, cv2.CV_64F, 0, 1, ksize=3)
        sobel_raw = np.sqrt(sobel_x**2 + sobel_y**2)
        sobel_raw = np.uint8(255 * sobel_raw / np.max(sobel_raw))

        # Only keep edges within the detection mask
        region_edges = np.logical_and(sobel_raw > 30, detection_mask > 0)

        # Darken the edges to create outline
        frame8[region_edges] = frame8[region_edges] * 0.2  # Very dark for clear outline

        cv2.putText(frame8, "Step 8: Home - Colored House with Edges", (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.0, frame8_color, 2)
        cv2.putText(frame8, f"Perfect Detection! Dice: {dice_score:.1%}", (20, h - 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, frame8_color, 2)
    else:
        cv2.putText(frame8, "Step 8: Home - No House Detected", (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 2)

    cv2.imwrite(str(output_dir / f"frame8_home.jpg"), frame8)

    print(f"✓ Created 8 frames for {img_path.name}")
    return True


if __name__ == "__main__":
    base_dir = Path(__file__).parent.parent
    raw_images_dir = base_dir / "images" / "raw_images"
    result_dir = base_dir / "images" / "result_images"
    slideshow_dir = base_dir / "images" / "slideshow"
    gt_dir = base_dir / "images" / "ground_truth"

    # Create slideshow directory
    slideshow_dir.mkdir(parents=True, exist_ok=True)

    print("="*70)
    print("GENERATING SLIDESHOW FOR TOP 3 DETECTIONS")
    print("="*70)

    # Load validation results to find top 3
    validation_file = result_dir / "VALIDATION_RESULTS.md"

    # Parse dice scores from colorful images
    colorful_dir = result_dir / "success_colorful"
    if not colorful_dir.exists():
        print("❌ No colorful images found. Run generate_validated_results.py first.")
        sys.exit(1)

    # Extract scores from filenames
    scores = []
    for colorful_file in colorful_dir.glob("image_*_colorful_*.jpg"):
        parts = colorful_file.stem.split('_')
        img_num = int(parts[1])
        # Extract dice score from filename (e.g., dice93%)
        dice_str = parts[-1].replace('dice', '').replace('iou', '').replace('%', '')
        dice_score = float(dice_str) / 100.0

        scores.append((img_num, dice_score, colorful_file))

    # Sort by dice score (highest first)
    scores.sort(key=lambda x: x[1], reverse=True)

    # Take top 3
    top_3 = scores[:3]

    if len(top_3) == 0:
        print("❌ No images with high enough scores.")
        sys.exit(1)

    print(f"\nTop 3 Images:")
    for rank, (img_num, dice, _) in enumerate(top_3, 1):
        print(f"  {rank}. Image {img_num}: Dice = {dice:.1%}")

    # Generate frames for each success
    for rank, (img_num, dice, _) in enumerate(top_3, 1):
        img_name = f"house_img{img_num}.jpg"
        img_path = raw_images_dir / img_name

        if not img_path.exists():
            print(f"⚠️  {img_path} not found")
            continue

        # Create subfolder for this image
        img_dir = slideshow_dir / f"top{rank}_image{img_num:02d}"
        img_dir.mkdir(exist_ok=True)

        create_step_frames(img_path, img_num, img_dir, dice)

    # Also generate TWO failure examples with highest Dice scores
    print(f"\n{'='*70}")
    print("GENERATING FAILURE EXAMPLES (Top 2 Highest Dice)")
    print('='*70)

    failed_dir = result_dir / "failed"
    if failed_dir.exists():
        # Look for both missed and low_dice failures
        failed_files = list(failed_dir.glob("image_*_missed_*.jpg")) + list(failed_dir.glob("image_*_low_dice*.jpg"))
        if failed_files:
            # Extract dice scores from filenames and sort by highest dice
            failed_with_scores = []
            for failed_file in failed_files:
                parts = failed_file.stem.split('_')
                img_num = int(parts[1])

                # Extract dice score from filename (e.g., "dice33%" or "dice0%")
                dice_str = parts[-1].replace('dice', '').replace('%', '')
                dice_score = float(dice_str) / 100.0

                failed_with_scores.append((img_num, dice_score, failed_file))

            # Sort by dice score (highest first) and take top 2
            failed_with_scores.sort(key=lambda x: x[1], reverse=True)
            top_2_failures = failed_with_scores[:2]

            print(f"\nTop 2 Failures (by Dice):")
            for rank, (img_num, dice, _) in enumerate(top_2_failures, 1):
                print(f"  {rank}. Image {img_num}: Dice = {dice:.1%}")

            # Generate frames for each failure
            for rank, (img_num, dice, _) in enumerate(top_2_failures, 1):
                img_name = f"house_img{img_num}.jpg"
                img_path = raw_images_dir / img_name

                if img_path.exists():
                    # Create subfolder for failure
                    img_dir = slideshow_dir / f"failure{rank}_image{img_num:02d}"
                    img_dir.mkdir(exist_ok=True)

                    create_step_frames(img_path, img_num, img_dir, dice)
                    print(f"✓ Created failure example {rank} for image {img_num}")
                else:
                    print(f"⚠️  Source image not found for failed detection")
        else:
            print("⚠️  No failed detections found")
    else:
        print("⚠️  Failed directory not found")

    print()
    print("="*70)
    print("SLIDESHOW COMPLETE")
    print("="*70)
    print(f"\nFrames saved to: {slideshow_dir}/")
    print("\nEach folder contains 8 frames:")
    print("  1. Original")
    print("  2. Red Channel")
    print("  3. Sobel Edges")
    print("  4. Connected Components")
    print("  5. Shape Classification")
    print("  6. House Detection")
    print("  7. Final Colored Result")
    print("  8. Home - Outlined & Colored House")
    print("\nIncludes:")
    print("  - Top 3 successful detections (highest Dice scores)")
    print("  - Top 2 failure examples (highest Dice among failures)")
    print("\nPerfect for GitHub README showcase!")
    print("="*70)
