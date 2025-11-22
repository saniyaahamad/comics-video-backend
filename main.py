from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.responses import JSONResponse
import cv2
import numpy as np
import os
from typing import List, Optional

from src.cartoonizer import Cartoonizer
from src.video_creator import VideoCreator
from src.utils import ensure_directories, allowed_file, generate_filename, save_uploaded_file
from config import config

app = FastAPI(title="Comics and Video Cartoonizer API", version="1.0.0")

# Initialize components
cartoonizer = Cartoonizer()
video_creator = VideoCreator()

# Ensure directories exist on startup
ensure_directories()

@app.get("/")
async def root():
    return {"message": "Comics and Video Cartoonizer API", "status": "running"}

@app.post("/cartoonize/image")
async def cartoonize_image(
    file: UploadFile = File(...),
    style: str = Form('default'),
    output_format: str = Form('png')
):
    """
    Cartoonize a single image
    Styles: default, comic, sketch, painting
    """
    try:
        # Validate file
        if not allowed_file(file.filename):
            raise HTTPException(status_code=400, detail="File type not allowed")
        
        # Save uploaded file
        filename = generate_filename(output_format, 'cartoon_')
        file_path = await save_uploaded_file(file, filename)
        
        # Read and process image
        image = cv2.imread(file_path)
        if image is None:
            raise HTTPException(status_code=400, detail="Invalid image file")
        
        # Apply cartoon effect
        cartoon_image = cartoonizer.apply_cartoon_effect(image, style)
        
        # Save result
        output_path = os.path.join(config.OUTPUT_FOLDER, filename)
        cv2.imwrite(output_path, cartoon_image)
        
        # Clean up uploaded file
        os.remove(file_path)
        
        return JSONResponse({
            "status": "success",
            "message": "Image cartoonized successfully",
            "output_file": filename,
            "style": style
        })
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)