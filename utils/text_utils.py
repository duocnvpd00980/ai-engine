from xml.sax.saxutils import escape
from typing import Any

def safe_xml_escape(text: Any) -> str:
    """Chống lỗi ParseError cho SVG."""
    if text is None: return ""
    return escape(str(text))

def format_upper(text: Any) -> str:
    """Viết hoa và làm sạch text."""
    return safe_xml_escape(text).upper()