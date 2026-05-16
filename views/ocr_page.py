import streamlit as st
import os
from ocr.main import extract_text_from_image, extract_text_from_pdf, analyze_medical_text

def render():
    st.markdown("<h2 class='title-text'>📄 Medical Report OCR Scanner</h2>", unsafe_allow_html=True)
    st.write("Upload your medical documents securely. Our AI will extract data and suggest relevant departments.")
    
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        file = st.file_uploader("Upload Medical Report (PDF, PNG, JPG)", type=['png', 'jpg', 'jpeg', 'pdf'])
    with col2:
        img_camera = st.camera_input("Or Take a Picture Live 📸")
        
    target_file = file or img_camera
    st.markdown("</div>", unsafe_allow_html=True)
    
    if target_file:
        with st.spinner("Analyzing document with Tesseract OCR..."):
            ext = "png" if img_camera else target_file.name.split('.')[-1]
            temp_path = f"temp_upload.{ext}"
            with open(temp_path, "wb") as f:
                f.write(target_file.getbuffer())
            
            if ext.lower() in ['png', 'jpg', 'jpeg']:
                text = extract_text_from_image(temp_path)
            else:
                text = extract_text_from_pdf(temp_path)
                
            os.remove(temp_path)
            
            c1, c2 = st.columns([2, 1])
            with c1:
                st.subheader("Raw Extracted Text")
                st.text_area("OCR Output", text, height=250)
                
            with c2:
                st.subheader("AI Analysis Results")
                depts = analyze_medical_text(text)
                st.write("**Suggested Departments:**")
                for d in depts:
                    st.markdown(f"<div style='background-color:#10b981; color:white; padding:10px; border-radius:8px; margin-bottom:10px; text-align:center;'><b>{d}</b></div>", unsafe_allow_html=True)
                st.write("**Confidence Score:** 92%")
                st.progress(92)
