import json
import logging
import asyncio
import random
from typing import Dict, Any

from google import genai
from google.genai import types

from core.config import GEMINI_API_KEY
from models.ad_request import AdRequest


class BrainService:
    def __init__(self):
        self.client = genai.Client(api_key=GEMINI_API_KEY)
        self.model_id = "gemini-1.5-flash"
        self.logger = logging.getLogger("BrainService")

    # =========================
    # 🧠 SYSTEM INSTRUCTION
    # =========================
    def _build_system_instruction(self, ad_request: AdRequest) -> str:
        color = ad_request.preferred_color or "#D4AF37"
        membership = ad_request.user_profile.membership

        return f"""
ROLE: Senior Art Director & Performance Marketing Expert

MISSION:
Create a unified, high-end advertising concept with strong visual consistency.

CRITICAL RULES:

1. COLOR SYSTEM:
Primary color: {color}
- must dominate lighting, reflections, and environment
- apply in: ambient light, sky tone, water reflection, UI accents
- avoid conflicting colors

2. STYLE LOCK:
Luxury resort, cinematic, premium materials (glass, marble, gold)

3. COPYWRITING RULE:
- DO NOT use any personal names
- Use universal, aspirational messaging
- Optional: reference membership level ({membership})
- Keep headline short (max 6 words)

4. CONSISTENCY:
All elements must follow ONE unified visual theme
No randomness, no mixed styles

5. OUTPUT:
Return structured JSON only
"""

    # =========================
    # 🧠 SAFE JSON PARSE
    # =========================
    def _safe_parse_json(self, text: str) -> Dict[str, Any]:
        try:
            return json.loads(text)
        except Exception:
            try:
                cleaned = text.strip().replace("```json", "").replace("```", "")
                return json.loads(cleaned)
            except Exception as e:
                self.logger.error(f"JSON parse failed: {text}")
                raise e

    # =========================
    # 🧠 BUILD IMAGE PROMPT
    # =========================
    def _build_image_prompt(self, concept: Dict[str, Any], color: str) -> str:
        return f"""
{concept.get("visual_theme", "Luxury resort")} scene

ENVIRONMENT:
{concept.get("environment", "Beachfront villa with infinity pool and ocean view")}

LIGHTING:
{concept.get("lighting", f"Cinematic sunset lighting with {color} ambient glow, soft reflections, volumetric light")}

MATERIAL:
Glass, marble, water reflections, luxury textures

MOOD:
{concept.get("mood", "calm, exclusive, premium lifestyle")}

STYLE:
Ultra realistic, 8k, unreal engine 5, ray tracing

COLOR RULE:
Primary color {color} must dominate entire scene
No conflicting colors

NEGATIVE:
no cartoon, no low quality, no mixed color palette,
no oversaturated colors, no random lighting
"""

    # =========================
    # 🧠 MAIN FUNCTION
    # =========================
    async def analyze_and_creative(self, ad_request: AdRequest) -> Dict[str, Any]:
        loop = asyncio.get_event_loop()
        system_instr = self._build_system_instruction(ad_request)
        color = ad_request.preferred_color or "#D4AF37"

        response_schema = {
            "type": "object",
            "properties": {
                "visual_theme": {"type": "string"},
                "environment": {"type": "string"},
                "lighting": {"type": "string"},
                "mood": {"type": "string"},
                "main_title": {"type": "string"},
                "sub_title": {"type": "string"},
                "highlight_text": {"type": "string"},
                "cta_text": {"type": "string"}
            },
            "required": [
                "visual_theme",
                "environment",
                "lighting",
                "mood",
                "main_title",
                "sub_title",
                "highlight_text",
                "cta_text"
            ]
        }

        try:
            response = await loop.run_in_executor(
                None,
                lambda: self.client.models.generate_content(
                    model=self.model_id,
                    contents=f"""
CUSTOMER + PRODUCT DATA:
{ad_request.model_dump_json()}

TASK:
Create a HIGH-END advertising concept.

Focus:
- luxury perception
- emotional trigger
- premium lifestyle

DO NOT use personal names.
DO NOT generate image prompt.
Only return structured concept.
""",
                    config=types.GenerateContentConfig(
                        system_instruction=system_instr,
                        response_mime_type="application/json",
                        response_schema=response_schema,
                        temperature=0.7,
                    )
                )
            )

            concept = self._safe_parse_json(response.text)

            image_prompt = self._build_image_prompt(concept, color)

            return {
                "image_prompt": image_prompt,
                "main_title": concept["main_title"],
                "sub_title": concept["sub_title"],
                "highlight_text": concept["highlight_text"],
                "cta_text": concept["cta_text"],
                "accent_color": color
            }

        except Exception as e:
            self.logger.error(f"🔥 BrainService Error: {str(e)}")
            return self._get_fallback_data(ad_request)

    # =========================
    # 🧠 FALLBACK
    # =========================
    def _get_fallback_data(self, ad_request: AdRequest) -> Dict[str, Any]:
        color = ad_request.preferred_color or "#D4AF37"
        membership = ad_request.user_profile.membership

        titles = [
            "Trải nghiệm đẳng cấp thượng lưu",
            "Không gian nghỉ dưỡng hoàn hảo",
            "Chuẩn sống tinh hoa"
        ]

        subtitles = [
            f"Khám phá {ad_request.product_info.name}",
            f"Tận hưởng {ad_request.product_info.name}",
            "Không gian dành cho giới tinh hoa"
        ]

        highlights = [
            "ƯU ĐÃI ĐẶC QUYỀN",
            "LIMITED OFFER",
            f"EXCLUSIVE {membership.upper()}"
        ]

        ctas = [
            "Đặt ngay",
            "Khám phá ngay",
            "Xem chi tiết"
        ]

        image_prompt = f"""
Luxury beachfront villa at sunset

ENVIRONMENT:
Infinity pool, ocean view, palm trees

LIGHTING:
Cinematic sunset with {color} ambient glow,
soft reflections, volumetric light

MATERIAL:
Glass, marble, water reflections

MOOD:
Calm, premium, exclusive

STYLE:
Ultra realistic, 8k, unreal engine 5, ray tracing

COLOR RULE:
{color} dominant, no conflicting colors

NEGATIVE:
no cartoon, no low quality, no mixed color palette
"""

        return {
            "image_prompt": image_prompt,
            "main_title": random.choice(titles),
            "sub_title": random.choice(subtitles),
            "highlight_text": random.choice(highlights),
            "cta_text": random.choice(ctas),
            "accent_color": color
        }