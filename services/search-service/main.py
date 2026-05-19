from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import search
from app.core.config import settings


app = FastAPI(
    title="Geo3D Search Service",
    description="Search service for similar geometry problems",
    version=settings.API_VERSION,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(search.router)


@app.get("/")
def root():
    return {
        "service": "search-service",
        "status": "running",
        "version": settings.API_VERSION,
    }


@app.get("/health")
def health_check():
    return {
        "service": "search-service",
        "status": "healthy",
        "version": settings.API_VERSION,
    }

