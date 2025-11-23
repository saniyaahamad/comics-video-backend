import os
from dotenv import load_dotenv

load_dotenv()

# GitHub Configuration
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
GITHUB_REPO = os.getenv('GITHUB_REPO', 'saniyaahamad/comics-video-backend')
GITHUB_BRANCH = os.getenv('GITHUB_BRANCH', 'main')

# File paths - Use absolute paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
OUTPUT_FOLDER = os.path.join(BASE_DIR, 'output')
TEMP_FOLDER = os.path.join(BASE_DIR, 'temp')

# Supported formats
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'mp4', 'avi', 'mov'}
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
