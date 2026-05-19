from PIL import Image, ImageDraw, ImageFont

def image_to_pdf(text, output_path):

    img = Image.new("RGB", (1240, 1754), "white")
    draw = ImageDraw.Draw(img)

    font = ImageFont.truetype("fonts/handwriting.ttf", 40)

    x, y = 60, 60

    for line in text.split("\n"):
        draw.text((x, y), line, font=font, fill="black")
        y += 60

    img.save(output_path)

    return output_path