from pathlib import Path
from typing import List

from fastapi import APIRouter, HTTPException, Request

router = APIRouter(prefix="/api/gallery", tags=["gallery"])

BASE_DIR = Path(__file__).resolve().parent.parent.parent
CANDIDATE_DIRS = [
    BASE_DIR / "assets" / "gallry",  # handle misspelling if present
    BASE_DIR / "assets" / "gallery",
    BASE_DIR / "assets",
]
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp"}


def get_assets_dir() -> Path:
    """Return the first existing assets directory."""
    for candidate in CANDIDATE_DIRS:
        if candidate.exists():
            return candidate
    return BASE_DIR / "assets"


def list_image_names(directory: Path) -> List[str]:
    """List image filenames in the given directory."""
    if not directory.exists():
        return []

    files: List[str] = []
    for item in directory.iterdir():
        if item.is_file() and item.suffix.lower() in IMAGE_EXTENSIONS:
            files.append(item.name)
    return sorted(files)


@router.get("/", response_model=List[str])
async def list_gallery_images(request: Request):
    """Return gallery images as a list of absolute URLs."""
    assets_dir = get_assets_dir()
    images = list_image_names(assets_dir)
    if not images:
        raise HTTPException(status_code=404, detail="No images found in gallery")

    base_url = str(request.base_url)  # includes trailing slash
    return [f"{base_url}assets/{name}" for name in images]
