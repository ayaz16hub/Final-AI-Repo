from PIL import Image

def make_pdf(image_path):

    image = Image.open(image_path)

    pdf_path = "outputs/final_output.pdf"

    image.convert("RGB").save(pdf_path)

    return pdf_path