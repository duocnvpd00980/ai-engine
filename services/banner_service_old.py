import os
import base64
import cairosvg
from render.svg_renderer import render_svg
from services.comfy_cloud import ComfyCloudService
# Import chính xác dictionary TEMPLATE_CONFIG và Key
from core.config import TEMPLATE_CONFIG, COMFY_API_KEY

comfy_service = ComfyCloudService(api_key=COMFY_API_KEY)

async def generate_banner(data):
    # Truy xuất đường dẫn từ dictionary
    workflow_path = TEMPLATE_CONFIG["WORKFLOW_PATH"]
    svg_path = TEMPLATE_CONFIG["SVG_TEMPLATE_PATH"]

    if not os.path.exists(workflow_path):
        raise FileNotFoundError(f"Không tìm thấy file: {workflow_path}")

    # 1. AI tạo ảnh nền
    image_bytes = await comfy_service.generate_image(workflow_path, {"6": data.highlight_text})
    
    # 2. Encode Base64
    base64_img = f"data:image/png;base64,{base64.b64encode(image_bytes).decode()}"

    # 3. Render SVG
    svg_content = render_svg(svg_path, {
        "image_url": base64_img,
        "brand_name": data.brand_name,
        "main_title": data.main_title,
        "highlight_text": data.highlight_text,
        "sub_title": data.sub_title,
        "accent_color": data.accent_color
    })

    # 4. Export PNG
    return cairosvg.svg2png(bytestring=svg_content.encode('utf-8'), output_width=1376, output_height=768)