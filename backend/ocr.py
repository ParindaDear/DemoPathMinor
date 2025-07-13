from PIL import Image # นำเข้าโมดูล Image จาก library Pillow ซึ่งเป็น library สำหรับการจัดการและประมวลผลรูปภาพ
import pytesseract #นำเข้า library ที่ช่วยแปลงข้อความจากภาพ (OCR)

def extract_text_from_image(image_path):
    text = pytesseract.image_to_string(Image.open(image_path), lang='eng+tha')
    return text