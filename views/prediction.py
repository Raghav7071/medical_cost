import streamlit as st
import pandas as pd
import joblib
import time
import plotly.express as px
from datetime import datetime
from database import save_prediction
from utils.helpers import convert_currency, generate_pdf_report

@st.cache_resource
def load_pipelines():
    try:
        models = {
            'Treatment_Cost': joblib.load('models/treatment_cost_pipeline.pkl'),
            'Travel_Cost': joblib.load('models/travel_cost_pipeline.pkl'),
            'Stay_Cost': joblib.load('models/stay_cost_pipeline.pkl'),
            'Medicine_Cost': joblib.load('models/medicine_cost_pipeline.pkl'),
            'Total_Cost': joblib.load('models/total_cost_pipeline.pkl')
        }
        categories = joblib.load('models/categories.pkl')
        return models, categories
    except Exception as e:
        return None, None

def render():
    st.markdown("<h2 class='title-text'>💡 Smart Cost Prediction Engine</h2>", unsafe_allow_html=True)
    models, categories = load_pipelines()
    
    if not models or not categories:
        st.error("ML Models are missing. Please wait for train_model.py to finish generating them.")
        return
        
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    with st.form("predict_form"):
        col1, col2 = st.columns(2)
        with col1:
            disease = st.selectbox("Disease/Condition", categories['Disease'])
            country = st.selectbox("Target Country", categories['Country'])
            hospital_type = st.selectbox("Hospital Type", categories['Hospital_Type'])
            doctor_exp = st.selectbox("Doctor Experience", categories['Doctor_Experience'])
            insurance = st.selectbox("Insurance Coverage", categories['Insurance'])
        with col2:
            stay_days = st.number_input("Estimated Stay (Days)", 1, 365, 10)
            travel_class = st.selectbox("Travel Class", categories['Travel_Class'])
            room_type = st.selectbox("Room Category", categories['Room_Type'])
            city = st.selectbox("Target City", categories['City'])
            target_currency = st.selectbox("Display Currency", ["USD", "INR", "EUR", "AED", "GBP"])
            
        submit = st.form_submit_button("Generate AI Cost Estimate 🚀")
    st.markdown("</div>", unsafe_allow_html=True)
    
    if submit:
        with st.spinner("Processing data through ML Pipeline..."):
            time.sleep(1) # Simulated loading for UX
            try:
                # Let the sklearn Pipeline handle everything
                input_df = pd.DataFrame([{
                    "Disease": disease,
                    "Country": country,
                    "Hospital_Type": hospital_type,
                    "Stay_Days": stay_days,
                    "Travel_Class": travel_class,
                    "Room_Type": room_type,
                    "Doctor_Experience": doctor_exp,
                    "Insurance": insurance,
                    "City": city
                }])
                
                # Predict directly with the pipelines
                t_cost = models['Treatment_Cost'].predict(input_df)[0]
                tr_cost = models['Travel_Cost'].predict(input_df)[0]
                s_cost = models['Stay_Cost'].predict(input_df)[0]
                m_cost = models['Medicine_Cost'].predict(input_df)[0]
                tot_cost = models['Total_Cost'].predict(input_df)[0]
                
                # Format Output
                v_t, sym = convert_currency(t_cost, target_currency)
                v_tr, _ = convert_currency(tr_cost, target_currency)
                v_s, _ = convert_currency(s_cost, target_currency)
                v_m, _ = convert_currency(m_cost, target_currency)
                v_tot, _ = convert_currency(tot_cost, target_currency)
                
                # Database Save
                save_prediction(st.session_state['user_id'], disease, country, v_tot)
                st.session_state['prediction_history'].append({
                    'type': 'Prediction', 'details': f"{disease} in {country} ({sym}{v_tot:,.0f})", 
                    'time': datetime.now().strftime("%H:%M")
                })
                
                st.success("✅ AI Cost Prediction Generated Successfully!")
                
                st.markdown("### 📊 Estimated Budget Breakdown")
                c1, c2, c3, c4, c5 = st.columns(5)
                c1.markdown(f"<div class='glass-card' style='padding:15px;'><div class='metric-title'>Treatment</div><div class='metric-value' style='font-size:20px;'>{sym}{v_t:,.0f}</div></div>", unsafe_allow_html=True)
                c2.markdown(f"<div class='glass-card' style='padding:15px;'><div class='metric-title'>Travel</div><div class='metric-value' style='font-size:20px;'>{sym}{v_tr:,.0f}</div></div>", unsafe_allow_html=True)
                c3.markdown(f"<div class='glass-card' style='padding:15px;'><div class='metric-title'>Stay</div><div class='metric-value' style='font-size:20px;'>{sym}{v_s:,.0f}</div></div>", unsafe_allow_html=True)
                c4.markdown(f"<div class='glass-card' style='padding:15px;'><div class='metric-title'>Medicine</div><div class='metric-value' style='font-size:20px;'>{sym}{v_m:,.0f}</div></div>", unsafe_allow_html=True)
                c5.markdown(f"<div class='glass-card' style='padding:15px; border-left:4px solid #10b981;'><div class='metric-title'>Total</div><div class='metric-value' style='font-size:20px; color:#10b981;'>{sym}{v_tot:,.0f}</div></div>", unsafe_allow_html=True)
                
                fig = px.pie(values=[v_t, v_tr, v_s, v_m], names=['Treatment', 'Travel', 'Stay', 'Medicine'], hole=0.5)
                fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig, use_container_width=True)
                
                patient_details = {"Disease": disease, "Country": country, "Hospital": hospital_type, "Stay": f"{stay_days} Days"}
                costs = {"Total Budget": f"{sym}{v_tot:,.2f}", "Treatment": f"{sym}{v_t:,.2f}"}
                pdf_path = generate_pdf_report(patient_details, costs)
                with open(pdf_path, "rb") as pdf_file:
                    st.download_button("Download PDF Report 📥", data=pdf_file, file_name="MedTour_Estimate.pdf", mime="application/pdf")
                    
            except Exception as e:
                st.error("Prediction failed. The ML Pipeline encountered an error.")
                st.write(f"*(Developer Error Trace: {str(e)})*")
