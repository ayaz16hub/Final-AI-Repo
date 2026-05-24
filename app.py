from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware

import shutil
import os

from ocr import extract_text

app = FastAPI()

# CORS settings for Flutter connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Backend Running"}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Uploaded file is not an image.")

    # Temporarily save image for EasyOCR to read
    temp_path = f"temp_{file.filename}"
    try:
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # EasyOCR function call
        extracted_text = extract_text(temp_path)
        
        return {
            "success": True,
            "extracted_text": extracted_text,
            "image_url": "https://via.placeholder.com/150",
            "pdf_url": "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Delete temp file after processing
        if os.path.exists(temp_path):
            os.remove(temp_path)