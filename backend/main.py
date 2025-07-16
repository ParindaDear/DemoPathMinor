from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from ocr import extract_text_from_image
from pdf_reader import extract_text_from_pdf
import shutil
import os
from entity_extractor import extract_entities

from fpdf import FPDF
from fastapi.responses import FileResponse

# func ตัดข้อความเป็นบรรทัดย่อยตามความกว้างของหน้า
def split_text_to_lines(pdf: FPDF, text: str, max_width: float):
    words = text.split()
    lines = []
    current_line = ""

    for word in words:
        test_line = f"{current_line} {word}".strip()
        if pdf.get_string_width(test_line) <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)
    return lines

# func สร้าง PDF รายงาน พร้อมตัดข้อความ entity ที่ยาวเกินขอบขวา
def generate_report_pdf(text: str, entities: list, output_path: str):
    pdf = FPDF()
    pdf.add_page()

    font_path = os.path.join("fonts", "THSarabunNew.ttf")
    pdf.add_font("THSarabun", "", font_path, uni=True)
    pdf.set_font("THSarabun", size=14)

    available_width = pdf.w - 2 * pdf.l_margin

    # ส่วน Original Text
    pdf.cell(0, 10, "Original Text:", ln=True)
    original_lines = split_text_to_lines(pdf, text, max_width=available_width)
    for line in original_lines:
        pdf.cell(w=available_width, h=10, txt=line, ln=True)

    # เว้นบรรทัด
    pdf.ln(10)
    pdf.cell(0, 10, "Entities:", ln=True)

    # ส่วน Entities
    for entity in entities:
        line = f"{entity['label']}: {entity['text']}"
        entity_lines = split_text_to_lines(pdf, line, max_width=available_width)
        for l in entity_lines:
            pdf.cell(w=available_width, h=10, txt=l, ln=True)

    pdf.output(output_path)


# ----------------------------- FASTAPI -----------------------------
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TextRequest(BaseModel):
    text: str

@app.post("/upload/")
async def upload(file: UploadFile = File(...)):
    file_path = f"temp/{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    if file.filename.endswith(".pdf"):
        text = extract_text_from_pdf(file_path)
    else:
        text = extract_text_from_image(file_path)

    entities = extract_entities(text)

    report_path = f"temp/report_{file.filename}.pdf"
    generate_report_pdf(text, entities, report_path)

    os.remove(file_path)
    return {
        "text": text,
        "entities": entities,
        "report_url": f"/report/{os.path.basename(report_path)}"
    }

@app.post("/analyze/")
async def analyze(input: TextRequest):
    entities = extract_entities(input.text)
    return {"entities": entities}

@app.get("/report/{filename}")
async def download_report(filename: str):
    report_path = f"temp/{filename}"
    return FileResponse(report_path, media_type="application/pdf", filename=filename)
