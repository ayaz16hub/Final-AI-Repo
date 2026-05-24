from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

import shutil
import os
import uuid

from ocr.extract_text import extract_text
from handwriting.generate_handwriting import generate_handwriting
from pdf_generator.make_pdf import make_pdf

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# folders
UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# static files
app.mount("/outputs", StaticFiles(directory="outputs"), name="outputs")


@app.get("/")
def home():
    return {"message": "Backend Running"}


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):

    try:

    

        unique_id = str(uuid.uuid4())

        temp_path = os.path.join(
            UPLOAD_FOLDER,
            f"{unique_id}_{file.filename}"
        )

        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        print("IMAGE SAVED")

        # OCR
        extracted_text = extract_text(temp_path)

        print("OCR DONE")

        # Handwriting image
        handwritten_image = generate_handwriting(
            extracted_text
        )

        print("HANDWRITING DONE")

        # PDF
        pdf_file = make_pdf(handwritten_image)

        print("PDF DONE")

        return {

            "success": True,

            "extracted_text": extracted_text,

            "image_url":
            "https://final-ai-handwriitng-caligraphy-backend.onrender.com/outputs/handwritten.png",

            "pdf_url":
            "https://final-ai-handwriitng-caligraphy-backend.onrender.com/outputs/final_output.pdf"
        }

    except Exception as e:

        print("ERROR:", str(e))

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )