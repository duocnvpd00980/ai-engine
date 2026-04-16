import httpx
import urllib.parse

import httpx
import urllib.parse
import random

class PollinationsService:
    async def generate_image(self, prompt: str, width: int = 1376, height: int = 768):
        # 1. Encode prompt
        encoded_prompt = urllib.parse.quote(prompt)
        
        # 2. Tạo số ngẫu nhiên (seed) để tránh bị cache ảnh cũ
        seed = random.randint(0, 999999)
        
        # 3. SỬ DỤNG ENDPOINT PUBLIC (Thường không yêu cầu Key)
        # Thay 'gen.pollinations.ai' bằng 'image.pollinations.ai'
        url = (
            f"https://image.pollinations.ai/prompt/{encoded_prompt}"
            f"?width={width}"
            f"&height={height}"
            f"&model=flux"  # Bạn có thể thử đổi thành 'flux-pro' nếu có key, hoặc để 'flux' cho bản thường
            f"&seed={seed}"
            f"&nologo=true"
        )
        
        headers = {
            # Thử xóa Authorization header nếu bạn đang để trống hoặc để sai
            "Accept": "image/*",
            "User-Agent": "Mozilla/5.0" # Giả lập trình duyệt để tránh bị chặn
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers, timeout=60.0)
            
            if response.status_code == 200:
                return response.content
            elif response.status_code == 401:
                # Nếu vẫn lỗi 401, nghĩa là model 'flux' hiện tại đã bị khóa Premium
                # Thử bỏ tham số &model=flux để dùng model mặc định của họ
                fallback_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width={width}&height={height}&seed={seed}&nologo=true"
                response = await client.get(fallback_url, timeout=60.0)
                return response.content
            else:
                raise Exception(f"Lỗi hệ thống: Pollinations Error {response.status_code}")