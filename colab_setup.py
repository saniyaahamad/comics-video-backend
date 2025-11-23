# Google Colab Setup for Comics-Video-Backend
import os
import subprocess
import requests
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
import cv2
import numpy as np
import uvicorn
from google.colab.output import eval_js

# Install dependencies
print("Installing dependencies...")
subprocess.run(["pip", "install", "-r", "requirements.txt"], check=True)

# Import your modules
from src.cartoonizer import Cartoonizer
from src.video_creator import VideoCreator  
from src.utils import ensure_directories, allowed_file, generate_filename, save_uploaded_file
import config

app = FastAPI(title="Comics Video Backend - Colab", version="1.0.0")

# Initialize components
cartoonizer = Cartoonizer()
video_creator = VideoCreator()
ensure_directories()

@app.get("/")
async def root():
    return {"message": "Comics Video Backend running on Colab!", "status": "running"}

@app.post("/cartoonize")
async def cartoonize_media(file: UploadFile = File(...), style: str = Form('default')):
    """Unified endpoint for images and videos"""
    try:
        if not allowed_file(file.filename):
            return JSONResponse({"status": "error", "message": "File type not allowed"})
        
        file_extension = file.filename.split('.')[-1].lower()
        
        if file_extension in ['png', 'jpg', 'jpeg']:
            # Process image
            filename = generate_filename('png', 'cartoon_')
            file_path = await save_uploaded_file(file, filename)
            image = cv2.imread(file_path)
            cartoon_image = cartoonizer.apply_cartoon_effect(image, style)
            output_path = os.path.join(config.OUTPUT_FOLDER, filename)
            cv2.imwrite(output_path, cartoon_image)
            os.remove(file_path)
            return JSONResponse({
                "status": "success", 
                "message": "Image processed!",
                "output_file": filename,
                "media_type": "image",
                "style": style
            })
            
        elif file_extension in ['mp4', 'avi', 'mov']:
            # Process video  
            filename = generate_filename('mp4', 'cartoon_video_')
            file_path = await save_uploaded_file(file, filename)
            output_filename = generate_filename('mp4', 'cartoon_')
            output_path = os.path.join(config.OUTPUT_FOLDER, output_filename)
            output_path, frame_count = video_creator.create_cartoon_video(file_path, output_path, style)
            os.remove(file_path)
            return JSONResponse({
                "status": "success",
                "message": "Video processed!",
                "output_file": output_filename, 
                "media_type": "video",
                "style": style,
                "frames_processed": frame_count
            })
            
    except Exception as e:
        return JSONResponse({"status": "error", "message": str(e)})

# Colab-specific setup
def run_in_colab():
    print("?? Starting server on Colab...")
    # Get public URL using ngrok
    from pyngrok import ngrok
    public_url = ngrok.connect(8000)
    print(f"?? Your API is live at: {public_url}")
    print(f"?? API docs: {public_url}/docs")
    
    # Start server
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    run_in_colab()