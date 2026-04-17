import os
import logging
import asyncio
import base64
from openai import OpenAI
from core.config import VERCEL_API_KEY

client = OpenAI(
    api_key=VERCEL_API_KEY,
    base_url="https://ai-gateway.vercel.sh/v1"
)


class ImageGenerationService:
    def __init__(self):
        self.logger = logging.getLogger("ImageService")

    async def generate_flux_image(self, prompt: str) -> bytes:
        try:
            loop = asyncio.get_event_loop()

            response = await loop.run_in_executor(
                None,
                lambda: client.images.generate(
                    model="bfl/flux-pro-1.1",
                    prompt=prompt,
                    size="1024x1024"
                )
            )

            data = response.data[0]

            # ✅ CHỈ NHẬN BASE64 → CONVERT THÀNH BYTES
            if hasattr(data, "b64_json") and data.b64_json:
                return base64.b64decode(data.b64_json)

            raise ValueError("No image data returned")

        except Exception as e:
            self.logger.error(f"🔥 Lỗi tạo ảnh Flux: {str(e)}")
            return None