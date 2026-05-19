from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import uuid

def generate_handwriting_pdf(text):

    filename = f"{uuid.uuid4()}.pdf"

    output_path = f"outputs/{filename}"

    c = canvas.Canvas(output_path, pagesize=letter)

    y = 750

    for line in text.split("\n"):

        c.drawString(50, y, line)

        y -= 20

        if y < 50:
            c.showPage()
            y = 750

    c.save()

    return filename