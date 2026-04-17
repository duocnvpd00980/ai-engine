from PIL import Image, ImageDraw, ImageFont, ImageColor
import requests
from io import BytesIO
import re
import os
from PIL import ImageFont

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
FONT_DIR = os.path.join(BASE_DIR, "assets", "fonts", "roboto")


# --- HELPER: COLOR ---
def get_color(color_str):
    if not color_str:
        return (255, 255, 255, 255)

    color_str = color_str.lstrip('#')

    # RGBA (8 ký tự)
    if len(color_str) == 8:
        r = int(color_str[0:2], 16)
        g = int(color_str[2:4], 16)
        b = int(color_str[4:6], 16)
        a = int(color_str[6:8], 16)
        return (r, g, b, a)

    try:
        rgb = ImageColor.getrgb(f"#{color_str}")
        return rgb + (255,)
    except:
        return (255, 255, 255, 255)


# --- FONT ---
def load_font(size, bold=False):
    try:
        font_file = "Roboto-Bold.ttf" if bold else "Roboto-Medium.ttf"
        font_path = os.path.join(FONT_DIR, font_file)

        print("━━━━━━━━ FONT DEBUG ━━━━━━━━")
        print("📁 FONT_DIR:", FONT_DIR)
        print("📄 FONT FILE:", font_file)
        print("📌 FULL PATH:", font_path)
        print("✔ EXISTS:", os.path.exists(font_path))

        font = ImageFont.truetype(font_path, int(size))

        print("✅ FONT LOADED OK:", font)

        return font

    except Exception as e:
        print("❌ FONT ERROR:", e)
        print("⚠️ FALLBACK TO DEFAULT FONT")

        return ImageFont.load_default()

# --- IMAGE ---
def load_image(src, w=None, h=None):
    if not src or "{{" in src:
        print(f"⚠️ INVALID SRC: {src}")
        return None

    try:
        print(f"🌐 LOAD IMAGE: {src}")

        headers = {
            "User-Agent": "Mozilla/5.0",
            "Accept": "image/*"
        }

        if src.startswith("http"):
            res = requests.get(src, timeout=10, headers=headers)

            print("👉 STATUS:", res.status_code)
            print("👉 SIZE:", len(res.content))

            if res.status_code != 200 or len(res.content) < 1000:
                print("❌ INVALID IMAGE RESPONSE")
                return None

            img = Image.open(BytesIO(res.content))
        else:
            img = Image.open(src)

        img = img.convert("RGBA")

        final_w = int(w) if w else img.width
        final_h = int(h) if h else img.height

        img = img.resize((final_w, final_h), Image.Resampling.LANCZOS)
        return img

    except Exception as e:
        print(f"❌ IMAGE ERROR: {e}")
        return None


# --- FIX VARS ---
def replace_vars(text, data):
    if not text or not isinstance(text, str):
        return text

    def repl(match):
        key = match.group(1).strip()
        value = data.get(key)

        if value is None:
            print(f"⚠️ Missing key: {key}")
            return f"[{key}]"

        return str(value)

    return re.sub(r"\{\{\s*(.*?)\s*\}\}", repl, text)


# --- MAIN RENDER ---
def render_canvas(template: dict, data: dict):

    # ✅ FIX: đọc đúng settings
    settings = template.get("settings", {})
    width = settings.get("width", 1024)
    height = settings.get("height", 576)

    print("📦 DATA:", data)
    print(f"📐 SIZE: {width}x{height}")

    # Canvas
    canvas = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(canvas)

    # Layers
    layers = template.get("layers", [])
    layers.sort(key=lambda x: x.get("z_index", 0))

    for layer in layers:
        l_type = layer.get("type")
        x = int(layer.get("x", 0))
        y = int(layer.get("y", 0))

        # --- IMAGE ---
        if l_type == "image":
            src = replace_vars(layer.get("src", ""), data)
            print("👉 FINAL SRC:", src)

            img_w = layer.get("width", layer.get("w"))
            img_h = layer.get("height", layer.get("h"))

            img = load_image(src, img_w, img_h)

            if img:
                canvas.paste(img, (x, y), img)
            else:
                print(f"⚠️ IMAGE NOT LOADED: {src}")

        # --- SHAPE ---
        elif l_type == "shape":
            w = int(layer.get("width", layer.get("w", 0)))
            h = int(layer.get("height", layer.get("h", 0)))
            color = get_color(layer.get("background_color", "#ffffff"))
            radius = int(layer.get("border_radius", 0))

            draw.rounded_rectangle(
                [x, y, x + w, y + h],
                radius=radius,
                fill=color
            )

        # --- TEXT ---
        elif l_type == "text":
            content = replace_vars(layer.get("content", ""), data)

            if not content:
                print(f"⚠️ EMPTY TEXT at ({x},{y})")
                continue

            font_size = int(layer.get("font_size", 30))
            is_bold = layer.get("bold", False)
            font = load_font(font_size, is_bold)
            color = get_color(layer.get("color", "#ffffff"))

            draw.text((x, y), content, fill=color, font=font)

        else:
            print(f"⚠️ UNKNOWN TYPE: {l_type}")

    return canvas