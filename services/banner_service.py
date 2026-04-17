import base64
import cairosvg
import logging
import time

from render.svg_renderer import render_svg
from services.brain_service import BrainService
from core.config import SVG_CONTENT_RAW
from services.image_service import ImageGenerationService
from utils.core import safe_escape, format_banner_text
from utils.image_utils import img_to_base64, get_image_as_base64

brain_service = BrainService()
image_service = ImageGenerationService()
logger = logging.getLogger("BannerService")

async def generate_banner(ad_data):
    start_time = time.time()
    try:
        logger.info("🚀 START BANNER GENERATION")

        # 1. 🧠 AI CONCEPT
        creative = await brain_service.analyze_and_creative(ad_data)
        
        # Kiểm tra fields bắt buộc
        required = ["image_prompt", "main_title", "sub_title", "highlight_text", "cta_text"]
        for field in required:
            if field not in creative: raise ValueError(f"Missing field: {field}")

        # 2. 🎨 IMAGE GENERATION (FLUX)
        image_bytes = await image_service.generate_flux_image(creative["image_prompt"])
        bg_base64 = img_to_base64(image_bytes)
        
        # 3. 🛠️ LOGO & BRAND IDENTITY
        logo_base64 = await get_image_as_base64(ad_data.brand_identity.get("logo", ""))
        brand = ad_data.brand_identity

        # 4. 🧩 SVG PREPARATION
        brand = ad_data.brand_identity
        svg_data = {
            "image_url": bg_base64,
            "logo_url": logo_base64,
            "brand_name": safe_escape(brand.get("name", "CoinStrat")),
            "accent_color": brand.get("color", "#07d76e"),
            "main_title": format_banner_text(creative["main_title"]),
            "highlight_text": format_banner_text(creative["highlight_text"]),
            "sub_title": safe_escape(creative["sub_title"]),
            "cta_text": safe_escape(creative["cta_text"]),
            "badge_text": format_banner_text(creative.get("badge_text", "ANNOUNCEMENT")),
            "stats_value": safe_escape(creative.get("stats_value", "+210.00% APY"))
        }

        # 5. 🖼️ RENDER SVG -> PNG
        svg_rendered = render_svg(SVG_CONTENT_RAW, svg_data)
        
        png_bytes = cairosvg.svg2png(
            bytestring=svg_rendered.encode("utf-8"),
            output_width=1376,
            output_height=768
        )

        logger.info(f"🎉 SUCCESS | Duration: {time.time() - start_time:.2f}s")
        return png_bytes

    except Exception as e:
        logger.exception("🔥 BANNER GENERATION FAILED")
        return await _fallback_banner(ad_data)

async def _fallback_banner(ad_data):
    """Tạo banner mặc định khi toàn bộ quy trình AI/Render gặp sự cố."""
    try:
        logger.warning("⚠️ USING FALLBACK BANNER")
        brand = ad_data.brand_identity
        
        # Vẫn cố gắng lấy logo cho fallback nếu có thể
        logo_url = await get_image_as_base64(brand.get("logo", ""))

        svg_data = {
            "image_url": "",
            "logo_url": logo_url,
            "brand_name": safe_escape(brand.get("name", "CoinStrat")),
            "main_title": "PREMIUM SOLUTION",
            "sub_title": "Tối ưu hóa tài sản số của bạn",
            "highlight_text": "JOIN US NOW",
            "cta_text": "Bắt đầu ngay",
            "accent_color": brand.get("color", "#07d76e"),
            "badge_text": "OFFER",
            "stats_value": "+100% Secure"
        }
        
        svg_rendered = render_svg(SVG_CONTENT_RAW, svg_data)
        return cairosvg.svg2png(bytestring=svg_rendered.encode("utf-8"))
    except:
        return b"" # Trả về rỗng nếu cả fallback cũng chết