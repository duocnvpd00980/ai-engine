from fastapi import APIRouter, Response
import logging
import io

from models.template_request import CanvasRenderRequest
from render.canvas_renderer import render_canvas
from templates.template_store import TEMPLATES
from models.canvas_request import CanvasRequest

router = APIRouter()
logger = logging.getLogger("CanvasTestAPI")


@router.post("/test-template")
async def template_canvas(request: CanvasRenderRequest):

    logger.info("🔥 HIT /render-canvas")

    try:
        template = request.template
        data = request.data or {}

        if not template:
            logger.error("❌ Missing template")
            return Response(b"", media_type="image/png")

        layers = template.get("layers", [])
        if not layers:
            logger.error("❌ Template has no layers")
            return Response(b"", media_type="image/png")

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

        return Response(
            content=image_bytes,
            media_type="image/png"
        )

    except Exception as e:
        logger.exception(f"🔥 ERROR: {str(e)}")
        return Response(b"", media_type="image/png")