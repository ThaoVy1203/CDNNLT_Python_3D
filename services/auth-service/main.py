from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import auth, nguoi_dung
from app.core.config import settings


app = FastAPI(
    title="Geo3D Auth Service",
    description="Authentication and user service for Geo3D",
    version=settings.API_VERSION,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(nguoi_dung.router)


@app.get("/")
def root():
    return {
        "service": "auth-service",
        "status": "running",
        "version": settings.API_VERSION,
    }


@app.get("/health")
def health_check():
    return {
        "service": "auth-service",
        "status": "healthy",
        "version": settings.API_VERSION,
    }

