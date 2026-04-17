from fastapi import APIRouter, Response
import logging
import io

from render.canvas_renderer import render_canvas
from templates.template_store import TEMPLATES
from models.canvas_request import CanvasRequest

router = APIRouter()
logger = logging.getLogger("CanvasTestAPI")


@router.post("/test-canvas")
async def test_canvas(request: CanvasRequest):

    logger.info("🔥 HIT /test-canvas")

    try:
        template_id = request.template_id
        data = request.data or {}

        if not template_id:
            logger.error("❌ Missing template_id")
            return Response(b"", media_type="image/png")

        template = TEMPLATES.get(template_id)

        if not template:
            logger.error(f"❌ Template not found: {template_id}")
            return Response(b"", media_type="image/png")

        layers = template.get("layers", [])
        if not layers:
            logger.error("❌ Template has no layers")
            return Response(b"", media_type="image/png")

        logger.info(f"📦 Template: {template_id}")
        logger.info(f"📐 Size: {template.get('width')}x{template.get('height')}")
        logger.info(f"🧩 Layers: {len(layers)}")
        logger.info(f"🧠 Data keys: {list(data.keys())}")

        img = render_canvas(template, data)

        if img is None:
            logger.error("❌ Render returned None")
            return Response(b"", media_type="image/png")

        buffer = io.BytesIO()
        img = img.convert("RGBA")
        img.save(buffer, format="PNG")

        image_bytes = buffer.getvalue()

        if not image_bytes or len(image_bytes) < 100:
            logger.error("❌ Image empty or invalid")
            return Response(b"", media_type="image/png")

        logger.info(f"✅ DONE | {len(image_bytes)} bytes")

        return Response(
            content=image_bytes,
            media_type="image/png"
        )

    except Exception as e:
        logger.exception(f"🔥 ERROR: {str(e)}")
        return Response(b"", media_type="image/png")