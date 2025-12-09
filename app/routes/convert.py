import io
import base64
import numpy as np
from typing import Optional
from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from PIL import Image
import cv2

from app.config import settings

router = APIRouter(prefix="/api/v1/convert", tags=["convert"])

colorization_net = None

def load_colorization_model():
    """Load the colorization model (using OpenCV's pre-trained model)"""
    global colorization_net
    if colorization_net is None:
        try:
            prototxt = "models/colorization_deploy_v2.prototxt"
            caffemodel = "models/colorization_release_v2.caffemodel"
            pts_npy = "models/pts_in_hull.npy"
            
            colorization_net = cv2.dnn.readNetFromCaffe(prototxt, caffemodel)
            pts = np.load(pts_npy)
            
            # Load cluster centers
            class8 = colorization_net.getLayerId("class8_ab")
            conv8 = colorization_net.getLayerId("conv8_313_rh")
            pts = pts.transpose().reshape(2, 313, 1, 1)
            colorization_net.getLayer(class8).blobs = [pts.astype("float32")]
            colorization_net.getLayer(conv8).blobs = [np.full([1, 313], 2.606, dtype="float32")]
            
            print("Colorization model loaded successfully")
        except Exception as e:
            print(f"Warning: Could not load pre-trained model: {e}")
            colorization_net = "simple"  # Fallback to simple method
    
    return colorization_net

@router.post("")
async def convert_grayscale_to_color(
    file: UploadFile = File(..., description="Grayscale SAR image to convert")
):
    """
    Convert a grayscale SAR image to a colorized version using Gemini AI.
    
    Args:
        file: Uploaded grayscale image file (JPEG, PNG, etc.)
        
    Returns:
        JSON response with the colorized image in base64 format
    """
    
    # Validate file type
    if not file.content_type.startswith('image/'):
        raise HTTPException(
            status_code=400,
            detail="File must be an image (JPEG, PNG, etc.)"
        )
    
    try:
        # Read the uploaded file
        image_bytes = await file.read()
        original_image = Image.open(io.BytesIO(image_bytes))
        
        # Convert to RGB if needed
        if original_image.mode != 'RGB':
            original_image = original_image.convert('RGB')
        
        # Convert PIL to numpy array
        img_array = np.array(original_image)
        
        # Try to load and use the colorization model
        model = load_colorization_model()
        
        if model == "simple":
            # Fallback to simple pseudocolor method
            colorized_image = apply_simple_colorization(img_array)
            method = "pseudocolor_mapping"
        else:
            # Use deep learning colorization
            colorized_image = apply_dl_colorization(img_array, model)
            method = "deep_learning_colorization"
        
        # Convert result to PIL Image
        result_image = Image.fromarray(colorized_image.astype('uint8'))
        
        # Convert to base64
        buffer = io.BytesIO()
        result_image.save(buffer, format="PNG")
        img_base64 = base64.b64encode(buffer.getvalue()).decode()
        
        # Also include original for comparison
        orig_buffer = io.BytesIO()
        original_image.save(orig_buffer, format="PNG")
        orig_base64 = base64.b64encode(orig_buffer.getvalue()).decode()
        
        return JSONResponse(content={
            "success": True,
            "message": "Image colorized successfully",
            "original_filename": file.filename,
            "original_size": {
                "width": original_image.width,
                "height": original_image.height
            },
            "method": method,
            "original_image_base64": f"data:image/png;base64,{orig_base64}",
            "colorized_image_base64": f"data:image/png;base64,{img_base64}"
        })
        
    except Exception as e:
        import traceback
        error_detail = f"Error processing image: {str(e)}\n{traceback.format_exc()}"
        print(error_detail)
        raise HTTPException(
            status_code=500,
            detail=f"Error processing image: {str(e)}"
        )

def apply_dl_colorization(img_array, model):
    img_rgb = cv2.cvtColor(img_array, cv2.COLOR_BGR2RGB)
    img_lab = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2LAB)
    img_l = img_lab[:, :, 0]
    img_l_resized = cv2.resize(img_l, (224, 224))
    img_l_resized = img_l_resized - 50
    model.setInput(cv2.dnn.blobFromImage(img_l_resized))
    ab = model.forward()[0, :, :, :].transpose((1, 2, 0))
    ab = cv2.resize(ab, (img_array.shape[1], img_array.shape[0]))
    img_lab_colored = np.concatenate((img_l[:, :, np.newaxis], ab), axis=2)
    img_rgb_colored = cv2.cvtColor(img_lab_colored.astype('float32'), cv2.COLOR_LAB2RGB)
    img_rgb_colored = np.clip(img_rgb_colored, 0, 255)
    return img_rgb_colored


def apply_simple_colorization(img_array):
    if len(img_array.shape) == 3:
        gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
    else:
        gray = img_array
    height, width = gray.shape
    colored = np.zeros((height, width, 3), dtype=np.uint8)
    mask_dark = gray < 85
    colored[mask_dark] = np.stack([gray[mask_dark] // 3, gray[mask_dark] // 2, gray[mask_dark]], axis=-1)
    mask_mid = (gray >= 85) & (gray < 170)
    colored[mask_mid] = np.stack([gray[mask_mid] // 3, gray[mask_mid], gray[mask_mid] // 3], axis=-1)
    mask_bright = gray >= 170
    colored[mask_bright] = np.stack([gray[mask_bright], gray[mask_bright] // 2, gray[mask_bright] // 4], axis=-1)
    return colored
