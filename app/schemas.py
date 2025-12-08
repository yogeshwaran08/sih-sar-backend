from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class UserBase(BaseModel):
    """Base user schema"""
    username: str
    email: EmailStr


class UserCreate(UserBase):
    """User creation schema"""
    password: str


class UserResponse(UserBase):
    """User response schema"""
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    """User login schema"""
    username: str
    password: str


class TokenResponse(BaseModel):
    """Token response schema (access token only)"""
    access_token: str
    token_type: str = "bearer"


class TokenRefresh(BaseModel):
    """Token refresh schema"""
    refresh_token: str


class CurrentUser(BaseModel):
    """Current user schema"""
    id: int
    username: str
    email: str
    is_active: bool


# Metrics Schemas for SAR Colorization Model
class EpochPreviews(BaseModel):
    """Preview images for an epoch"""
    input: Optional[str] = None
    generated: Optional[str] = None
    gt: Optional[str] = None


class EpochRecord(BaseModel):
    """Metrics record for a single epoch"""
    epoch: int
    G_total: float
    D_total: float
    loss_GAN: Optional[float] = None
    loss_pixel: Optional[float] = None
    loss_perceptual: Optional[float] = None
    psnr: Optional[float] = None
    ssim: Optional[float] = None
    lpips: Optional[float] = None
    fid: Optional[float] = None
    deltaE2000_mean: Optional[float] = None
    deltaE2000_median: Optional[float] = None
    lr: Optional[float] = None
    epochTimeMs: Optional[int] = None
    previews: Optional[EpochPreviews] = None


class ModelMetricsData(BaseModel):
    """Complete metrics data for a model"""
    model: str
    version: str
    dataset: str
    epochs: list[EpochRecord]


class ModelsResponse(BaseModel):
    """Response containing all models"""
    models: dict[str, ModelMetricsData]
