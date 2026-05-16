import streamlit as st
from recommendation_engine import get_hospitals, get_doctors

def render():
    st.markdown("<h2 class='title-text'>🏥 AI Matchmaking & Recommendations</h2>", unsafe_allow_html=True)
    st.write("Find the perfect hospital and specialist tailored to your budget and medical needs.")
    
    with st.form("rec_form"):
        col1, col2, col3 = st.columns(3)
        with col1:
            disease = st.text_input("Disease Specialization", "Heart Bypass")
        with col2:
            country = st.selectbox("Target Country", ["USA", "India", "Turkey", "Singapore", "Thailand", "Germany"])
            city = st.text_input("Preferred City (Optional)", "New York")
        with col3:
            budget = st.number_input("Max Budget ($)", 1000, 150000, 15000)
            
        submit = st.form_submit_button("Find My Matches 🔍")
        
    if submit:
        st.markdown("---")
        st.subheader("🏆 Top Recommended Hospitals")
        hosp = get_hospitals(disease, country, city, budget)
        
        if hosp:
            for h in hosp:
                with st.expander(f"🏥 {h['Name']} - {h['Cost_Range']} Package"):
                    st.write(f"**Specialization:** {h['Specialization']}")
                    st.write(f"**City:** {h['City']}")
                    st.write(f"**Patient Rating:** ⭐ {h['Rating']}/5.0")
                    st.button(f"Request Quote from {h['Name']}", key=h['Name'])
        else:
            st.warning("No hospitals found matching this budget. Try increasing your budget.")
            
        st.markdown("---")
        st.subheader("👨‍⚕️ Top Matching Specialists")
        docs = get_doctors(disease, country)
        for d in docs:
            st.markdown(f"<div class='glass-card' style='padding:15px; border-left: 4px solid #2563eb;'>"
                        f"<h4>{d['Name']}</h4>"
                        f"<p><b>Experience:</b> {d['Experience']} | <b>Languages:</b> {d['Language']}</p>"
                        f"</div>", unsafe_allow_html=True)
