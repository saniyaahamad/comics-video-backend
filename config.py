import os 
from dotenv import load_dotenv 
 
load_dotenv() 
 
# GitHub Configuration 
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN') 
GITHUB_REPO = os.getenv('GITHUB_REPO', 'saniyaahamad/comics-video-backend') 
GITHUB_BRANCH = os.getenv('GITHUB_BRANCH', 'main') 
 
# File paths 
UPLOAD_FOLDER = 'uploads' 
OUTPUT_FOLDER = 'output' 
TEMP_FOLDER = 'temp' 
 
# Supported formats 
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'mp4', 'avi', 'mov'} 
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB 
