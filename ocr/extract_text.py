import easyocr

reader = easyocr.Reader(['en'])

def extract_text(image_path):

    results = reader.readtext(image_path)

    text = ""

    for item in results:
        text += item[1] + " "

    return text