from fastapi import FastAPI, UploadFile, File #นำเข้า FastAPI และ func สำหรับรับไฟล์ upload
from fastapi.middleware.cors import CORSMiddleware
from ocr import extract_text_from_image       
from pdf_reader import extract_text_from_pdf  
import shutil #ใช้สำหรับการจัดการไฟล์ระดับสูง
import os     #ใช้สำหรับทำงานกับ os

app = FastAPI() #สร้าง FastAPI app

#อนุญาตให้ React frontend เรียก API ได้
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # frontend ของ Vite
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#กำหนด route /upload/ เป็น HTTP POST สำหรับรับไฟล์
@app.post("/upload/")
async def upload(file: UploadFile =  File(...)):
    file_path = f"temp/{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    if file.filename.endswith(".pdf"):
        text = extract_text_from_pdf(file_path) #จะเรียก func extract_text_from_pdf() เพื่อดึงข้อความจาก pdf
        
    else:
        text = extract_text_from_image(file_path)
    
    os.remove(file_path)  #ลบไฟล์ทิ้งหลังจากประมวลผลเสร็จ (ไม่ให้รกเครื่อง, ไม่ให้เกิด os error)
    return {"text": text} #ส่งข้อความดิบกลับไปยัง frontend ในรูปแบบ JSON