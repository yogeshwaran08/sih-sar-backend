from fastapi import APIRouter, HTTPException
from app.schemas import ModelsResponse, ModelMetricsData, EpochRecord
import pandas as pd
from pathlib import Path
from typing import Dict

router = APIRouter(prefix="/api/models", tags=["metrics"])

DATA_DIR = Path(__file__).parent.parent.parent / "data"


def load_model_data() -> Dict[str, ModelMetricsData]:
    """Load model metrics data from CSV files."""
    model_data = {}
    
    metadata_file = DATA_DIR / "models_metadata.csv"
    if not metadata_file.exists():
        return {}
    
    metadata_df = pd.read_csv(metadata_file)
    
    for _, row in metadata_df.iterrows():
        model_id = row['model_id']
        csv_file = DATA_DIR / f"{model_id}.csv"
        
        if not csv_file.exists():
            continue
        
        epochs_df = pd.read_csv(csv_file)
        
        epochs = []
        for _, epoch_row in epochs_df.iterrows():
            epochs.append(
                EpochRecord(
                    epoch=int(epoch_row['epoch']),
                    G_total=float(epoch_row['G_total']),
                    D_total=float(epoch_row['D_total']),
                    loss_GAN=float(epoch_row['loss_GAN']),
                    loss_pixel=float(epoch_row['loss_pixel']),
                    loss_perceptual=float(epoch_row['loss_perceptual']),
                    psnr=float(epoch_row['psnr']),
                    ssim=float(epoch_row['ssim']),
                    lpips=float(epoch_row['lpips']),
                    fid=float(epoch_row['fid']) if pd.notna(epoch_row['fid']) else None,
                    deltaE2000_mean=float(epoch_row['deltaE2000_mean']),
                    deltaE2000_median=float(epoch_row['deltaE2000_median']),
                    lr=float(epoch_row['lr']),
                    epochTimeMs=int(epoch_row['epochTimeMs'])
                )
            )
        
        model_data[model_id] = ModelMetricsData(
            model=row['model'],
            version=row['version'],
            dataset=row['dataset'],
            epochs=epochs
        )
    
    return model_data


MODEL_DATA = load_model_data()


@router.get("/metrics", response_model=ModelsResponse)
async def get_all_model_metrics():
    """
    Get metrics for all available SAR colorization models.
    
    Returns complete training metrics including:
    - Loss values (Generator, Discriminator, GAN, Pixel, Perceptual)
    - Quality metrics (PSNR, SSIM, LPIPS, FID)
    - Color accuracy (deltaE2000)
    - Training parameters (learning rate, epoch time)
    """
    return ModelsResponse(models=MODEL_DATA)


@router.get("/{model_id}/metrics", response_model=ModelMetricsData)
async def get_model_metrics(model_id: str):
    """
    Get metrics for a specific model by ID.
    
    Args:
        model_id: Identifier for the model (e.g., 'sar-colorizer-v1')
        
    Returns:
        Complete metrics data for the specified model
        
    Raises:
        404: Model not found
    """
    if model_id not in MODEL_DATA:
        raise HTTPException(
            status_code=404, 
            detail=f"Model '{model_id}' not found. Available models: {list(MODEL_DATA.keys())}"
        )
    return MODEL_DATA[model_id]


@router.get("/{model_id}/metrics/latest", response_model=EpochRecord)
async def get_latest_epoch_metrics(model_id: str):
    """
    Get metrics for the latest epoch of a specific model.
    
    Args:
        model_id: Identifier for the model
        
    Returns:
        Metrics from the most recent training epoch
        
    Raises:
        404: Model not found
    """
    if model_id not in MODEL_DATA:
        raise HTTPException(
            status_code=404,
            detail=f"Model '{model_id}' not found"
        )
    
    model_data = MODEL_DATA[model_id]
    if not model_data.epochs:
        raise HTTPException(
            status_code=404,
            detail=f"No epochs found for model '{model_id}'"
        )
    
    return model_data.epochs[-1]


@router.get("/{model_id}/metrics/epoch/{epoch_number}", response_model=EpochRecord)
async def get_epoch_metrics(model_id: str, epoch_number: int):
    """
    Get metrics for a specific epoch of a model.
    
    Args:
        model_id: Identifier for the model
        epoch_number: Epoch number to retrieve
        
    Returns:
        Metrics from the specified epoch
        
    Raises:
        404: Model or epoch not found
    """
    if model_id not in MODEL_DATA:
        raise HTTPException(
            status_code=404,
            detail=f"Model '{model_id}' not found"
        )
    
    model_data = MODEL_DATA[model_id]
    
    # Find the epoch
    epoch = next((e for e in model_data.epochs if e.epoch == epoch_number), None)
    
    if not epoch:
        raise HTTPException(
            status_code=404,
            detail=f"Epoch {epoch_number} not found for model '{model_id}'"
        )
    
    return epoch
