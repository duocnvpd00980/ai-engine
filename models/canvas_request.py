from pydantic import BaseModel, Field, model_validator
from typing import Dict, Any


class CanvasRequest(BaseModel):
    template_id: str = Field(
        default="crypto_banner_01",
        description="ID của template"
    )

    data: Dict[str, Any] = Field(
        default_factory=lambda: {
            "image_url": "https://fastly.picsum.photos/id/77/450/300.jpg?hmac=V_LawevwSaVitpQs2t7AnuBi84UPSNl1Qp3PmKkmaXc",
            "highlight_text": "ANNOUNCEMENT",
            "main_title": "COPY TRADE SMARTER",
            "sub_title": "FOLLOW TOP TRADERS",
            "cta_text": "START NOW",
            "badge_text": "HOT DEAL"
        },
        description="Dữ liệu dynamic"
    )

    @model_validator(mode="after")
    def check_required_fields(self):
        required_fields = [
            "image_url",
            "main_title",
            "highlight_text",
            "sub_title",
            "cta_text",
            "badge_text"
        ]

        missing = [k for k in required_fields if not self.data.get(k)]

        if missing:
            print(f"⚠️ Missing fields: {missing}")

        return self

    model_config = {
        "json_schema_extra": {
            "example": {
                "template_id": "crypto_banner_01",
                "data": {
                    "image_url": "https://fastly.picsum.photos/id/77/450/300.jpg?hmac=V_LawevwSaVitpQs2t7AnuBi84UPSNl1Qp3PmKkmaXc",
                    "highlight_text": "ANNOUNCEMENT",
                    "main_title": "COPY TRADE SMARTER",
                    "sub_title": "FOLLOW TOP TRADERS",
                    "cta_text": "START NOW",
                    "badge_text": "HOT DEAL"
                }
            }
        }
    }