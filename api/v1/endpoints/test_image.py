from fastapi import APIRouter, HTTPException, Query
from services.image_service import ImageGenerationService # Đảm bảo đúng tên file/thư mục của bạn

router = APIRouter()
image_service = ImageGenerationService()

@router.get("/test-flux")
async def test_flux_generation(
    prompt: str = Query(..., example="A luxury interior of a modern villa, cinematic lighting, 8k")
):
    """
    Route để test nhanh khả năng tạo ảnh của Flux Pro 1.1 qua Vercel Gateway.
    """
    url = await image_service.generate_flux_image(prompt)
    
    if "your-storage.com" in url:
        raise HTTPException(
            status_code=500, 
            detail="Tạo ảnh thất bại, hệ thống đang dùng ảnh fallback. Kiểm tra lại API Key!"
        )
    
    return {
        "status": "success",
        "prompt": prompt,
        "image_url": url
    }