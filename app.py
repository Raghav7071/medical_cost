import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os
import matplotlib.pyplot as plt
from utils.helpers import convert_currency, generate_pdf_report, get_hospital_recommendation, get_best_city_recommendation

# 1. Page Configuration
st.set_page_config(
    page_title="AI Medical Tourism Cost Predictor",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Custom CSS for Modern UI
st.markdown("""
<style>
    /* Main App Background and text */
    .stApp {
        background-color: #f8fafc;
        color: #1e293b;
        font-family: 'Inter', sans-serif;
    }
    /* Headers */
    h1, h2, h3 {
        color: #0f172a;
        font-weight: 700;
    }
    /* Metric Cards */
    div[data-testid="metric-container"] {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 0.75rem;
        padding: 1rem;
        box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
        transition: transform 0.2s ease-in-out;
    }
    div[data-testid="metric-container"]:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1);
    }
    div[data-testid="metric-container"] label {
        color: #64748b;
        font-weight: 500;
    }
    div[data-testid="metric-container"] div[data-testid="stMetricValue"] {
        color: #3b82f6;
        font-weight: 800;
    }
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e2e8f0;
    }
    /* Buttons */
    .stButton>button {
        width: 100%;
        background-color: #3b82f6;
        color: white;
        font-weight: 600;
        border-radius: 0.5rem;
        padding: 0.5rem 1rem;
        border: none;
        transition: background-color 0.2s ease;
    }
    .stButton>button:hover {
        background-color: #2563eb;
    }
    /* Card-like containers */
    .css-1r6slb0, .st-emotion-cache-1r6slb0 {
        background: white;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# 3. Load Models and Encoders
@st.cache_resource
def load_models():
    try:
        models = {
            'Treatment_Cost': joblib.load('saved_models/rf_model_treatment_cost.pkl'),
            'Travel_Expense': joblib.load('saved_models/rf_model_travel_expense.pkl'),
            'Stay_Cost': joblib.load('saved_models/rf_model_stay_cost.pkl'),
            'Total_Cost': joblib.load('saved_models/rf_model_total_cost.pkl')
        }
        label_encoders = joblib.load('saved_models/label_encoders.pkl')
        scaler = joblib.load('saved_models/scaler.pkl')
        return models, label_encoders, scaler
    except Exception as e:
        st.error("Models not found. Please run model_training.py first.")
        return None, None, None

models, label_encoders, scaler = load_models()

# 4. App Layout & Sidebar
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2966/2966327.png", width=100)
st.sidebar.title("MedTour AI")
st.sidebar.markdown("Predict medical tourism costs with machine learning.")

page = st.sidebar.radio("Navigation", ["Cost Predictor", "Data Analytics", "AI Assistant"])

# Options for inputs based on dataset generation logic
diseases = ['Heart Bypass', 'Knee Replacement', 'Spinal Fusion', 'Cataract Surgery', 'Dental Implants', 'Cosmetic Surgery', 'Oncology Treatment']
countries = ['USA', 'UK', 'Canada', 'Australia', 'Germany', 'France', 'UAE']
hospital_types = ['Public', 'Private', 'Premium International']
treatment_types = ['Surgical', 'Non-Surgical', 'Radiotherapy', 'Chemotherapy']
cities = ['Bangkok', 'Istanbul', 'Mumbai', 'Singapore', 'Kuala Lumpur', 'Dubai', 'Seoul']
room_types = ['General Ward', 'Semi-Private', 'Private', 'VIP Suite']
currencies = ['USD', 'INR', 'AED', 'EUR', 'GBP']

if page == "Cost Predictor":
    st.title("💡 AI Medical Cost Predictor")
    st.markdown("Get an accurate estimation of your medical trip budget.")
    
    with st.container():
        st.markdown('<div class="css-1r6slb0">', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        
        with col1:
            disease = st.selectbox("Disease/Condition", diseases)
            country = st.selectbox("Target Country", countries)
            hospital_type = st.selectbox("Hospital Type", hospital_types)
            treatment_type = st.selectbox("Treatment Type", treatment_types)
        
        with col2:
            city = st.selectbox("Target City", cities)
            room_type = st.selectbox("Room Type", room_types)
            stay_days = st.number_input("Estimated Stay Duration (Days)", min_value=1, max_value=365, value=10)
            target_currency = st.selectbox("Select Currency", currencies, index=0)
            
        predict_btn = st.button("Predict Costs 🚀")
        st.markdown('</div>', unsafe_allow_html=True)
        
    if predict_btn and models:
        with st.spinner("Analyzing healthcare data..."):
            # Prepare input
            input_data = pd.DataFrame([{
                'Disease': disease,
                'Country': country,
                'Hospital_Type': hospital_type,
                'Treatment_Type': treatment_type,
                'City': city,
                'Room_Type': room_type,
                'Stay_Days': stay_days
            }])
            
            # Encode
            try:
                for col, le in label_encoders.items():
                    # Handle unseen labels just in case
                    if input_data[col][0] not in le.classes_:
                        input_data[col] = le.transform([le.classes_[0]])
                    else:
                        input_data[col] = le.transform(input_data[col])
                        
                # Scale
                input_scaled = scaler.transform(input_data)
                
                # Predict
                treatment_cost = models['Treatment_Cost'].predict(input_scaled)[0]
                travel_expense = models['Travel_Expense'].predict(input_scaled)[0]
                stay_cost = models['Stay_Cost'].predict(input_scaled)[0]
                total_cost = models['Total_Cost'].predict(input_scaled)[0]
                
                # Apply currency conversion
                t_cost_c, sym = convert_currency(treatment_cost, target_currency)
                tr_exp_c, _ = convert_currency(travel_expense, target_currency)
                s_cost_c, _ = convert_currency(stay_cost, target_currency)
                tot_cost_c, _ = convert_currency(total_cost, target_currency)
                
                st.subheader("📊 Estimated Medical Budget")
                
                # Metrics Display
                mcol1, mcol2, mcol3, mcol4 = st.columns(4)
                mcol1.metric("Treatment Cost", f"{sym}{t_cost_c:,.2f}")
                mcol2.metric("Travel Expense", f"{sym}{tr_exp_c:,.2f}")
                mcol3.metric("Hospital Stay", f"{sym}{s_cost_c:,.2f}")
                mcol4.metric("Total Budget", f"{sym}{tot_cost_c:,.2f}")
                
                st.markdown("---")
                
                # Visualizations
                st.subheader("Cost Breakdown")
                fig, ax = plt.subplots(figsize=(8, 4))
                costs = [t_cost_c, tr_exp_c, s_cost_c]
                labels = ['Treatment', 'Travel', 'Stay']
                colors = ['#3b82f6', '#10b981', '#f59e0b']
                ax.pie(costs, labels=labels, autopct='%1.1f%%', colors=colors, startangle=90, wedgeprops={'width': 0.4})
                ax.axis('equal')
                st.pyplot(fig)
                
                # Recommendations
                st.subheader("🏥 AI Recommendations")
                rcol1, rcol2 = st.columns(2)
                with rcol1:
                    st.info("**Recommended Hospitals**")
                    hosp_recs = get_hospital_recommendation(disease, country, hospital_type)
                    for hr in hosp_recs:
                        st.write(f"✓ {hr}")
                
                with rcol2:
                    st.success("**Top Cities for this Treatment**")
                    city_recs = get_best_city_recommendation(disease)
                    for cr in city_recs:
                        st.write(f"📍 {cr}")
                        
                # Report Generation
                st.subheader("📄 Download Report")
                patient_details = {
                    "Disease": disease,
                    "Country": country,
                    "City": city,
                    "Hospital Type": hospital_type,
                    "Room Type": room_type,
                    "Stay Duration": f"{stay_days} Days"
                }
                cost_preds = {
                    "Treatment Cost": f"{sym}{t_cost_c:,.2f}",
                    "Travel Expense": f"{sym}{tr_exp_c:,.2f}",
                    "Stay Cost": f"{sym}{s_cost_c:,.2f}",
                    "Total Budget": f"{sym}{tot_cost_c:,.2f}"
                }
                pdf_path = generate_pdf_report(patient_details, cost_preds)
                with open(pdf_path, "rb") as pdf_file:
                    st.download_button(
                        label="Download PDF Report 📥",
                        data=pdf_file,
                        file_name="Medical_Budget_Report.pdf",
                        mime="application/pdf"
                    )
            except Exception as e:
                st.error(f"Error during prediction: {e}")

elif page == "Data Analytics":
    st.title("📈 Healthcare Data Analytics")
    try:
        df = pd.read_csv('dataset.csv')
        st.write("View the synthetic healthcare dataset used to train the AI models.")
        st.dataframe(df.head(100))
        
        st.subheader("Global Cost Analysis")
        
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Average Treatment Cost by Disease**")
            disease_cost = df.groupby('Disease')['Total_Cost'].mean().sort_values(ascending=False)
            fig, ax = plt.subplots(figsize=(10, 6))
            disease_cost.plot(kind='bar', color='#3b82f6', ax=ax)
            plt.ylabel("Average Total Cost ($)")
            plt.xticks(rotation=45)
            st.pyplot(fig)
            
        with col2:
            st.write("**Hospital Type Distribution**")
            hosp_dist = df['Hospital_Type'].value_counts()
            fig, ax = plt.subplots(figsize=(8, 8))
            ax.pie(hosp_dist, labels=hosp_dist.index, autopct='%1.1f%%', colors=['#10b981', '#f59e0b', '#ef4444'])
            st.pyplot(fig)
            
    except FileNotFoundError:
        st.error("Dataset not found. Run model_training.py to generate dataset.csv")

elif page == "AI Assistant":
    st.title("🤖 AI Medical Assistant")
    st.markdown("Ask our AI assistant about symptoms, medical tourism tips, or hospital recommendations.")
    
    # Simple Mock Chatbot for demonstration
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("E.g., What are the best countries for heart bypass?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            # Mock response logic
            response = "I am an AI assistant. Based on your query, popular destinations for your mentioned procedure often include countries like India, Thailand, and the USA. Would you like a cost estimate for any of these?"
            if "heart" in prompt.lower():
                response = "For Heart Bypass, top recommended destinations include USA for advanced care and India/Thailand for cost-effective, high-quality care."
            elif "symptom" in prompt.lower():
                response = "I cannot provide a medical diagnosis, but I recommend consulting a healthcare professional. For specialized treatments, our predictor can help estimate costs once you have a diagnosis."
                
            st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("© 2026 MedTour AI")
