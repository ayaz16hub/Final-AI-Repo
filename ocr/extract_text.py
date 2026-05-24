import easyocr
import os

os.environ["EASYOCR_MODULE_PATH"] = os.path.join(
    os.path.expanduser("~"),
    ".EasyOCR"
)

reader = easyocr.Reader(['en'], gpu=False)

def extract_text(image_path):
    try:
        results = reader.readtext(image_path)

        text = ""

        for item in results:
            text += item[1] + " "

        return text.strip()

    except Exception as e:
        return f"OCR Error: {str(e)}"