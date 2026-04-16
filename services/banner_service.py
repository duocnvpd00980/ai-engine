import base64
import cairosvg
import logging

from render.svg_renderer import render_svg
from services.pollinations_service import PollinationsService
from services.brain_service import BrainService
from core.config import SVG_CONTENT_RAW


brain_service = BrainService()
pollinations_service = PollinationsService()
logger = logging.getLogger("BannerService")


async def generate_banner(ad_data):
    try:
        # =========================
        # 1. 🧠 AI CONCEPT (GIỮ OBJECT, KHÔNG .model_dump())
        # =========================
        creative = await brain_service.analyze_and_creative(ad_data)

        # Validate basic (tránh crash ngầm)
        required_fields = [
            "image_prompt",
            "main_title",
            "sub_title",
            "highlight_text",
            "cta_text",
            "accent_color"
        ]

        for field in required_fields:
            if field not in creative:
                raise ValueError(f"Missing field from BrainService: {field}")

        # =========================
        # 2. 🎨 GENERATE IMAGE
        # =========================
        try:
            image_bytes = await pollinations_service.generate_image(
                creative["image_prompt"]
            )
        except Exception as e:
            logger.error(f"Image generation failed: {str(e)}")
            image_bytes = None

        # fallback image (tránh crash)
        if image_bytes:
            base64_img = f"data:image/png;base64,{base64.b64encode(image_bytes).decode()}"
        else:
            base64_img = ""  # SVG sẽ fallback background

        # =========================
        # 3. 🧩 RENDER SVG
        # =========================
        svg_data = {
            "image_url": base64_img,
            "brand_name": ad_data.brand_name,
            "main_title": creative["main_title"],
            "sub_title": creative["sub_title"],
            "highlight_text": creative["highlight_text"],
            "cta_text": creative["cta_text"],
            "accent_color": creative["accent_color"]
        }

        svg_rendered = render_svg(SVG_CONTENT_RAW, svg_data)

        # =========================
        # 4. 🖼️ EXPORT PNG
        # =========================
        png_bytes = cairosvg.svg2png(
            bytestring=svg_rendered.encode("utf-8"),
            output_width=1376,
            output_height=768
        )

        return png_bytes

    except Exception as e:
        logger.error(f"🔥 Banner Generation Failed: {str(e)}")
        return _fallback_banner(ad_data)


# =========================
# 🧯 FALLBACK (CỰC QUAN TRỌNG)
# =========================
def _fallback_banner(ad_data):
    try:
        svg_data = {
            "image_url": "",
            "brand_name": ad_data.brand_name,
            "main_title": "Luxury Experience",
            "sub_title": ad_data.product_info.name,
            "highlight_text": "ƯU ĐÃI ĐẶC BIỆT",
            "cta_text": "Xem ngay",
            "accent_color": ad_data.preferred_color or "#D4AF37"
        }

        svg_rendered = render_svg(SVG_CONTENT_RAW, svg_data)

        return cairosvg.svg2png(
            bytestring=svg_rendered.encode("utf-8"),
            output_width=1376,
            output_height=768
        )
    except Exception as e:
        logger.error(f"Fallback failed: {str(e)}")
        return b""