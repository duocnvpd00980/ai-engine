CANVAS_TEMPLATE = {
    "width": 1376,
    "height": 768,
    "layers": [
        {
            "type": "background",
            "color": "#00120a"
        },
        {
            "type": "image",
            "src": "{{ image_url }}",
            "x": 0,
            "y": 0,
            "w": 1376,
            "h": 768
        },
        {
            "type": "text",
            "content": "{{ main_title }}",
            "x": 80,
            "y": 120,
            "font_size": 72,
            "bold": True,
            "color": "#ffffff"
        },
        {
            "type": "text",
            "content": "{{ highlight_text }}",
            "x": 80,
            "y": 220,
            "font_size": 40,
            "bold": True,
            "color": "#07d76e"
        },
        {
            "type": "text",
            "content": "{{ sub_title }}",
            "x": 80,
            "y": 320,
            "font_size": 28,
            "color": "#cccccc"
        },
        {
            "type": "text",
            "content": "{{ cta_text }}",
            "x": 80,
            "y": 480,
            "font_size": 36,
            "bold": True,
            "color": "#07d76e"
        }
    ]
}