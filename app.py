from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# فلٹر ایپ کے کنکشن کے لیے CORS اوپن کرنا
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "AI Handwriting Backend is Running Successfully!"}

@app.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    # 1. فائل ٹائپ کو بالکل سیفلی چیک کریں
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="اپلوڈ کی گئی فائل امیج نہیں ہے۔")

    try:
        # 🟢 کوئی عارضی فائل ہارڈ ڈسک پر نہیں بنے گی! 
        # ڈائریکٹ ریم (Memory) سے بائٹس ریڈ کرنا تاکہ پرمیشن ایرر نہ آئے
        file_bytes = await file.read()
        
        if not file_bytes:
            raise HTTPException(status_code=400, detail="فائل کا ڈیٹا خالی ہے۔")

        # ٹیسٹ آؤٹ پٹ جو فلٹر اسکرین پر لازمی دکھنا چاہیے
        return {
            "success": True,
            "extracted_text": "مبارک ہو! لائیو سرور نے بغیر کسی لوکل فائل کے ڈیٹا ریم میں پڑھ لیا ہے۔",
            "image_url": "https://via.placeholder.com/150",
            "pdf_url": "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf"
        }

    except Exception as e:
        # اگر کوئی بھی اندرونی مسئلہ آئے گا تو وہ یہاں سے فلٹر کو صاف نظر آئے گا
        raise HTTPException(status_code=500, detail=f"بیک اینڈ پروسیسنگ ایرر: {str(e)}")