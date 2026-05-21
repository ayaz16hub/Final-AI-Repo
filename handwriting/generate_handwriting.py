from PIL import Image, ImageDraw, ImageFont
import textwrap
import os

OUTPUT_FOLDER = "outputs"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def generate_handwriting(text):

    # Create blank white page
    img = Image.new("RGB", (800, 1000), color="white")

    draw = ImageDraw.Draw(img)

    # Load handwriting font
    font = ImageFont.truetype("fonts/handwriting.ttf", 32)

    # Wrap text
    lines = textwrap.wrap(text, width=40)

    y_text = 50

    for line in lines:
        draw.text((50, y_text), line, fill="black", font=font)
        y_text += 50

    output_path = os.path.join(OUTPUT_FOLDER, "handwritten.png")

    img.save(output_path)

    return output_path