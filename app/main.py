from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.config import settings
from app.routes.auth import router as auth_router
from app.routes.gallery import router as gallery_router
from app.routes.metrics import router as metrics_router
from app.routes.convert import router as convert_router
from app.routes.convert_simple import router as convert_simple_router

app = FastAPI(
    title="SIH SAR Colorization API",
    description="REST API with JWT Authentication and Model Metrics",
    version="1.0.0"
)

BASE_DIR = Path(__file__).resolve().parent.parent

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost",
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
        "*",  # Allow all in development - remove in production
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Include routers
app.include_router(auth_router)
app.include_router(metrics_router)
app.include_router(gallery_router)
app.include_router(convert_router)
app.include_router(convert_simple_router)

# Serve static assets (images) - must be mounted after routers
ASSETS_DIR = BASE_DIR / "assets"
if ASSETS_DIR.exists():
    app.mount("/assets", StaticFiles(directory=str(ASSETS_DIR)), name="assets")


@app.get("/", tags=["root"])
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to SIH SAR Colorization API",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "auth": "/auth",
            "metrics": "/api/models/metrics",
            "gallery": "/api/gallery"
        }
    }


@app.get("/health", tags=["health"])
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}
