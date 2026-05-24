import time
import requests
import pytesseract
from PIL import Image
import firebase_admin
from firebase_admin import credentials, db
from io import BytesIO

# ---------------- Tesseract path ----------------
pytesseract.pytesseract.tesseract_cmd = r"D:\Flutter\Tesseract OCR\tesseract.exe"

# ---------------- Firebase init ----------------
cred = credentials.Certificate("firebase_key.json")

firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://YOUR_PROJECT.firebaseio.com/'
})

# ---------------- OCR FUNCTION ----------------
def run_ocr_from_url(image_url):
    response = requests.get(image_url)
    img = Image.open(BytesIO(response.content))
    text = pytesseract.image_to_string(img)
    return text

# ---------------- MAIN LOOP ----------------
def listen_for_requests():
    print("🚀 OCR Backend Started...")

    while True:
        ref = db.reference("ocr_requests")
        requests_data = ref.get()

        if requests_data:
            for key, value in requests_data.items():

                # only process pending requests
                if value.get("status") == "pending":

                    print("📷 Processing image...")

                    image_url = value.get("image_url")

                    try:
                        # OCR
                        text = run_ocr_from_url(image_url)

                        # save result
                        db.reference("ocr_results").push({
                            "text": text,
                            "image_url": image_url
                        })

                        # update status
                        db.reference("ocr_requests").child(key).update({
                            "status": "done"
                        })

                        print("✅ Done:", text)

                    except Exception as e:
                        db.reference("ocr_requests").child(key).update({
                            "status": "error"
                        })
                        print("❌ Error:", e)

        time.sleep(5)  # check every 5 seconds


# ---------------- RUN ----------------
if __name__ == "__main__":
    listen_for_requests()