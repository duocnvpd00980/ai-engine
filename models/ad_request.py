from pydantic import BaseModel, Field
from typing import Optional, List

class UserProfile(BaseModel):
    name: str = Field(..., example="Nguyễn Văn Được")
    gender: str = Field(default="male", example="male")
    interests: List[str] = Field(default=[], example=["Nghỉ dưỡng", "Kiến trúc", "Golf"])
    membership: str = Field(default="Standard", example="Diamond")

class ProductInfo(BaseModel):
    name: str = Field(..., example="The Ocean Villas")
    features: str = Field(..., example="Biệt thự hướng biển, hồ bơi riêng, dịch vụ quản gia 24/7")
    price: Optional[str] = Field(None, example="Từ 15.000.000đ/đêm")

class AdRequest(BaseModel):
    brand_name: str = Field(default="SUNSET RESORT", example="MARINA BAY SIDE")
    user_profile: UserProfile
    product_info: ProductInfo
    
    # Màu sắc bám theo yêu cầu User
    preferred_color: Optional[str] = Field(
        None, 
        description="Mã màu Hex người dùng muốn (ví dụ: #008080 cho màu xanh mòng két)",
        example="#008080" 
    )
    style_tone: str = Field(
        default="Elegant", 
        description="Phong cách: Minimalist, Bold, Elegant, hoặc Vintage",
        example="Elegant"
    )
    
    request_text: Optional[str] = Field(
        None, 
        example="Tạo banner quảng cáo biệt thự nghỉ dưỡng, màu sắc sang trọng, bám theo tông xanh của biển"
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "brand_name": "MARINA BAY SIDE",
                "user_profile": {
                    "name": "Anh Được",
                    "gender": "male",
                    "interests": ["Đầu tư", "Du lịch hạng sang"],
                    "membership": "Diamond"
                },
                "product_info": {
                    "name": "Panorama Suite",
                    "features": "View toàn cảnh vịnh Đà Nẵng, nội thất nhập khẩu Ý",
                    "price": "Giá ưu đãi hội viên"
                },
                "preferred_color": "#008080", # Màu xanh Teal sang trọng
                "style_tone": "Elegant",
                "request_text": "Tạo banner giới thiệu căn hộ cao cấp, phong cách thượng lưu, tông màu xanh biển chủ đạo"
            }
        }
    }