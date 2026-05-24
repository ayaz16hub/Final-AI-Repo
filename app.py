from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

import shutil
import os

from ocr.extract_text import extract_text
from handwriting.generate_handwriting import generate_handwriting
from pdf_generator.make_pdf import make_pdf

app = FastAPI()

# outputs folder serve karne ke liye
app.mount("/outputs", StaticFiles(directory="outputs"), name="outputs")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.get("/")
def home():
    return {"message": "Backend Running"}

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    try:
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # optional processing
        text = extract_text(file_path)

        return {
            "status": "success",
            "filename": file.filename,
            "text": text
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))