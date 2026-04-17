from pydantic import BaseModel, Field, model_validator
from typing import Dict, Any


class CanvasRenderRequest(BaseModel):

    # 👉 TEMPLATE DEFAULT (giống crypto_banner_01)
    template: Dict[str, Any] = Field(
        default_factory=lambda: {
            "settings": {
                "width": 1024,
                "height": 576
            },
            "layers": [
                {
                    "type": "image",
                    "src": "{{ image_url }}",
                    "x": 0, "y": 0, "w": 1024, "h": 576,
                    "z_index": 1
                },
                {
                    "type": "shape",
                    "x": 0, "y": 0,
                    "width": 1024, "height": 576,
                    "background_color": "#00000066",
                    "z_index": 2
                },
                {
                    "type": "shape",
                    "x": 80, "y": 80,
                    "width": 180, "height": 36,
                    "background_color": "#12c96d",
                    "border_radius": 20,
                    "z_index": 3
                },
                {
                    "type": "text",
                    "content": "{{ badge_text }}",
                    "x": 105, "y": 92,
                    "font_size": 18,
                    "bold": True,
                    "color": "#000000",
                    "z_index": 4
                },
                {
                    "type": "text",
                    "content": "{{ main_title }}",
                    "x": 80, "y": 180,
                    "font_size": 64,
                    "bold": True,
                    "color": "#ffffff",
                    "z_index": 5
                },
                {
                    "type": "text",
                    "content": "{{ sub_title }}",
                    "x": 80, "y": 260,
                    "font_size": 32,
                    "color": "#12c96d",
                    "z_index": 6
                },
                {
                    "type": "shape",
                    "x": 80, "y": 360,
                    "width": 250, "height": 60,
                    "background_color": "#ffffff",
                    "border_radius": 8,
                    "z_index": 7
                },
                {
                    "type": "text",
                    "content": "{{ cta_text }}",
                    "x": 125, "y": 380,
                    "font_size": 24,
                    "bold": True,
                    "color": "#000000",
                    "z_index": 8
                }
            ]
        },
        description="Template JSON"
    )

    # 👉 DATA DEFAULT
    data: Dict[str, Any] = Field(
        default_factory=lambda: {
            "image_url": "https://picsum.photos/1024/576",
            "highlight_text": "ANNOUNCEMENT",
            "main_title": "COPY TRADE SMARTER",
            "sub_title": "FOLLOW TOP TRADERS",
            "cta_text": "START NOW",
            "badge_text": "HOT DEAL"
        },
        description="Dynamic data"
    )

    # 👉 VALIDATOR
    @model_validator(mode="after")
    def check_required_fields(self):
        required_fields = [
            "image_url",
            "main_title",
            "sub_title",
            "cta_text",
            "badge_text"
        ]

        missing = [k for k in required_fields if not self.data.get(k)]

        if missing:
            print(f"⚠️ Missing fields: {missing}")

        return self

    # 👉 SWAGGER EXAMPLE
    model_config = {
    "json_schema_extra": {
        "example": {
            "template": {
                "settings": {
                    "width": 1024,
                    "height": 576
                },
                "layers": [
                    {
                        "type": "image",
                        "src": "{{ image_url }}",
                        "x": 0, "y": 0, "w": 1024, "h": 576
                    },
                    {
                        "type": "text",
                        "content": "{{ badge_text }}",
                        "x": 105,
                        "y": 92,
                        "font_size": 18,
                        "bold": True,
                        "color": "#000000"
                    },
                    {
                        "type": "text",
                        "content": "{{ main_title }}",
                        "x": 80,
                        "y": 180,
                        "font_size": 64,
                        "bold": True,
                        "color": "#ffffff"
                    },
                    {
                        "type": "text",
                        "content": "{{ sub_title }}",
                        "x": 80,
                        "y": 260,
                        "font_size": 32,
                        "color": "#12c96d"
                    },
                    {
                        "type": "shape",
                        "x": 80,
                        "y": 360,
                        "width": 250,
                        "height": 60,
                        "background_color": "#ffffff"
                    },
                    {
                        "type": "text",
                        "content": "{{ cta_text }}",
                        "x": 125,
                        "y": 380,
                        "font_size": 24,
                        "bold": True,
                        "color": "#000000"
                    }
                ]
            },
            "data": {
                "image_url": "https://picsum.photos/1024/576",
                "badge_text": "HOT",
                "main_title": "HELLO WORLD",
                "sub_title": "TEST",
                "cta_text": "CLICK"
            }
        }
    }
}