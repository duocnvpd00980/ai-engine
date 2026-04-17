from pydantic import BaseModel, Field
from typing import Dict, Any, Optional


class AdRequest(BaseModel):
    # 1. Ý tưởng campaign
    request_text: str = Field(..., description="User campaign idea")

    # 2. Sản phẩm / dịch vụ
    service_info: Dict[str, Any] = Field(...)

    # 3. BRAND (bắt buộc giữ identity)
    brand_identity: Dict[str, Any] = Field(...)

    # 4. MARKETING TARGET (mở rộng)
    marketing_context: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Audience, goal, emotion"
    )

    # 5. VISUAL CONTROL (mở rộng cho Flux)
    visual_control: Optional[Dict[str, Any]] = Field(
        default=None,
        description="layout, lighting, composition"
    )

    # 6. OUTPUT CONTROL (tuỳ chọn nâng cao)
    output_control: Optional[Dict[str, Any]] = Field(
        default=None,
        description="format, size, ratio, platform"
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "brand_identity": {
                    "name": "CoinStrat",
                    "color": "#07d76e",
                    "logo": "https://www.coinstrat.com/logo.png",
                    "style": "modern fintech, crypto, high-tech financial platform"
                },
                "marketing_context": {
                    "industry": "crypto finance / digital asset platform",
                    "emotion": "trust, growth, financial freedom, opportunity",
                    "goal": "user acquisition / sign-up / deposit",
                    "target": "crypto investors, traders, passive income seekers"
                },
                "output_control": {
                    "platform": "facebook ads / google display",
                    "ratio": "16:9",
                    "format": "high conversion banner"
                },
                "request_text": "Tạo banner quảng cáo nền tảng tài chính crypto giúp người dùng đầu tư, vay và kiếm lợi nhuận từ tài sản số",
                "service_info": {
                    "name": "CoinStrat Platform",
                    "features": "crypto exchange, earn interest, borrowing, copy trading, dual investment, AI auto investing",
                    "core_value": "tối ưu lợi nhuận từ tài sản crypto với rủi ro thấp hơn ngân hàng truyền thống",
                    "pricing_model": "free signup + earn from yield products"
                },
                "visual_control": {
                    "layout": "dashboard UI + abstract financial network",
                    "lighting": "neon blue cyber glow, futuristic lighting",
                    "mood": "high-tech, trustworthy, global finance network",
                    "visual_elements": [
                    "crypto charts",
                    "network nodes",
                    "digital assets flow",
                    "mobile trading UI"
                    ]
                }
                }
        }
    }