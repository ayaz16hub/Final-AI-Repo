from fastapi.staticfiles import StaticFiles
from pdf_generator.make_pdf import make_pdf
from handwriting.generate_handwriting import generate_handwriting
from fastapi import FastAPI, UploadFile, File
import shutil
import os

from ocr.extract_text import extract_text

app = FastAPI()

app.mount("/outputs", StaticFiles(directory="outputs"), name="outputs")

UPLOAD_FOLDER = "uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.get("/")
def home():
    return {"message": "Backend Running"}


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):

    try:

        file_path = os.path.join(
            UPLOAD_FOLDER,
            file.filename
        )

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        print("FILE SAVED")

        extracted_text = extract_text(file_path)

        print("OCR DONE")

        handwritten_image = generate_handwriting(
            extracted_text
        )

        print("HANDWRITING DONE")

        pdf_file = make_pdf(handwritten_image)

        print("PDF DONE")

        return {

            "message": "Success",

            "extracted_text": extracted_text,

            "image_url":
            "https://final-ai-handwriitng-caligraphy-backend.onrender.com/outputs/handwritten.png",

            "pdf_url":
            "https://final-ai-handwriitng-caligraphy-backend.onrender.com/outputs/final_output.pdf"
        }

    except Exception as e:

        print("ERROR:", str(e))

        return {
            "error": str(e)
        }