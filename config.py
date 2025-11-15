import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Application configuration"""
    
    # API Keys
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    
    # File Upload Settings
    UPLOAD_FOLDER = 'uploads'
    MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB
    
    # AI Settings
    AI_MODEL_GEMINI = 'gemini-2.0-flash-lite'
    MAX_TOKENS = 1000
    TEMPERATURE = 0.7
    
    # App Settings
    APP_NAME = "Smart Insight Engine"
    DEBUG = True

    @staticmethod
    def init_app():
        """Initialize application folders"""
        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
        os.makedirs('data', exist_ok=True)
        os.makedirs('outputs', exist_ok=True)

# Initialize folders
Config.init_app()

# Test config
if __name__ == "__main__":
    print("="*60)
    print("CONFIG TEST")
    print("="*60)
    print(f"Gemini Key Set: {bool(Config.GEMINI_API_KEY)}")
    print(f"Upload Folder: {Config.UPLOAD_FOLDER}")
    print(f"AI Model (GEMINI): {Config.AI_MODEL_GEMINI}")
    print("="*60)