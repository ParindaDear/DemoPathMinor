import pdfplumber

# Learning from The data school website
def extract_text_from_pdf(pdf_path):
    text = '' # ตัวแปร text เก็บข้อความที่ดึงออกมาจากแต่ละหน้า
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() #ดึงข้อความจากแต่ละหน้าโดยใช้ page.extract_text() แล้วนำมาต่อกันในตัวแปร text
    return text