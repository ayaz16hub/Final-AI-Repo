from PIL import Image, ImageDraw, ImageFont

def text_to_handwriting(text, output_path):

    img = Image.new("RGB", (1240, 1754), "white")
    draw = ImageDraw.Draw(img)

    # FIX: proper font path (NOT text)
    font = ImageFont.truetype("fonts/handwriting.ttf", 40)

    x, y = 50, 50

    for line in text.split("\n"):
        draw.text((x, y), line, fill="black", font=font)
        y += 60

    img.save(output_path)

    return output_path