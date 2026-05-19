from pickle import APPEND

from fastapi import FastAPI, File, UploadFile
import shutil
import os
import time

from services.ocr_service import extract_text
from services.handwriting_service import text_to_handwriting
from services.pdf_service import image_to_pdf


from fastapi.staticfiles import StaticFiles



from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.mount("/outputs", StaticFiles(directory="outputs"), name="outputs")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.get("/")

def home():
    return {"message": "Backend Running Successfully 🚀"}


@app.post("/process-file/")
async def process_file(file: UploadFile = File(...)):

    try:
        print("1️⃣ Request received")

        file_path = f"{UPLOAD_FOLDER}/{file.filename}"

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        print("2️⃣ File saved")

        text = extract_text(file_path)
        print("3️⃣ OCR done")

        hw_image = f"{OUTPUT_FOLDER}/handwritten_{int(time.time())}.png"
        text_to_handwriting(text, hw_image)
        print("4️⃣ handwriting done")

        pdf_path = f"{OUTPUT_FOLDER}/final.pdf"
        image_to_pdf(hw_image, pdf_path)
        print("5️⃣ PDF done")

        return {
           
            "text": text,
            "image": f"http://192.168.100.3:8000/{hw_image}",
            "pdf": f"http://192.168.100.3:8000/{pdf_path}"
        }

    except Exception as e:
        print("🔥 ERROR:", str(e))
        return {"error": str(e)}