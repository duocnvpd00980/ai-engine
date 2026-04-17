from fastapi import APIRouter, HTTPException
import logging

from models.ad_request import AdRequest
from services.brain_service import BrainService

router = APIRouter()
logger = logging.getLogger("AITestAPI")

brain_service = BrainService()


@router.post("/test-content")
async def test_content_ai(request: AdRequest):

    try:
        logger.info("🧠 CALL AI CREATIVE")

        ad_data = request.model_dump(exclude_none=True)
        logger.info(f"📦 INPUT DATA: {ad_data}")

        creative = await brain_service.analyze_and_creative(request)

        required = [
            "image_prompt",
            "main_title",
            "sub_title",
            "highlight_text",
            "cta_text"
        ]

        missing = [f for f in required if f not in creative]

        if missing:
            raise HTTPException(
                status_code=400,
                detail=f"Missing fields: {missing}"
            )

        logger.info("✅ AI CREATIVE SUCCESS")
        logger.info(f"📤 OUTPUT: {creative}")

        return {
            "success": True,
            "creative": creative
        }

    except Exception as e:
        logger.exception("❌ AI CREATIVE ERROR")
        raise HTTPException(status_code=500, detail=str(e))