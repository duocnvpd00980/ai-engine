from fastapi import APIRouter, Response
from models.ad_request import AdRequest
from services.banner_service import generate_banner

router = APIRouter()

@router.post("/generate")
async def api_generate_banner(request: AdRequest):
    # 'request' tự động được validate bởi Pydantic
    image_bytes = await generate_banner(request)
    return Response(content=image_bytes, media_type="image/png")