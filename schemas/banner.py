from pydantic import BaseModel, Field
from typing import Optional

class AdRequest(BaseModel):

    # 2. Thương hiệu: Nhận diện Brand (Dòng nhỏ trên cùng)
    brand_name: str = Field(
        default="NIKE LUXURY",
        description="Tên thương hiệu hoặc danh mục",
        example="COINSTRAT"
    )

    # 3. Tiêu đề chính: Dòng dẫn dắt (Font vừa, trắng)
    main_title: str = Field(
        default="BỘ SƯU TẬP MỚI 2026", 
        description="Thông điệp dẫn dắt (VD: PROFIT FROM, SIÊU PHẨM...)",
        example="PROFIT FROM"
    )

    # 4. Trọng tâm (Highlight): Nội dung quan trọng nhất (Font to, màu accent)
    highlight_text: str = Field(
        default="SALE 50%", 
        description="Nội dung to nhất (VD: CRYPTO FALLS, GIẢM 2TR)",
        example="CRYPTO FALLS"
    )

    # 5. Phụ đề: Thúc đẩy hành động hoặc thông tin thêm
    sub_title: str = Field(
        default="Dành cho 100 khách hàng đầu tiên", 
        description="Lời kêu gọi hoặc thông tin bổ trợ",
        example="2026 GUIDE"
    )

    # 6. Màu sắc chủ đạo: Điều khiển màu của Brand, Highlight, Nút và Viền
    accent_color: str = Field(
        default="#00FF88",
        description="Mã màu Hex (VD: #00FF88 xanh neon, #FF3333 đỏ)",
        example="#00FF88"
    )

    # Cấu hình Swagger UI hiển thị mẫu cực chuẩn
    model_config = {
        "json_schema_extra": {
            "example": {
                "brand_name": "TECH STORE",
                "main_title": "SIÊU PHẨM CÔNG NGHỆ",
                "highlight_text": "GIẢM 2TR",
                "sub_title": "Bảo hành 1 đổi 1 trong 12 tháng",
                "accent_color": "#00FF88"
            }
        }
    }