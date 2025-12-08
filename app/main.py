from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.routes.auth import router as auth_router
from app.routes.metrics import router as metrics_router

# Initialize FastAPI app
app = FastAPI(
    title="SIH SAR Colorization API",
    description="REST API with JWT Authentication and Model Metrics",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router)
app.include_router(metrics_router)


@app.get("/", tags=["root"])
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to SIH SAR Colorization API",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "auth": "/auth",
            "metrics": "/api/models/metrics"
        }
    }


@app.get("/health", tags=["health"])
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}
