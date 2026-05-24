from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import shutil
import uuid
import os

from services.ocr_service import extract_text_from_image
from services.handwriting_service import generate_handwriting_pdf


app = FastAPI()

# =========================
# BASE PATHS (RENDER SAFE)
# =========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")

# Create folders safely
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Mount static only if folder exists (extra safety)
if os.path.exists(OUTPUT_DIR):
  OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")
os.makedirs(OUTPUT_DIR, exist_ok=True)


# =========================
# ROUTES
# =========================

@app.get("/")
def home():
    return {"message": "AI Handwriting Backend Running"}


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        # Unique filename
        unique_name = f"{uuid.uuid4()}_{file.filename}"
        upload_path = os.path.join(UPLOAD_DIR, unique_name)

        # Save uploaded file
        with open(upload_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # OCR Extract
        extracted_text = extract_text_from_image(upload_path)

        # Generate handwriting PDF
        output_pdf = generate_handwriting_pdf(extracted_text)

        pdf_url = f"https://ai-handwritting.onrender.com/outputs/{output_pdf}"

        return JSONResponse({
            "success": True,
            "text": extracted_text,
            "pdf_url": pdf_url
        })

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": str(e)
            }
        )