FROM python:3.11

RUN apt-get update && apt-get install -y tesseract-ocr

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

EXPOSE 10000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "10000"]