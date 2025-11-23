import cv2
import cv2
import numpy as np
import os

class VideoCreator:
    def __init__(self):
        pass
    
    def create_cartoon_video(self, input_path, output_path, style='default'):
        """
        Simple video processing - just copy the video for now
        """
        # For testing, just copy the file
        import shutil
        shutil.copy2(input_path, output_path)
        
        # Get frame count
        cap = cv2.VideoCapture(input_path)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        cap.release()
        
        return output_path, frame_count