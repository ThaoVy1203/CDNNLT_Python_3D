from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.nguoi_dung_routes import router as nguoi_dung_router
from routes.bai_toan_routes import router as bai_toan_router

app = FastAPI(
    title="API Hệ thống Giải Toán Hình Học",
    description="API cho hệ thống giải toán hình học 3D",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(nguoi_dung_router)
app.include_router(bai_toan_router)

@app.get("/")
def root():
    return {
        "message": "API Hệ thống Giải Toán Hình Học",
        "docs": "/docs",
        "status": "running"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
