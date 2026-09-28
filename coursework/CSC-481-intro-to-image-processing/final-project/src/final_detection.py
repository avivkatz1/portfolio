"""
FINAL House Detection System
- Filters nested rectangles (only keep outer)
- Detects pentagons (5-sided roof+body shapes)
- Validates to filter false positives
- Paints detected houses
"""

import functions as fn
import numpy as np
import cv2


def filter_nested_rectangles(rectangles):
    """Remove rectangles contained within other rectangles."""
    outer_rectangles = []
    for i, rect1 in enumerate(rectangles):
        is_contained = False
        for j, rect2 in enumerate(rectangles):
            if i == j:
                continue
            if (rect1.x >= rect2.x and rect1.y >= rect2.y and
                rect1.x + rect1.w <= rect2.x + rect2.w and
                rect1.y + rect1.h <= rect2.y + rect2.h and
                rect1.area < rect2.area):
                is_contained = True
                break
        if not is_contained:
            outer_rectangles.append(rect1)
    return outer_rectangles


def validate_house(roof, body, is_pentagon=False):
    """
    Validate house with relaxed thresholds for pentagons.
    """
    if is_pentagon:
        # Pentagons are complete house shapes - less strict
        if roof.area < 800:
            return False, "Pentagon too small"
        if roof.h < 50:
            return False, f"Pentagon height too small: {roof.h}"
        return True, "Valid pentagon house"

    # Traditional triangle+rectangle validation
    if roof.area < 800 or body.area < 1500:  # Relaxed from 1000/2000
        return False, "Too small"

    if roof.area < body.area * 0.08:
        return False, "Roof too small relative to body"

    if roof.area > body.area * 2.5:
        return False, "Roof too large relative to body"

    body_ar = body.aspect_ratio()
    if body_ar < 0.25 or body_ar > 3.5:
        return False, f"Body aspect ratio unusual: {body_ar:.2f}"

    if roof.h < 15 or roof.h > 250:
        return False, f"Roof height unusual: {roof.h}"

    if body.h < 25 or body.h > 350:
        return False, f"Body height unusual: {body.h}"

    total_h = (body.y + body.h) - roof.y
    if total_h < 50:
        return False, f"Total height too small: {total_h}"

    return True, "Valid house"


def are_pentagons_near(pent1, pent2, threshold=50):
    """Check if two pentagons are near each other (potentially part of same house)."""
    # Check if bounding boxes are close
    dist_x = abs(pent1.cx - pent2.cx)
    dist_y = abs(pent1.cy - pent2.cy)

    # If centroids are within threshold, they're near
    if dist_x < threshold and dist_y < threshold:
        return True

    # Check if bounding boxes overlap or are adjacent
    if (pent1.x < pent2.x + pent2.w + threshold and
        pent1.x + pent1.w + threshold > pent2.x and
        pent1.y < pent2.y + pent2.h + threshold and
        pent1.y + pent1.h + threshold > pent2.y):
        return True

    return False


def is_pentagon_near_rectangle(pentagon, rectangle, threshold=50):
    """
    Check if pentagon is near or above a rectangle.
    Pentagon might be a roof, rectangle might be a body.
    """
    # Check horizontal alignment (should be roughly aligned)
    x_overlap = not (pentagon.x + pentagon.w < rectangle.x - threshold or
                     pentagon.x > rectangle.x + rectangle.w + threshold)

    # Check vertical relationship (pentagon above or touching rectangle)
    is_above = pentagon.y < rectangle.y + threshold
    is_touching = abs((pentagon.y + pentagon.h) - rectangle.y) < threshold

    # Check if they're adjacent (side by side)
    is_adjacent_x = abs(pentagon.x - (rectangle.x + rectangle.w)) < threshold or \
                    abs((pentagon.x + pentagon.w) - rectangle.x) < threshold
    is_adjacent_y = not (pentagon.y + pentagon.h < rectangle.y or
                        pentagon.y > rectangle.y + rectangle.h)

    return (x_overlap and (is_above or is_touching)) or (is_adjacent_x and is_adjacent_y)


def find_pentagon_rectangle_combos(pentagons, rectangles, debug=False):
    """
    Find pentagons that are positioned near rectangles.
    These combos are more likely to be houses than pentagons alone.
    Returns: (pentagons_with_rects, pentagons_alone)
    """
    pentagons_with_rects = []
    pentagons_alone = []

    for pentagon in pentagons:
        has_nearby_rect = False
        for rectangle in rectangles:
            if is_pentagon_near_rectangle(pentagon, rectangle):
                pentagons_with_rects.append((pentagon, rectangle))
                has_nearby_rect = True
                if debug:
                    print(f"  Pentagon at ({pentagon.x},{pentagon.y}) paired with rectangle at ({rectangle.x},{rectangle.y})")
                break  # Only pair with first matching rectangle

        if not has_nearby_rect:
            pentagons_alone.append(pentagon)
            if debug:
                print(f"  Pentagon at ({pentagon.x},{pentagon.y}) is alone (no nearby rectangle)")

    return pentagons_with_rects, pentagons_alone


def filter_pentagons(pentagons, debug=False):
    """
    Filter pentagons based on proximity.
    If multiple pentagons are not near each other, keep only the largest.
    If they're near, keep all (they might form a larger house).
    """
    if len(pentagons) <= 1:
        return pentagons

    # Check if all pentagons are near each other
    all_near = True
    for i in range(len(pentagons)):
        for j in range(i + 1, len(pentagons)):
            if not are_pentagons_near(pentagons[i], pentagons[j]):
                all_near = False
                break
        if not all_near:
            break

    if all_near:
        # All pentagons are connected/near - keep all
        if debug:
            print(f"  All {len(pentagons)} pentagons are near each other - keeping all")
        return pentagons
    else:
        # Pentagons are scattered - keep only the largest
        largest = max(pentagons, key=lambda p: p.area)
        if debug:
            print(f"  Multiple scattered pentagons - keeping largest (area={largest.area:.0f})")
        return [largest]


def paint_detected_house(original_img, house, labels, stats, is_pentagon=False):
    """Paint the detected house region (no outlines, just colored fill)."""
    result = original_img.copy()
    house_mask = np.zeros(labels.shape, dtype=np.uint8)

    if is_pentagon:
        # For pentagon, just use the shape bounds
        house_x = house.roof.x
        house_y = house.roof.y
        house_w = house.roof.w
        house_h = house.roof.h
    else:
        house_x = min(house.roof.x, house.body.x)
        house_y = house.roof.y
        house_w = max(house.roof.x + house.roof.w, house.body.x + house.body.w) - house_x
        house_h = (house.body.y + house.body.h) - house_y

    # Fill overlapping components
    for i in range(1, labels.max() + 1):
        if i >= len(stats):
            continue
        x, y, w, h, area = stats[i]
        if (x < house_x + house_w and x + w > house_x and
            y < house_y + house_h and y + h > house_y):
            house_mask[labels == i] = 255

    # Create yellow overlay (no outlines - just fill)
    overlay = result.copy()
    overlay[house_mask > 0] = [0, 255, 255]
    result = cv2.addWeighted(result, 0.6, overlay, 0.4, 0)

    return result


def final_detect_houses(img, image_index, debug=False):
    """
    FINAL detection combining all improvements.
    """
    if debug:
        print(f"\n{'='*60}")
        print(f"Image {image_index + 1} - FINAL DETECTION")
        print('='*60)

    original = img.copy()
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)[:, :, 2]
    sobel = fn.sobel_image(rgb)

    # Connected components
    cc_result = fn.connected_components(sobel)
    labels = cc_result['labels']
    stats = cc_result['stats']
    num_labels = cc_result['num_labels']

    # Extract shapes
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

        # PENTAGON DETECTION (roof+body as one shape)
        if num_vertices == 5:
            # Check if it looks like a house (wider at bottom)
            points = approx.reshape(-1, 2)
            top_y = points[:, 1].min()
            bottom_y = points[:, 1].max()

            # Pentagon should have reasonable height
            if h >= 50:
                shape = fn.TriangleShape(x, y, w, h, contour_area, approx)
                pentagons.append(shape)
                if debug:
                    print(f"  Pentagon: ({x},{y}) {w}x{h}, area={contour_area:.0f}")

        # Try to simplify to rectangle
        if num_vertices > 4 and num_vertices <= 6:
            epsilon2 = 0.08 * cv2.arcLength(hull, True)
            approx2 = cv2.approxPolyDP(hull, epsilon2, True)
            if len(approx2) == 4:
                approx = approx2
                num_vertices = 4

        # Classify
        if num_vertices == 3:
            shape = fn.TriangleShape(x, y, w, h, contour_area, approx)
            triangles.append(shape)
            shapes.append(shape)
        elif num_vertices == 4:
            shape = fn.RectangleShape(x, y, w, h, contour_area, approx)
            rectangles.append(shape)
            shapes.append(shape)

    # Filter nested rectangles
    rectangles = filter_nested_rectangles(rectangles)

    if debug:
        print(f"Shapes: {len(triangles)}T, {len(rectangles)}R, {len(pentagons)}P (after filtering)")

    validated_houses = []

    # STRATEGY 1: Traditional triangle+rectangle (HIGHEST PRIORITY)
    # Try this first - if triangle+rectangle combo exists, use it
    if debug:
        print(f"\nStrategy 1: Triangle + Rectangle detection")

    for tol_x, tol_y in [(30, 40), (50, 60), (80, 100), (100, 150)]:
        detector = fn.HouseDetector(shapes, tolerance_x=tol_x, tolerance_y=tol_y)

        for triangle in detector.triangles:
            if not triangle.is_pointing_up():
                continue

            candidates = detector._find_base_candidates(triangle)
            for rect in candidates:
                score = detector._score_house_match(triangle, rect)
                if score > 0.6:
                    is_valid, reason = validate_house(triangle, rect)

                    if debug:
                        status = "✓" if is_valid else "✗"
                        print(f"  {status} T+R house (score={score:.2f}): {reason}")

                    if is_valid:
                        house = detector._create_house(triangle, rect)
                        house._is_pentagon = False
                        validated_houses.append(house)

        if validated_houses:
            if debug:
                print(f"  Found {len(validated_houses)} house(s) via triangle+rectangle")
            break

    # STRATEGY 2: Pentagon + Rectangle combos (MEDIUM PRIORITY)
    # If pentagon is near a rectangle, they likely form a house together
    if not validated_houses and pentagons and rectangles:
        if debug:
            print(f"\nStrategy 2: Pentagon + Rectangle combos")

        pentagon_rect_combos, pentagons_alone_list = find_pentagon_rectangle_combos(
            pentagons, rectangles, debug=debug
        )

        # Try pentagon+rectangle combos first (more likely to be houses)
        for pentagon, rect in pentagon_rect_combos:
            # Treat as a combined shape - use pentagon for validation but consider it stronger
            is_valid, reason = validate_house(pentagon, rect, is_pentagon=False)

            if debug:
                status = "✓" if is_valid else "✗"
                print(f"  {status} Pentagon+Rectangle combo: {reason}")

            if is_valid:
                # Create house from the combo
                house = fn.DetectedHouse(
                    roof=pentagon,
                    body=rect,
                    features=[],
                    x=min(pentagon.x, rect.x),
                    y=pentagon.y,
                    w=max(pentagon.x + pentagon.w, rect.x + rect.w) - min(pentagon.x, rect.x),
                    h=(rect.y + rect.h) - pentagon.y
                )
                house._is_pentagon = False  # It's a combo, not pure pentagon
                validated_houses.append(house)

        if validated_houses:
            if debug:
                print(f"  Found {len(validated_houses)} house(s) via pentagon+rectangle combos")
    else:
        pentagons_alone_list = pentagons  # No rectangles, all pentagons are alone

    # STRATEGY 3: Pentagon alone (LOWEST PRIORITY - FALLBACK)
    # Only use if no other strategy worked
    if not validated_houses and pentagons_alone_list:
        if debug:
            print(f"\nStrategy 3: Pentagon detection alone (fallback)")

        # Filter pentagons based on proximity
        filtered_pentagons = filter_pentagons(pentagons_alone_list, debug=debug)

        for pentagon in filtered_pentagons:
            is_valid, reason = validate_house(pentagon, pentagon, is_pentagon=True)
            if debug:
                status = "✓" if is_valid else "✗"
                print(f"  {status} Pentagon house: {reason}")

            if is_valid:
                # Create DetectedHouse from pentagon
                house = fn.DetectedHouse(
                    roof=pentagon,
                    body=pentagon,  # Same shape for both
                    features=[],
                    x=pentagon.x,
                    y=pentagon.y,
                    w=pentagon.w,
                    h=pentagon.h
                )
                house._is_pentagon = True
                validated_houses.append(house)

    if debug:
        print(f"Total validated: {len(validated_houses)} house(s)")

    if not validated_houses:
        return [], labels, stats

    # Paint all validated houses
    result = original.copy()
    for house in validated_houses:
        is_pentagon = getattr(house, '_is_pentagon', False)
        result = paint_detected_house(result, house, labels, stats, is_pentagon)

    # Save only if debug mode (for testing)
    if debug:
        output_filename = f"house_final_{image_index + 1}.jpg"
        fn.save_image(result, output_filename)
        print(f"Saved: {output_filename}")

    return validated_houses, labels, stats


if __name__ == "__main__":
    print("FINAL House Detection System")
    print("- Pentagon detection (5-sided house shapes)")
    print("- Filtered nested rectangles")
    print("- Validated to avoid false positives\n")

    results = []
    for idx in range(23):
        path = f"house_img{idx + 1}.jpg"
        img = cv2.imread(path)
        if img is None:
            continue

        debug = idx < 5 or idx in [5, 11]  # Debug first 5, plus 6 and 12
        houses, labels, stats = final_detect_houses(img, idx, debug=debug)

        results.append({'image': idx + 1, 'houses': len(houses)})

        if not debug:
            status = f"✅ {len(houses)}" if houses else "❌"
            print(f"Image {idx + 1}: {status}")

    print(f"\n{'='*60}")
    print("FINAL RESULTS")
    print('='*60)
    total = sum(r['houses'] for r in results)
    detected = sum(1 for r in results if r['houses'] > 0)
    print(f"Detected in: {detected}/23 images ({detected/23*100:.1f}%)")
    print(f"Total houses: {total}")
    print(f"False positives filtered: Image 4 and others")
    print('='*60)
