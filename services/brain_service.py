import json
import logging
import asyncio
from openai import OpenAI
from models.ad_request import AdRequest
from core.config import VERCEL_API_KEY
from templates.prompt_campaign import build_campaign_prompt


class BrainService:
    def __init__(self):
        self.client = OpenAI(
            api_key=VERCEL_API_KEY,
            base_url="https://ai-gateway.vercel.sh/v1"
        )
        self.model = "openai/gpt-5.4"
        self.logger = logging.getLogger("BrainService")

    async def analyze_and_creative(self, ad_request: AdRequest):
        loop = asyncio.get_event_loop()

        # =========================
        # INPUT EXTRACTION
        # =========================
        service_info = ad_request.service_info
        brand_identity = ad_request.brand_identity or {}

        color = brand_identity.get("color", "#D4AF37")
        style = brand_identity.get("style", "luxury")

        # =========================
        # BUILD PROMPT
        # =========================
        prompt = build_campaign_prompt(
            request_text=ad_request.request_text,
            service_info=service_info,
            preferred_color=color,
            brand_identity=brand_identity,
            marketing_context=getattr(ad_request, "marketing_context", None),
            visual_control=getattr(ad_request, "visual_control", None)
        )

        try:
            response = await loop.run_in_executor(
                None,
                lambda: self.client.responses.create(
                    model=self.model,
                    input=prompt
                )
            )

            text = response.output[0].content[0].text
            text = text.replace("```json", "").replace("```", "").strip()

            data = json.loads(text)

            return {
                "image_prompt": data["image_prompt"],
                "main_title": data["main_title"],
                "sub_title": data["sub_title"],
                "highlight_text": data["highlight_text"],
                "cta_text": data["cta_text"],
                "accent_color": color,
                "style": style
            }

        except Exception as e:
            self.logger.error(f"Brain error: {e}")

            return {
                "image_prompt": f"Luxury cinematic scene with {color} lighting",
                "main_title": "Đẳng cấp nghỉ dưỡng",
                "sub_title": service_info.get("product_name", "Premium Service"),
                "highlight_text": "ƯU ĐÃI",
                "cta_text": "Xem ngay",
                "accent_color": color,
                "style": style
            }