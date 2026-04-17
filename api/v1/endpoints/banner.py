from fastapi import APIRouter, Response
from models.ad_request import AdRequest
from services.banner_service import generate_banner
import logging

router = APIRouter()
logger = logging.getLogger("BannerAPI")


@router.post("/generate")
async def api_generate_banner(request: AdRequest):
    logger.info("🔥 HIT /v1/generate endpoint")
    logger.info(f"📦 REQUEST: {request.model_dump()}")

    image_bytes = await generate_banner(request)

    if not image_bytes:
        logger.error("❌ generate_banner returned empty result")
        return Response(content=b"", media_type="image/png")

    logger.info(f"✅ IMAGE SIZE: {len(image_bytes)} bytes")

    return Response(content=image_bytes, media_type="image/png")