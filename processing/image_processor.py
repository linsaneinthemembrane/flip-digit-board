import cv2
import numpy as np
from PIL import Image

class ImageProcessor:
    def __init__(self):
        pass
        
    def process_image(self, image_path, target_width=40, target_height=25):
        """Process image for flip digit display"""
        try:
            # Read image using OpenCV
            image = cv2.imread(image_path)
            if image is None:
                print(f"Could not load image: {image_path}")
                return None
                
            # Convert BGR to RGB
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            # Resize to target dimensions
            image = cv2.resize(image, (target_width, target_height), interpolation=cv2.INTER_LANCZOS4)
            
            # Convert to grayscale
            gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
            
            # Apply Gaussian blur to reduce noise
            blurred = cv2.GaussianBlur(gray, (3, 3), 0)
            
            # Apply adaptive thresholding for better binary conversion
            binary = cv2.adaptiveThreshold(
                blurred, 
                255, 
                cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                cv2.THRESH_BINARY, 
                11, 
                2
            )
            
            # Invert so black pixels become white (displayed segments)
            binary = cv2.bitwise_not(binary)
            
            return binary
            
        except Exception as e:
            print(f"Error processing image: {e}")
            return None
            
    def image_to_ascii(self, image_array, ascii_chars=" .:-=+*#%@"):
        """Convert image to ASCII representation"""
        if len(image_array.shape) == 3:
            image_array = np.mean(image_array, axis=2)
            
        # Normalize to 0-1 range
        normalized = image_array / 255.0
        
        # Map to ASCII characters
        ascii_image = []
        for row in normalized:
            ascii_row = ""
            for pixel in row:
                char_index = int(pixel * (len(ascii_chars) - 1))
                ascii_row += ascii_chars[char_index]
            ascii_image.append(ascii_row)
            
        return ascii_image