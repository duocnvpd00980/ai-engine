import httpx
import base64

async def image_url_to_base64(url: str) -> str:
    if not url or not url.startswith("http"):
        return ""

    async with httpx.AsyncClient() as client:
        try:
            # Tải ảnh với timeout 10 giây
            response = await client.get(url, timeout=10.0)
            if response.status_code == 200:
                # Xác định định dạng ảnh (png, jpg, ...)
                content_type = response.headers.get("Content-Type", "image/png")
                # Mã hóa không chứa ký tự xuống dòng (\n)
                encoded_body = base64.b64encode(response.content).decode("utf-8")
                # Trả về full chuỗi data URI
                return f"data:{content_type};base64,{encoded_body}"
        except Exception as e:
            print(f"Lỗi tải ảnh: {e}")
            return ""
    return ""