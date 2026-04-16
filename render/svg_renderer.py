from jinja2 import Template

def render_svg(svg_content: str, context: dict) -> str:
    """
    svg_content: Chuỗi nội dung SVG đã đọc từ file
    context: Dictionary chứa data (brand_name, main_title,...)
    """
    try:
        # Tạo template từ chuỗi nội dung trong RAM
        template = Template(svg_content)
        # Render nội dung với các biến từ context
        return template.render(context)
    except Exception as e:
        print(f"❌ Lỗi Render Jinja2: {str(e)}")
        return svg_content # Trả về nội dung gốc nếu lỗi