import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # Database
    DB_SERVER: str = os.getenv("DB_SERVER", "NGOTHITHAOVY")
    DB_NAME: str = os.getenv("DB_NAME", "dbCDNNLT")
    DB_USER: str = os.getenv("DB_USER", "sa")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "123456")
    
    # API
    API_TITLE: str = "API Hệ thống Giải Toán Hình Học 3D"
    API_VERSION: str = "1.0.0"
    API_DESCRIPTION: str = "API cho hệ thống giải toán hình học không gian 3 chiều sử dụng Gemini AI"
    
    # Gemini AI
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-2.5-flash-lite")
    
    # Serper.dev (Google Search API)
    SERPER_API_KEY: str = os.getenv("SERPER_API_KEY", "")
    SEARCH_SERVICE_URL: str = os.getenv("SEARCH_SERVICE_URL", "http://127.0.0.1:8002")
    
    # File Search
    USE_FILE_SEARCH: bool = os.getenv("USE_FILE_SEARCH", "true").lower() == "true"
    DOCUMENTS_PATH: str = os.getenv("DOCUMENTS_PATH", "Documents")
    MAX_SEARCH_RESULTS: int = int(os.getenv("MAX_SEARCH_RESULTS", "3"))
    FILE_SEARCH_INDEX_NAME: str = os.getenv("FILE_SEARCH_INDEX_NAME", "geometry-documents-index")
    
    # CORS
    CORS_ORIGINS: list = ["*"]

settings = Settings()
