import easyocr
import os

# Render server par permissions error se bachne ke liye path config
os.environ["EASYOCR_MODULE_PATH"] = os.path.join(os.path.expanduser("~"), ".EasyOCR")

# gpu=False lagana zaroori hai kyunki Render free tier par GPU nahi deta
reader = easyocr.Reader(['en'], gpu=False)

def extract_text(image_path):
    try:
        results = reader.readtext(image_path)
        text = ""
        for item in results:
            text += item[1] + " "
        return text.strip() if text.strip() else "No text found in image."
    except Exception as e:
        return f"OCR Error: {str(e)}"