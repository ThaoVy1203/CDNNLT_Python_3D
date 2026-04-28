import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # Database
    DB_SERVER: str = os.getenv("DB_SERVER", "localhost")
    DB_NAME: str = os.getenv("DB_NAME", "dbCDNNLT")
    DB_USER: str = os.getenv("DB_USER", "sa")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "123456")
    
    # API
    API_TITLE: str = "API Hệ thống Giải Toán Hình Học 3D"
    API_VERSION: str = "1.0.0"
    API_DESCRIPTION: str = "API cho hệ thống giải toán hình học không gian 3 chiều sử dụng Gemini AI"
    
    # Gemini AI
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    
    # CORS
    CORS_ORIGINS: list = ["*"]

settings = Settings()
