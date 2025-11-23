from fastapi import FastAPI, File, UploadFile, HTTPException, Form 
from fastapi.responses import JSONResponse 
import os 
 
from src.cartoonizer import Cartoonizer 
from src.video_creator import VideoCreator 
from src.utils import ensure_directories, allowed_file, generate_filename, save_uploaded_file 
import config 
 
app = FastAPI() 
 
cartoonizer = Cartoonizer() 
video_creator = VideoCreator() 
 
ensure_directories() 
 
@app.get("/") 
async def root(): 
    return {"message": "API Working"} 
 
@app.post("/cartoonize/image") 
async def cartoonize_image(file: UploadFile = File(...)): 
    return {"status": "image endpoint"} 
 
@app.post("/cartoonize/video") 
async def cartoonize_video(file: UploadFile = File(...)): 
    return {"status": "video endpoint"} 
 
if __name__ == "__main__": 
    import uvicorn 
    uvicorn.run(app, host="0.0.0.0", port=8000) 
