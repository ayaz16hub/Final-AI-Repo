import easyocr
import os

os.environ["EASYOCR_MODULE_PATH"] = os.path.join(
    os.path.expanduser("~"),
    ".EasyOCR"
)

def extract_text(image_path):

    try:

        reader = easyocr.Reader(['en'], gpu=False)

        results = reader.readtext(image_path)

        text = ""

        for item in results:
            text += item[1] + " "

        return text.strip()

    except Exception as e:
        return f"OCR Error: {str(e)}"