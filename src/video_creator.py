import cv2
import numpy as np
import os
from src.cartoonizer import Cartoonizer

class VideoCreator:
    def __init__(self):
        self.cartoonizer = Cartoonizer()
    
    def create_cartoon_video(self, input_path, output_path, style='default', fps=24):
        """
        Convert video to cartoon style
        """
        cap = cv2.VideoCapture(input_path)
        
        # Get video properties
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        original_fps = cap.get(cv2.CAP_PROP_FPS)
        
        # Use original FPS if available, otherwise use specified FPS
        fps = original_fps if original_fps > 0 else fps
        
        # Define codec and create VideoWriter
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))
        
        frame_count = 0
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Apply cartoon effect
            cartoon_frame = self.cartoonizer.apply_cartoon_effect(frame, style)
            
            # Resize back to original dimensions
            cartoon_frame = cv2.resize(cartoon_frame, (frame_width, frame_height))
            
            out.write(cartoon_frame)
            frame_count += 1
            
            # Progress indicator
            if frame_count % 30 == 0:
                print(f"Processed {frame_count} frames...")
        
        cap.release()
        out.release()
        
        return output_path, frame_count