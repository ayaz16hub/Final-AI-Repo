#!/usr/bin/env bash
# exit on error
set -o errexit

# پائتھن کی لائبریریز انسٹال کرنا
pip install -r requirements.txt

# لینوکس کے لیے ٹیسیریکٹ بائنری ڈاؤن لوڈ اور انسٹال کرنا
echo "Installing Tesseract OCR..."
mkdir -p bin
apt-get update && apt-get install -y tesseract-ocr