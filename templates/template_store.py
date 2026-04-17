TEMPLATES = {
    "crypto_banner_01": {
        "metadata": {
            "name": "High Conversion Crypto Banner",
            "ratio": "16:9",
            "standard": "Google Ads / Social Header"
        },
        "settings": {
            "width": 1024,
            "height": 576,
            "brand_color": "#12c96d",
            "overlay_opacity": "#00000066"
        },
        "layers": [
            {
                "id": "bg_image",
                "type": "image",
                "src": "{{ image_url }}",
                "x": 0, "y": 0, "w": 1024, "h": 576,
                "z_index": 1
            },
            {
                "id": "badge_bg",
                "type": "shape",
                "shape_type": "rectangle",
                "x": 80, "y": 80,
                "width": 180, "height": 36,
                "background_color": "#12c96d",
                "border_radius": 20, 
                "z_index": 3
            },
            {
                "id": "badge_text",
                "type": "text",
                "content": "{{ badge_text }}",
                "x": 105, "y": 92,
                "font_size": 18,
                "bold": True,
                "color": "#000000",
                "z_index": 4
            },
            {
                "id": "main_title",
                "type": "text",
                "content": "{{ main_title }}",
                "x": 80, "y": 180,
                "font_size": 64,
                "bold": True,
                "color": "#ffffff",
                "line_height": 1.2,
                "z_index": 5
            },
            {
                "id": "sub_title",
                "type": "text",
                "content": "{{ sub_title }}",
                "x": 80, "y": 260,
                "font_size": 32,
                "bold": False,
                "color": "#12c96d",
                "z_index": 6
            },
            {
                "id": "cta_button",
                "type": "shape",
                "shape_type": "rectangle",
                "x": 80, "y": 360,
                "width": 250, "height": 60,
                "background_color": "#ffffff",
                "border_radius": 8,
                "z_index": 7
            },
            {
                "id": "cta_text",
                "type": "text",
                "content": "{{ cta_text }}",
                "x": 125, "y": 380,
                "font_size": 24,
                "bold": True,
                "color": "#000000",
                "z_index": 8
            },
            {
                "id": "footer_text",
                "type": "text",
                "content": "*T&C Apply",
                "x": 80, "y": 520,
                "font_size": 14,
                "color": "#94a3b8",
                "z_index": 9
            }
        ]
    }
}