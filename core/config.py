import os
from pathlib import Path
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATE_DIR = BASE_DIR / "templates"
SVG_TEMPLATE_PATH = str(TEMPLATE_DIR / "gemini-svg.svg")

# Đọc sẵn nội dung SVG để dùng toàn cục
SVG_CONTENT_RAW = ""
if Path(SVG_TEMPLATE_PATH).exists():
    with open(SVG_TEMPLATE_PATH, "r", encoding="utf-8") as f:
        SVG_CONTENT_RAW = f.read()
    print(f"✅ DEBUG SUCCESS: Đã nạp nội dung SVG vào bộ nhớ.")
else:
    print(f"❌ DEBUG ERROR: Không tìm thấy file tại {SVG_TEMPLATE_PATH}")

# 3. Định nghĩa Dictionary TEMPLATE_CONFIG (Để fix lỗi NameError)
TEMPLATE_CONFIG = {
    "WORKFLOW_PATH": str(TEMPLATE_DIR / "workflow_api.json"),
    "SVG_TEMPLATE_PATH": str(TEMPLATE_DIR / "gemini-svg.svg"),
}

# 4. Định nghĩa các biến lẻ (Để các file khác import kiểu gì cũng chạy)
WORKFLOW_PATH = TEMPLATE_CONFIG["WORKFLOW_PATH"]
SVG_TEMPLATE_PATH = TEMPLATE_CONFIG["SVG_TEMPLATE_PATH"]
# Bổ sung vào cuối file core/config.py
GEMINI_API_KEY = "AQ.Ab8RN6JOsbKXG9mXJTmFEgA8_Wa5ReqUhvMII6jkNWLEWHHymA" # Thay bằng key của bạn
VERCEL_API_KEY = "vck_5UacjhI2NMS7o48iTNA19ghsJnvfTygfnLpVKbDpUa6siWIoFd1iq5jP"


# Kiểm tra file ngay khi khởi động
if not Path(SVG_TEMPLATE_PATH).exists():
    print(f"DEBUG ERROR: Không tìm thấy file tại -> {SVG_TEMPLATE_PATH}")
else:
    print(f"DEBUG SUCCESS: Đã tìm thấy file SVG.")
COMFY_API_KEY = "comfyui-78e9b0ef17abee9312df427664ad0bd517826e8e97e3dfd50885f114eebd2bd3"





#acomfyui-78e9b0ef17abee9312df427664ad0bd517826e8e97e3dfd50885f114eebd2bd3