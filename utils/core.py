import httpx
import base64
import logging
from typing import Any
from xml.sax.saxutils import escape

logger = logging.getLogger("Utils")



def safe_escape(text: Any) -> str:
    """Chuyển đổi sang string và escape các ký tự đặc biệt (&, <, >) cho XML/SVG."""
    if text is None: return ""
    return escape(str(text))

def format_banner_text(text: Any) -> str:
    """Làm sạch và viết hoa văn bản cho các tiêu đề mạnh mẽ."""
    return safe_escape(text).upper()