import pytesseract
from PIL import Image
import pdfplumber
import os

def extract_text_from_image(image_path):
    try:
        text = pytesseract.image_to_string(Image.open(image_path))
        return text
    except Exception as e:
        return f"OCR Error: {str(e)}"

def extract_text_from_pdf(pdf_path):
    try:
        text = ""
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() + "\n"
        return text
    except Exception as e:
        return f"PDF Error: {str(e)}"

def analyze_medical_text(text):
    text = text.lower()
    keywords = {
        'Cardiology': ['heart', 'bypass', 'ecg', 'blood pressure', 'arrhythmia'],
        'Orthopedics': ['bone', 'fracture', 'joint', 'knee', 'spine', 'fusion'],
        'Oncology': ['tumor', 'cancer', 'chemo', 'malignant', 'carcinoma'],
        'Neurology': ['brain', 'nerve', 'seizure', 'migraine', 'spinal'],
        'Dental': ['tooth', 'cavity', 'implant', 'gum'],
    }
    
    detected_departments = []
    for dept, words in keywords.items():
        if any(word in text for word in words):
            detected_departments.append(dept)
            
    return list(set(detected_departments)) if detected_departments else ["General Medicine"]
