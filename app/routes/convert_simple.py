import io
import base64
from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from PIL import Image

router = APIRouter(prefix="/api/v1/convert/simple", tags=["convert"])


@router.post("")
async def convert_simple_colorization(
    file: UploadFile = File(..., description="Grayscale image to convert")
):
    """
    Apply a simple pseudocolor mapping to grayscale image.
    This is a fallback method that doesn't require AI.
    
    Args:
        file: Uploaded grayscale image file
        
    Returns:
        JSON response with colorized image in base64 format
    """
    
    if not file.content_type.startswith('image/'):
        raise HTTPException(
            status_code=400,
            detail="File must be an image"
        )
    
    try:
        image_bytes = await file.read()
        original_image = Image.open(io.BytesIO(image_bytes))
        
        if original_image.mode != 'L':
            grayscale = original_image.convert('L')
        else:
            grayscale = original_image
        
        colored_image = Image.new('RGB', grayscale.size)
        pixels = grayscale.load()
        colored_pixels = colored_image.load()
        
        for i in range(grayscale.width):
            for j in range(grayscale.height):
                gray_value = pixels[i, j]
                
                # Simple color mapping based on intensity
                if gray_value < 85:
                    # Dark -> Blue tones (water)
                    r = gray_value // 3
                    g = gray_value // 2
                    b = gray_value
                elif gray_value < 170:
                    # Mid -> Green tones (vegetation)
                    r = gray_value // 3
                    g = gray_value
                    b = gray_value // 3
                else:
                    # Bright -> Brown/Red tones (urban/soil)
                    r = gray_value
                    g = gray_value // 2
                    b = gray_value // 4
                
                colored_pixels[i, j] = (r, g, b)
        
        # Convert to base64
        buffer = io.BytesIO()
        colored_image.save(buffer, format="PNG")
        img_base64 = base64.b64encode(buffer.getvalue()).decode()
        
        return JSONResponse(content={
            "success": True,
            "message": "Simple colorization applied",
            "original_filename": file.filename,
            "colorized_image_base64": f"data:image/png;base64,{img_base64}",
            "method": "pseudocolor_mapping"
        })
        
    except Exception as e:
        import traceback
        error_detail = f"Error processing image: {str(e)}\n{traceback.format_exc()}"
        print(error_detail)
        raise HTTPException(
            status_code=500,
            detail=f"Error processing image: {str(e)}"
        )
