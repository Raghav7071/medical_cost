import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# We can use a dummy response if no API key is provided, or try to use the API
def get_chatbot_response(prompt, api_key=None):
    if not api_key:
        api_key = os.getenv("GEMINI_API_KEY")
        
    if not api_key:
        return "Please set your Gemini API key in the sidebar to chat with the Medical Assistant. As a fallback, I am a simulated assistant. How can I help you with medical tourism today?"
        
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        system_prompt = "You are a professional Medical Tourism Assistant named MediGuide AI. You help patients with cost estimation, visa guidance, hospital selection, and general medical travel queries. Be polite, concise, and professional."
        response = model.generate_content(f"{system_prompt}\nUser: {prompt}\nAssistant:")
        return response.text
    except Exception as e:
        return f"Error connecting to AI: {str(e)}"
        
def get_symptom_analysis(symptoms, api_key=None):
    if not api_key:
        return {"Disease": "Unable to predict without API Key", "Department": "General", "Severity": "Unknown"}
        
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"Analyze these symptoms: {symptoms}. Provide a JSON response ONLY with keys: 'Disease' (most likely), 'Department' (medical department), and 'Severity' (Low, Medium, High)."
        response = model.generate_content(prompt)
        import json
        text = response.text.replace('```json','').replace('```','').strip()
        return json.loads(text)
    except:
        return {"Disease": "Diagnosis required", "Department": "General Consultation", "Severity": "Consult Doctor"}
