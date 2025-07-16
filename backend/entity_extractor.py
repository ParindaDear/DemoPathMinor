import spacy
import re

# โหลดโมเดลภาษาอังกฤษ spaCy
nlp_en = spacy.load("en_core_web_sm")


def extract_entities(text):
    results = []

    # วิเคราะห์ภาษาอังกฤษด้วย spaCy
    doc_en = nlp_en(text)
    for ent in doc_en.ents:
        # กรอง entity ที่ไม่น่าจะสมเหตุสมผล เช่น ตัวเลขยาวๆ ใน label DATE
        if ent.label_ == "DATE" and ent.text.isdigit() and len(ent.text) > 8:
            continue
        results.append({
            "text": ent.text,
            "label": ent.label_,
            "source": "spaCy-en"
        })

    # ตรวจหาเบอร์โทรศัพท์ด้วย regex
    phone_matches = re.findall(r"\b\d{9,11}\b", text)
    for m in phone_matches:
        results.append({
            "text": m,
            "label": "PHONE",
            "source": "regex"
        })

    return results