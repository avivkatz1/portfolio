import matplotlib.pyplot as plt
import math
import numpy as np
from scipy.ndimage import gaussian_filter
from scipy.signal import convolve2d
import cv2
import os
from scipy import ndimage 




class House_Finding:
    def method_RETR_EXTERNAL(self, img):
        return cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    def method_RETR_CCOMP(self, img):
        return cv2.findContours(img,cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    def method_RETR_TREE(self, img):
        return cv2.findContours(img,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    def method_RETR_LIST(self, img):
        return cv2.findContours(img,cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        
  
def get_all_contours_simple(img):
    contours_1, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours_2, _ = cv2.findContours(img, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    contours_3, _ = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours_4, _ = cv2.findContours(img, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contours_5, _ = cv2.findContours(img, cv2.RETR_FLOODFILL, cv2.CHAIN_APPROX_SIMPLE)
    return contours_1, contours_2, contours_3, contours_4, contours_5

def test_each_contour(contours_item,img, index_num):
    for i_eps in range(7):
        img_copy = img.copy()
        epsilon = 0.1*i_eps*cv2.arcLength(contours_item, True)
        for contour in contours_item:
            approx = cv2.approxPolyDP(contour, epsilon, True)
            # cv2.drawContours(img_copy, [approx], 0, (0, 0, 255), 5)
            # cv2.imshow("Approximation_{} for num {}".format(i_eps, index_num), img_copy)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()
            return img_copy
    hull = cv2.convexHull(contour)
    # cv2.drawContours(img_copy, [hull], 0, (0, 0, 255), 5)
    # cv2.imshow("Hull_ {}".format(index_num), img_copy)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    
        



def read_images_to_array(file_paths):
    images = []
    for file_path in file_paths:
        img = cv2.imread(file_path)
        if img is not None:
            images.append(img)
        else:
            raise FileNotFoundError(f"File {file_path} not found or could not be read.")
    return np.array(images)

# Example usage:
# file_paths = ['image1.jpg', 'image2.jpg', 'image3.jpg']
# images_array = read_images_to_array(file_paths)

def save_image(image, image_name):
    file_path = os.path.join(os.getcwd(), image_name)
    cv2.imwrite(file_path, image)

# Example usage:
# image = cv2.imread('image1.jpg')
# save_image(image, 'saved_image.jpg')
def show_this(img, title='Image', show_it = False):
    if(show_it):
        cv2.imshow(title, img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    return img

def getting_x_y_of_house(potential_roofs, potential_houses,  var_difference_y = 20,var_difference_x = 20):


    


    houses_found = []
    for roof_pot in potential_roofs:
        for house_pot in potential_houses:
            if(abs(roof_pot.x - house_pot.x) < var_difference_x and abs(roof_pot.y + roof_pot.h - house_pot.y )< var_difference_y ):
                houses_found.append([house_pot.x, roof_pot.y])
    return houses_found

def connected_components(img):
    """Returns labels and stats for downstream processing.

    Args:
        img: Binary input image

    Returns:
        Dictionary containing:
            - num_labels: Number of connected components
            - labels: Label map (same size as input)
            - stats: Stats array (x, y, w, h, area for each component)
            - centroids: Centroid coordinates for each component
    """
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(img, 8, cv2.CV_32S)

    # Remove background (largest component)
    max_label = 0
    max_label_count = 0
    for ind in range(num_labels):
        count = np.count_nonzero(labels == ind)
        if count > max_label_count:
            max_label = ind
            max_label_count = count
    labels = np.where(labels == max_label, 0, labels)

    return {
        'num_labels': num_labels,
        'labels': labels,
        'stats': stats,
        'centroids': centroids
    }

def get_colored_components_visualization(labels, num_labels):
    """Optional visualization of connected components.

    Args:
        labels: Label map from connected_components()
        num_labels: Number of labels

    Returns:
        Colored visualization image
    """
    colors = np.random.randint(0, 255, size=(num_labels, 3), dtype="uint8")
    colors[0] = [0, 0, 0]
    return colors[labels]


def display_images_with_titles(img_array, title_array=[]):
    img_total = len(img_array)
   
    fig, axes = plt.subplots(math.ceil(img_total/2), 2,figsize=(10,10))
    axes = axes.flatten()
    index = 0
    for a in axes:
        if(len(title_array)>0):
            if(index<len(title_array)):
                a.set_title(title_array[index])
        a.imshow(img_array[index] if index < img_total else img_array[0], cmap='gray')
        a.axis("off")
        index = index + 1
    plt.subplots_adjust(wspace=0, hspace = 0.1)
    plt.show()

    array = np.arange(40, 40 + 5 * 40, 5)
array = np.arange(20, 20 + 10 * 15, 10) 

# Example usage:
# images = [cv2.imread('image1.jpg'), cv2.imread('image2.jpg'), cv2.imread('image3.jpg')]
# titles = ['Title 1', 'Title 2', 'Title 3']
# display_images_with_titles(images, titles)

def split_rgb_channels(image):
    r, g, b = cv2.split(image)
    return [r,g,b]

def opening(img, kernel, iters = 2):
    erosion = cv2.erode(img,kernel,iterations = iters)
    dilation = cv2.dilate(erosion,kernel,iterations = iters)
    return dilation

def closing(img, kernel, iters = 2):
    dilation = cv2.dilate(img,kernel,iterations = iters)
    erosion = cv2.erode(dilation,kernel,iterations = iters)
    return erosion

def erosion(img,kernel,iters = 2):
    return cv2.erode(img,kernel,iterations = iters)

def dilation(img,kernel,iters = 2):
    return cv2.dilate(img,kernel,iterations = iters)

kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))

def merge_rgb_channels(r, g, b):
    return cv2.merge((r, g, b))

def preprocess_image_for_edge_detection(image, gray = False):
        # Convert to grayscale
    if gray:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Apply Gaussian blur to reduce noise and improve edge detection
    blurred_img = gaussian_filter(image, sigma=5)
        
    return blurred_img

def sobel_image(img):
    sobelx = cv2.Sobel(img,cv2.CV_64F,1,0,ksize=5)
    sobelx = cv2.convertScaleAbs(sobelx)
    
    sobely = cv2.Sobel(img,cv2.CV_64F,0,1,ksize=5)
    sobely = cv2.convertScaleAbs(sobely)

    sobel = cv2.addWeighted(sobelx, 0.5, sobely, 0.5, 0)
  
    sobel = cv2.threshold(sobel, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
    sobel = closing(sobel, kernel, 1)
    
    sobel = cv2.bitwise_not(sobel)

    return sobel

def sobel_edge_detection(image, x=1, y=1):
    sobel_x = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]) * x
    sobel_y = np.array([[1, 2, 1], [0, 0, 0], [-1, -2, -1]]) * y
    horizontal = convolve2d(image, sobel_x, mode='same', boundary='symm')
    vertical = convolve2d(image, sobel_y, mode='same', boundary='symm')
    
    return np.sqrt(np.square(horizontal) + np.square(vertical))

roberts_cross_v = np.array( [[1, 0 ], 
                             [0,-1 ]] ) 

roberts_cross_h = np.array( [[ 0, 1 ], 
                             [ -1, 0 ]] )

def edge_detection(image):
    image = preprocess_image_for_edge_detection(image)
    vertical = ndimage.convolve( image, roberts_cross_v )
    horizontal = ndimage.convolve( image, roberts_cross_h )
    edged_img = np.sqrt( np.square(horizontal) + np.square(vertical))
    return edged_img

class Roof:
    def __init__(self, x, y, w, h, area, approx):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.area = area
        self.approx = approx

class House:
    def __init__(self, x, y, w, h, area, approx):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.area = area
        self.approx = approx

class Window:
    def __init__(self, x, y, w, h, area, approx):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.area = area
        self.approx = approx

class Mask:
    def __init__(self, mask, x, y, w, h, area, approx, coords):
        self.mask = mask
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.area = area
        self.coords = coords
        self.approx = approx


# New shape classes for refactored architecture
class Shape:
    """Base class for detected shapes."""
    def __init__(self, x, y, w, h, area, approx):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.area = area
        self.approx = approx
        self.cx = x + w // 2
        self.cy = y + h // 2


class TriangleShape(Shape):
    """Triangle shape (potential roof)."""
    def is_pointing_up(self):
        """Check if triangle apex is at top."""
        if self.approx is None or len(self.approx) < 3:
            return False
        points = self.approx.reshape(-1, 2)
        top_point = points[points[:, 1].argmin()]
        return top_point[1] < self.cy


class RectangleShape(Shape):
    """Rectangle shape (potential house body, window, or door)."""
    def aspect_ratio(self):
        return self.w / self.h if self.h > 0 else 0

    def is_vertical(self):
        return self.aspect_ratio() < 0.7

    def is_horizontal(self):
        return self.aspect_ratio() > 1.3

    def is_square(self):
        return 0.7 <= self.aspect_ratio() <= 1.3


class ComplexShape(Shape):
    """Shape with more than 4 vertices."""
    pass


class ShapeClassifier:
    """Classify shapes from connected component masks."""
    def __init__(self, mask, stats, epsilon_factor=0.04):
        self.mask = mask
        self.x, self.y, self.w, self.h, self.area = stats
        self.contours, _ = cv2.findContours(
            mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )
        self.epsilon_factor = epsilon_factor

    def classify(self):
        """Classify shape as triangle, rectangle, or complex.

        Returns:
            Shape object (TriangleShape, RectangleShape, or ComplexShape) or None
        """
        if not self.contours:
            return None

        contour = max(self.contours, key=cv2.contourArea)
        epsilon = self.epsilon_factor * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)

        num_vertices = len(approx)

        if num_vertices == 3:
            return TriangleShape(self.x, self.y, self.w, self.h, self.area, approx)
        elif num_vertices == 4:
            return RectangleShape(self.x, self.y, self.w, self.h, self.area, approx)
        else:
            return ComplexShape(self.x, self.y, self.w, self.h, self.area, approx)

def find_contained_shapes(shapes, padding=5):
    """Find shapes that are contained within other shapes.

    Args:
        shapes: List of Shape objects
        padding: Tolerance in pixels for containment check

    Returns:
        Dictionary mapping outer RectangleShapes to their contained shapes
    """
    containment_map = {}

    for i, outer in enumerate(shapes):
        if not isinstance(outer, RectangleShape):
            continue

        contained = []
        for j, inner in enumerate(shapes):
            if i == j:
                continue

            # Check if inner is inside outer
            if (inner.x >= outer.x - padding and
                inner.y >= outer.y - padding and
                inner.x + inner.w <= outer.x + outer.w + padding and
                inner.y + inner.h <= outer.y + outer.h + padding):
                contained.append(inner)

        if contained:
            containment_map[outer] = contained

    return containment_map


class DetectedHouse:
    """Represents a detected house with roof, body, and features."""
    def __init__(self, roof, body, features, x, y, w, h):
        self.roof = roof
        self.body = body
        self.features = features  # Doors/windows
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def get_mask(self, img_shape):
        """Create combined mask for entire house."""
        mask = np.zeros(img_shape[:2], dtype=np.uint8)

        # Add roof region
        if self.roof.approx is not None:
            cv2.fillPoly(mask, [self.roof.approx], 255)

        # Add body region
        if self.body.approx is not None:
            cv2.fillPoly(mask, [self.body.approx], 255)

        return mask

    def draw_on_image(self, img, color=(0, 255, 0), thickness=3):
        """Draw house outline on image."""
        result = img.copy()

        # Draw roof in red
        if self.roof.approx is not None:
            cv2.drawContours(result, [self.roof.approx], 0, (0, 0, 255), thickness)

        # Draw body in green
        if self.body.approx is not None:
            cv2.drawContours(result, [self.body.approx], 0, color, thickness)

        # Draw features in blue
        for feature in self.features:
            if feature.approx is not None:
                cv2.drawContours(result, [feature.approx], 0, (255, 0, 0), thickness - 1)

        return result


class HouseDetector:
    """Detect houses using triangle-over-rectangle pattern matching."""
    def __init__(self, shapes, tolerance_x=30, tolerance_y=40):
        self.shapes = shapes
        self.tolerance_x = tolerance_x
        self.tolerance_y = tolerance_y

        # Separate shapes by type
        self.triangles = [s for s in shapes if isinstance(s, TriangleShape)]
        self.rectangles = [s for s in shapes if isinstance(s, RectangleShape)]

    def find_houses(self):
        """Find houses using triangle-over-rectangle pattern.

        Returns:
            List of DetectedHouse objects
        """
        houses = []

        for triangle in self.triangles:
            if not triangle.is_pointing_up():
                continue

            # Find rectangles below this triangle
            candidates = self._find_base_candidates(triangle)

            for rect in candidates:
                score = self._score_house_match(triangle, rect)
                if score > 0.6:  # Threshold for valid house
                    house = self._create_house(triangle, rect)
                    houses.append(house)

        return houses

    def _find_base_candidates(self, triangle):
        """Find rectangles that could be house body."""
        candidates = []

        for rect in self.rectangles:
            # Check horizontal alignment
            x_diff = abs(triangle.cx - rect.cx)
            if x_diff > self.tolerance_x:
                continue

            # Check vertical position (roof above body)
            y_diff = rect.y - (triangle.y + triangle.h)
            if y_diff < -self.tolerance_y or y_diff > self.tolerance_y:
                continue

            # Roof should be narrower or similar width to body
            if triangle.w > rect.w * 1.5:
                continue

            candidates.append(rect)

        return candidates

    def _score_house_match(self, roof, body):
        """Score how well roof and body match house pattern."""
        score = 0.0

        # Alignment score (0-0.3)
        x_alignment = 1 - min(abs(roof.cx - body.cx) / self.tolerance_x, 1)
        score += x_alignment * 0.3

        # Vertical position score (0-0.3)
        y_gap = abs(body.y - (roof.y + roof.h))
        y_score = 1 - min(y_gap / self.tolerance_y, 1)
        score += y_score * 0.3

        # Size proportion score (0-0.2)
        width_ratio = roof.w / body.w if body.w > 0 else 0
        if 0.5 <= width_ratio <= 1.2:
            score += 0.2

        # Aspect ratio score (0-0.2)
        if body.is_vertical() or body.is_square():
            score += 0.2

        return score

    def _create_house(self, roof, body):
        """Create detected house object."""
        # Find windows/doors within body
        contained = find_contained_shapes([body] + self.rectangles)
        features = contained.get(body, [])

        return DetectedHouse(
            roof=roof,
            body=body,
            features=features,
            x=body.x,
            y=roof.y,
            w=body.w,
            h=(body.y + body.h) - roof.y
        )


def skeletonize(img):
    skeleton = np.zeros(img.shape, np.uint8)
    while False:
        eroded = cv2.erode(img, kernel)
        temp = cv2.dilate(eroded, kernel)
        temp = cv2.subtract(img, temp)
        skeleton = cv2.bitwise_or(skeleton, temp)
        img = eroded.copy()
        if cv2.countNonZero(img) == 0:
            break
    return skeleton


def get_groups(img, col_img): 
    new_image = img.copy()
    new_image = skeletonize(~new_image)
    # cv2.imshow("get_group_shape", new_image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    gray_img = cv2.cvtColor(col_img, cv2.COLOR_BGR2GRAY)
    # cv2.imshow("gray group shape", gray_img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    _, col_img = cv2.threshold(gray_img, 20, 255, type=cv2.THRESH_BINARY)
    new_image = cv2.add(col_img, ~img)
    new_image_2 = erosion(new_image, kernel, 4)
    new_image_2 = dilation(new_image_2, kernel, 4)
    # cv2.imshow("group shape finished", new_image)
    # cv2.imshow("group shape finished 2", new_image_2)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    return new_image_2


def prepare_for_shape_detection(edge_img, colored_components_img):
    """Prepare edge image for shape detection with additional processing.

    This combines edges with colored component visualization to create
    better separated regions for shape detection.

    Args:
        edge_img: Binary edge image
        colored_components_img: Colored visualization from connected components

    Returns:
        Processed binary image ready for shape detection
    """
    new_image = edge_img.copy()
    new_image = skeletonize(~new_image)

    # Convert colored image to grayscale and threshold
    gray_img = cv2.cvtColor(colored_components_img, cv2.COLOR_BGR2GRAY)
    _, col_img_thresh = cv2.threshold(gray_img, 20, 255, type=cv2.THRESH_BINARY)

    # Combine
    new_image = cv2.add(col_img_thresh, ~edge_img)

    # Apply morphological operations to clean up
    new_image_2 = erosion(new_image, kernel, 4)
    new_image_2 = dilation(new_image_2, kernel, 4)
    new_image_2 = erosion(new_image_2, kernel, 4)
    new_image_2 = dilation(new_image_2, kernel, 4)

    return new_image_2


def get_group_shapes(labels, stats, centroids):
    """Extract shape masks directly from labels.

    Args:
        labels: Label map from connected_components()
        stats: Stats array from connected_components()
        centroids: Centroids array from connected_components()

    Returns:
        List of Mask objects for each component
    """
    array_of_masks = []
    num_labels = labels.max() + 1

    for i in range(1, num_labels):  # Skip background (0)
        if i not in labels:
            continue

        x, y, w, h, area = stats[i]
        cx, cy = centroids[i]

        # Create mask for this component
        mask = np.where(labels == i, 255, 0).astype(np.uint8)
        show_this(mask, "Mask INSIDE GROUP SHAPES", False)

        mask_found = Mask(mask, x, y, w, h, area, None, [cx, cy])
        array_of_masks.append(mask_found)

    return array_of_masks



# cycles through a list of function names, it one by one and returns all the masks

# a function that takes in an array of masks and returns one image with all the masks and each mask has 10% alpha of a yellow color
def combine_masks(masks):
    combined_mask = np.zeros_like(masks[0])
    for mask in masks:
        mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
        mask = cv2.addWeighted(mask, 0.1, np.zeros_like(mask), 0.9, 0)
        combined_mask = cv2.add(combined_mask, mask)
    return combined_mask



def highlight_house(masked_array, coord_of_houses,original,i, rule_used=""):
    
    num_houses = 0
    diff_x = 20
    diff_y = 40
    while num_houses == 0:
            image_to_show = original.copy()
            for home_mask in masked_array:
                    for house in coord_of_houses:
                        print("house {}".format(i))
                        print("actual_diff: {} diff_x: {}".format(abs(home_mask.x - house[0]), diff_x))
                        print("actual_diff: {} diff_y: {}".format(abs(home_mask.y - house[1]),diff_y))
                        if abs(home_mask.x - house[0]) < diff_x and abs(home_mask.y - house[1]) < diff_y:
                            print("found a match")
                            num_houses = num_houses + 1
                            highlight = show_this(home_mask.mask, "home_mask", False)
                            image_to_show = show_this(cv2.bitwise_and(original, original, mask = highlight),"house in image {}".format(i), True)
                            save_image(image_to_show, "house_in_image_{}{}.jpg".format(i+1, rule_used))
                            break
            diff_x = diff_x + 5
            diff_y = diff_y + 20
    return image_to_show



def connected_component_with_stats_finding_shapes(num_labels, labels, stats, centroids, rule, image, trial_num = 0):
    array_mask = []
    array_roof_potentials=[]
    array_house_potentials=[]
    array_window_potentials=[]
    img = image.copy()
    for i in range(num_labels):
        x, y, w, h, area = stats[i]
        cx, cy = centroids[i]
        if(i==0):
            continue
        if area<300:
            continue
        if w>400:
            continue
        if h>400:
            continue
        mask = np.where(labels ==i, 255, 0).astype(np.uint8)
        
        mask = dilation(mask, kernel,rule[0])
        mask = erosion(mask,kernel, rule[0])
         
        
        if rule[1] == "RETR_EXTERNAL":
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            for contour in contours:
                # make an all black image the size of the mask image
                approx = cv2.approxPolyDP(contour, 0.05 * cv2.arcLength(contour, True), True)
                if(len(approx)==3):
                    # roof = Roof(x,y,w,h,area, [approx])
                    roof = [x,y,w,h,area, approx]
                    roof_obj = Roof(x, y, w, h, area, approx)
                    array_roof_potentials.append(roof_obj)
                    cv2.drawContours(img, [approx], 0, (0, 0, 255), 5)
                elif(len(approx)==4):
                    window_obj = Window(x, y, w, h, area, approx)
                    house_obj = House(x, y, w, h, area, approx)
                    
                    cv2.drawContours(img, [approx], 0, (0, 255, 0), 5)
                    
                    array_window_potentials.append(window_obj)
                    array_house_potentials.append(house_obj)
                    # window = Window(x,y,w,h,area, [approx])
                else:
                    cv2.drawContours(img, [approx], 0, (255, 0, 0), 5)
                    # house = House(x,y,w,h,area, [approx])
                    house = [x,y,w,h,area, approx]
                    house_obj = House(x, y, w, h, area, approx)
                    array_house_potentials.append(house_obj)
                array_mask.append(mask)
                show_this(img, "Mask with trace", False)
                
                
                

        
        if rule[1] == "HULL":
            
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            for contour in contours:
                hull = cv2.convexHull(contour)
                # cv2.drawContours(img, [hull], 0, (0, 0, 255), 5)
                approx = cv2.approxPolyDP(hull, 0.05 * cv2.arcLength(hull, True), True)
                if(len(approx)==3):
                    # roof = Roof(x,y,w,h,area, [approx])
                    roof = [x,y,w,h,area, approx]
                    roof_obj = Roof(x, y, w, h, area, approx)
                    array_roof_potentials.append(roof_obj)
                    cv2.drawContours(img, [approx], 0, (0, 0, 255), 5) 
                elif(len(approx)==4):
                    window_obj = Window(x, y, w, h, area, approx)
                    house_obj = House(x, y, w, h, area, approx)
                    
                    cv2.drawContours(img, [approx], 0, (0, 255, 0), 5)
                    
                    array_window_potentials.append(window_obj)
                    array_house_potentials.append(house_obj)
                else:
                    cv2.drawContours(img, [approx], 0, (255, 0, 0), 5)
                    # house = House(x,y,w,h,area, [approx])
                    house = [x,y,w,h,area, approx]
                    house_obj = House(x, y, w, h, area, approx)
                    array_house_potentials.append(house_obj)
                array_mask.append(mask)
                show_this(img, "Mask with trace second time", False)
        
           
    return array_mask, array_roof_potentials, array_house_potentials
        

def check_if_house_has_roof(house, roof, theshold = 20):
    if house[0] - roof[0] < theshold and roof[1] + roof[2] - house[1] < theshold:
        return True
    return False



def edge_detection_sobel(image):
    image = preprocess_image_for_edge_detection(image)
    vertical = sobel_edge_detection(image, x=1, y=0)
    horizontal = sobel_edge_detection(image, x=0, y=1)
    edged_img = np.sqrt( np.square(horizontal) + np.square(vertical))
    edged_img*=255
    return edged_img

def edge_detection_canny(image, thresh1=0.1, thresh2=0.9, apertureSize=3):
    image = preprocess_image_for_edge_detection(image)
    image = (image * 255).astype(np.uint8)
    return cv2.Canny(image, thresh1,thresh2,apertureSize)
  
def rgb2gray(rgb):
    if(rgb[0][0].size<3):
        return rgb
    else: 
        return_arr = np.dot(rgb, [0.2989, 0.5870, 0.1140])
        return_arr = return_arr/255.0
        return return_arr

# Example usage:
# image = cv2.imread('image1.jpg')
# gray_image = convert_to_grayscale(image)
# save_image(gray_image, 'gray_image.jpg')




# Load the image
def rgb_to_hsi(image):
    # Convert the image to float32 for precision
    image_copy = image.copy()
    
    image_copy = image_copy.astype(np.float32) / 255.0
    
    # Split the image into R, G, B channels
    R, G, B = cv2.split(image_copy)
    
    # Calculate intensity
    I = (R + G + B) / 3.0
    
    # Calculate saturation
    min_RGB = np.minimum(np.minimum(R, G), B)
    S = 1 - (3 / (R + G + B ) * min_RGB)
    
    # Calculate hue
    num = 0.5 * ((R - G) + (R - B))
    den = np.sqrt((R - G) ** 2 + (R - B) * (G - B))
    theta = np.arccos(num / (den + 1e-6))
    
    H = np.where(B <= G, theta, 2 * np.pi - theta)
    H = H / (2 * np.pi)
    
    # Merge H, S, I channels back into an image
    hsi_image = cv2.merge([H, S, I])
    
    return hsi_image

def composite_images(images, weights=None):
    if weights is None:
        weights = [1] * len(images)
        
        # Ensure the weights array is the same length as the images array
    if len(weights) != len(images):
        raise ValueError("The length of weights must match the length of images")
        
        # Initialize the composite image with zeros
    composite_image = np.zeros_like(images[0], dtype=np.float32)
        
        # Iterate through the images and weights, adding the weighted images to the composite image
    for image, weight in zip(images, weights):
        composite_image += image * weight
        
        # Normalize the composite image to the range [0, 255]
    composite_image = np.clip(composite_image, 0, 255).astype(np.uint8)
        
    return composite_image

def rotate_image(image, turns):
        # Normalize the number of turns to be within 0-3
    turns = turns % 4
        
        # Rotate the image 90 degrees clockwise for each turn
    for _ in range(turns):
        image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
        
    return image

    # Example usage:
    # image = cv2.imread('image1.jpg')
    # rotated_image = rotate_image(image, 2)
    # save_image(rotated_image, 'rotated_image.jpg')
    
        # Ensure the image is in grayscale
def threshold_image(image, threshold):
    image_copy = image.copy()
        # Apply the threshold using numpy
    binary_image = np.where(image_copy > threshold, 255, 0).astype(np.uint8)
        
    return binary_image
    

    # Example usage:
    # gray_image = cv2.imread('gray_image.jpg', cv2.IMREAD_GRAYSCALE)
    # thresholded_image = threshold_image(gray_image, 128)
    # save_image(thresholded_image, 'thresholded_image.jpg')
    
# def replace_white_regions_with_color(color_image, bw_image, rgb_value):
#         # Ensure the black and white image is in grayscale
#     copy_img = color_image.copy()   
#         # Create a mask where the white regions in the black and white image are
#     mask = bw_image == 255
        
#         # Replace the white regions in the color image with the specified RGB value
#     copy_img[mask] = rgb_value
        
#     return copy_img

    # Example usage:
    # color_image = cv2.imread('color_image.jpg')
    # bw_image = cv2.imread('bw_image.jpg', cv2.IMREAD_GRAYSCALE)
    # rgb_value = [255, 0, 0]  # Red color
    # result_image = replace_white_regions_with_color(color_image, bw_image, rgb_value)
    # save_image(result_image, 'result_image.jpg')

def img_segmentation_rgb(img):
    red = img[:,:,0]
    green = img[:,:,1]
    blue = img[:,:,2]
    return red, green, blue



def img_array_thresh_n_replace_n_background(original_img, img_array, thresh_array=[70,70,70], color_array=[(50, 205, 50), (50, 205, 50), (50, 205, 50)]):
    new_img_array = []
    i = 0
    for img in img_array:
        black_white_img = threshold_image(rgb2gray(img), thresh_array[i])
        new_background = replace_white_regions_with_color(original_img, black_white_img, color_array[i])
        new_img_array.append(new_background)
        i = i + 1
    return new_img_array
 
 
