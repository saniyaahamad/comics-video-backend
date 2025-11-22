import os
import cv2
import numpy as np
import aiofiles
import uuid
from config import config

def ensure_directories():
    """Create necessary directories if they don't exist"""
    for directory in [config.UPLOAD_FOLDER, config.OUTPUT_FOLDER, config.TEMP_FOLDER]:
        os.makedirs(directory, exist_ok=True)

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in config.ALLOWED_EXTENSIONS

def generate_filename(extension, prefix=''):
    """Generate unique filename"""
    return f"{prefix}{uuid.uuid4().hex}.{extension}"

async def save_uploaded_file(file, filename):
    """Save uploaded file asynchronously"""
    file_path = os.path.join(config.UPLOAD_FOLDER, filename)
    async with aiofiles.open(file_path, 'wb') as buffer:
        content = await file.read()
        await buffer.write(content)
    return file_path

def resize_image(image, max_size=800):
    """Resize image while maintaining aspect ratio"""
    h, w = image.shape[:2]
    
    if max(h, w) > max_size:
        if h > w:
            new_h = max_size
            new_w = int(w * (max_size / h))
        else:
            new_w = max_size
            new_h = int(h * (max_size / w))
        
        image = cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_AREA)
    
    return image