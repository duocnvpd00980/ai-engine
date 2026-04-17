import httpx
import base64
import logging
import io
from typing import Any
from PIL import Image, ImageOps, ImageStat

logger = logging.getLogger("ImageUtils")

async def get_processed_logo(url: str) -> str:
    """
    Tải logo, tự động phát hiện nếu logo màu đen thì chuyển sang trắng.
    Trả về chuỗi Base64 Data URI.
    """
    if not url:
        return ""
    
    if url.startswith("data:image"):
        return url

    try:
        async with httpx.AsyncClient(verify=False) as client:
            response = await client.get(url, timeout=10.0)
            if response.status_code != 200:
                return ""
            
            img_content = response.content
            
            # Mở ảnh bằng Pillow để xử lý
            img = Image.open(io.BytesIO(img_content)).convert("RGBA")
            
            # 1. Kiểm tra độ sáng trung bình (Grayscale)
            # Chuyển tạm sang L (Luminance) để tính toán
            stat = ImageStat.Stat(img.convert("L"))
            brightness = stat.mean[0]
            
            # 2. Nếu logo quá tối (brightness < 50), tiến hành chuyển sang trắng
            if brightness < 50:
                logger.info(f"✨ Logo detected as dark ({brightness:.2f}). Converting to white...")
                
                # Tách kênh Alpha để giữ độ trong suốt
                r, g, b, alpha = img.split()
                
                # Tạo một ảnh màu trắng thuần cùng kích thước
                white_img = Image.new("RGB", img.size, (255, 255, 255))
                
                # Ghép ảnh trắng với kênh Alpha của logo gốc
                # Cách này giúp logo Đen -> Trắng mà vẫn giữ nguyên hình dạng, độ sắc nét
                img = Image.merge("RGBA", (*white_img.split(), alpha))
            
            # 3. Chuyển đổi kết quả cuối cùng sang Base64
            buffer = io.BytesIO()
            img.save(buffer, format="PNG") # Luôn dùng PNG để giữ độ trong suốt
            encoded_string = base64.b64encode(buffer.getvalue()).decode()
            
            return f"data:image/png;base64,{encoded_string}"

    except Exception as e:
        logger.error(f"❌ Error processing logo: {e}")
        return ""

def img_to_base64(image_bytes: bytes) -> str:
    """Chuyển bytes ảnh (từ Flux) sang Base64."""
    if not image_bytes:
        return ""
    encoded = base64.b64encode(image_bytes).decode()
    return f"data:image/png;base64,{encoded}"

async def get_image_as_base64(url: str) -> str:
    if not url: return ""
    
    try:
        async with httpx.AsyncClient(verify=False, timeout=10.0) as client:
            response = await client.get(url)
            if response.status_code != 200: return ""
            
            # Mở ảnh bằng Pillow
            img = Image.open(io.BytesIO(response.content)).convert("RGBA")
            data = img.getdata()

            new_data = []
            for item in data:
                # item là (R, G, B, A)
                # Nếu pixel có độ sáng thấp (gần đen) và không phải trong suốt
                # Ngưỡng (threshold) là 100 để lọc các màu xám đậm sang trắng
                if item[0] < 100 and item[1] < 100 and item[2] < 100 and item[3] > 0:
                    # Đổi thành màu trắng (255, 255, 255) giữ nguyên Alpha
                    new_data.append((255, 255, 255, item[3]))
                else:
                    new_data.append(item)

            img.putdata(new_data)
            
            # Lưu lại và encode
            buffer = io.BytesIO()
            img.save(buffer, format="PNG")
            encoded = base64.b64encode(buffer.getvalue()).decode()
            return f"data:image/png;base64,{encoded}"
            
    except Exception as e:
        logger.error(f"❌ Logo process error: {e}")
        return ""