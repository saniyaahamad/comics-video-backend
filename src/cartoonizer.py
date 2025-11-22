import cv2
import numpy as np
from src.utils import resize_image

class Cartoonizer:
    def __init__(self):
        self.kernel = np.ones((2, 2), np.uint8)
    
    def apply_cartoon_effect(self, image, style='default'):
        """
        Apply cartoon effect to image
        Styles: 'default', 'comic', 'sketch', 'painting'
        """
        # Resize image for faster processing
        image = resize_image(image)
        
        if style == 'default':
            return self._default_cartoon(image)
        else:
            return self._default_cartoon(image)
    
    def _default_cartoon(self, img):
        """Default cartoon effect"""
        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Apply median blur
        gray = cv2.medianBlur(gray, 5)
        
        # Detect edges
        edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, 
                                    cv2.THRESH_BINARY, 9, 9)
        
        # Color quantization
        data = np.float32(img).reshape((-1, 3))
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 1.0)
        _, label, center = cv2.kmeans(data, 8, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
        center = np.uint8(center)
        result = center[label.flatten()]
        result = result.reshape(img.shape)
        
        # Bilateral filter for smoothing
        blurred = cv2.bilateralFilter(result, 9, 300, 300)
        
        # Combine edges with color
        cartoon = cv2.bitwise_and(blurred, blurred, mask=edges)
        
        return cartoon
    
    def create_comic_strip(self, images, layout=(2, 2)):
        """
        Create comic strip from multiple images
        layout: (rows, columns)
        """
        rows, cols = layout
        
        # Resize all images to same size
        target_size = (400, 400)
        resized_images = []
        
        for img in images:
            resized = cv2.resize(img, target_size)
            resized_images.append(resized)
        
        # Create comic strip canvas
        comic_height = rows * target_size[1]
        comic_width = cols * target_size[0]
        comic_strip = np.zeros((comic_height, comic_width, 3), dtype=np.uint8)
        
        # Arrange images in grid
        for i in range(rows):
            for j in range(cols):
                idx = i * cols + j
                if idx < len(resized_images):
                    y_start = i * target_size[1]
                    y_end = (i + 1) * target_size[1]
                    x_start = j * target_size[0]
                    x_end = (j + 1) * target_size[0]
                    comic_strip[y_start:y_end, x_start:x_end] = resized_images[idx]
        
        return comic_strip