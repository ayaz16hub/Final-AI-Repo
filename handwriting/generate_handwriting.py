from PIL import Image, ImageDraw, ImageFont
import textwrap
import os
from datetime import datetime

OUTPUT_FOLDER = "outputs"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def generate_handwriting(text):

    # Page size
    img = Image.new("RGB", (800, 1000), color="white")
    draw = ImageDraw.Draw(img)

    # Fonts
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    font_path = os.path.join(BASE_DIR, "fonts", "handwriting.ttf")

    font = ImageFont.truetype(font_path, 32)

    header_font = ImageFont.truetype(font_path, 24)

    # Date + Day
    now = datetime.now()
    date_str = now.strftime("%d-%m-%Y")
    day_str = now.strftime("%A")

    # 🔵 Notebook margin lines
    draw.line([(100, 0), (100, 1000)], fill="blue", width=3)
    draw.line([(700, 0), (700, 1000)], fill="blue", width=3)

    # 🔴 Top red margin line
    draw.line([(40, 80), (760, 80)], fill="red", width=3)

    # Header text
    draw.text((50, 30), f"Date: {date_str}", fill="black", font=header_font)
    draw.text((600, 30), f"{day_str}", fill="black", font=header_font)

    # Wrap text
    lines = textwrap.wrap(text, width=38)

    # starting position
    x_text = 120
    y_text = 120

    line_height = 55  # spacing per line

    for line in lines:

        # 📘 horizontal notebook rule (light blue-gray)
        draw.line([(110, y_text + 35), (690, y_text + 35)], fill=(210, 210, 255), width=2)

        # ✍️ text on top of line
        draw.text((x_text, y_text), line, fill="black", font=font)

        y_text += line_height

    output_path = os.path.join(OUTPUT_FOLDER, "handwritten.png")
    img.save(output_path)

    return output_path