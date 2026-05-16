from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.core.config import settings
from app.api.routes import nguoi_dung, bai_toan, geometry, auth
import os
import asyncio

app = FastAPI(
    title=settings.API_TITLE,
    description=settings.API_DESCRIPTION,
    version=settings.API_VERSION
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve thư mục uploads/ dưới route /uploads
os.makedirs("uploads", exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Include routers
app.include_router(auth.router)
app.include_router(nguoi_dung.router)
app.include_router(bai_toan.router)
app.include_router(geometry.router)

@app.on_event("startup")
async def startup_event():
    """Initialize File Search on startup"""
    if settings.USE_FILE_SEARCH:
        print("\n" + "="*60)
        print("📚 INITIALIZING FILE SEARCH")
        print("="*60)
        try:
            from app.services.file_search_service import file_search_service
            # Run initialization in background to not block startup
            asyncio.create_task(file_search_service.initialize())
            print("✅ File Search initialization started in background")
        except Exception as e:
            print(f"⚠️  File Search initialization failed: {e}")
            print("   Server will continue without File Search")
        print("="*60 + "\n")
    else:
        print("\n📚 File Search is DISABLED (USE_FILE_SEARCH=false)\n")

@app.get("/")
def root():
    return {
        "message": settings.API_TITLE,
        "version": settings.API_VERSION,
        "docs": "/docs",
        "status": "running",
        "file_search_enabled": settings.USE_FILE_SEARCH
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy", 
        "version": settings.API_VERSION,
        "file_search_enabled": settings.USE_FILE_SEARCH
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
