import streamlit as st
from recommendation_engine import compare_packages

def render():
    # Initialize session states for package navigation
    if "current_package_page" not in st.session_state:
        st.session_state.current_package_page = "comparison"
    if "selected_package" not in st.session_state:
        st.session_state.selected_package = None

    if st.session_state.current_package_page == "comparison":
        show_comparison()
    elif st.session_state.current_package_page == "details":
        show_package_details()

def show_comparison():
    st.markdown("<h2 class='title-text'>⚖️ Healthcare Package Comparison</h2>", unsafe_allow_html=True)
    st.write("Compare different tiers of medical tourism packages. Select a tier to view details.")
    
    disease = st.selectbox("Select Treatment to Compare", ["Heart Bypass", "Oncology", "Knee Replacement", "Cosmetic Surgery"], key="compare_disease")
    base_cost = 10000
    
    packages = compare_packages(disease)
    
    cols = st.columns(3)
    for i, (p_name, details) in enumerate(packages.items()):
        color = "#f59e0b" if p_name == "Premium" else "#8b5cf6" if p_name == "Luxury" else "#3b82f6"
        with cols[i]:
            # HTML Card for styling
            st.markdown(f"""
            <div class='glass-card' style='border-top: 5px solid {color}; text-align:center;'>
                <h3 style='color:{color}; text-transform:uppercase;'>{p_name}</h3>
                <h1 style='color:#1e293b; margin:10px 0;'>${base_cost * details['Cost_Multiplier']:,.0f}</h1>
                <hr>
                <p>🛏️ <b>Room:</b> {details['Room']}</p>
                <p>👨‍⚕️ <b>Consultations:</b> {details['Consultations']}</p>
                <p>🚗 <b>Airport Transfer:</b> {details['Airport_Transfer']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Streamlit Button to handle click events
            if st.button(f"Select {p_name}", key=f"btn_{p_name}", use_container_width=True):
                st.session_state.selected_package = p_name
                st.session_state.current_package_page = "details"
                st.rerun()

def show_package_details():
    p_name = st.session_state.selected_package
    disease = st.session_state.get("compare_disease", "Heart Bypass")
    base_cost = 10000
    packages = compare_packages(disease)
    
    # Error Handling
    if not p_name or p_name not in packages:
        st.session_state.current_package_page = "comparison"
        st.rerun()
        
    details = packages[p_name]
    cost = base_cost * details['Cost_Multiplier']
    color = "#f59e0b" if p_name == "Premium" else "#8b5cf6" if p_name == "Luxury" else "#3b82f6"
    
    # Header & Back Button
    col_back, col_title = st.columns([1, 4])
    with col_back:
        if st.button("⬅️ Back to Plans"):
            st.session_state.current_package_page = "comparison"
            st.rerun()
    with col_title:
        st.markdown(f"<h2 class='title-text' style='color:{color}; margin-top:-5px;'>{p_name.upper()} PACKAGE DETAILS</h2>", unsafe_allow_html=True)
        
    st.markdown("---")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown(f"<div class='glass-card' style='border-left: 5px solid {color};'>", unsafe_allow_html=True)
        st.subheader(f"Treatment: {disease}")
        st.markdown("### 📋 Package Inclusions")
        st.write(f"🛏️ **Room Type:** {details['Room']}")
        st.write(f"👨‍⚕️ **Doctor Consultations:** {details['Consultations']}")
        st.write(f"🚗 **Airport Transfer:** {details['Airport_Transfer']}")
        
        st.markdown("### ✨ Additional Benefits")
        if p_name == "Standard":
            st.markdown("- Dedicated Nursing Staff\n- Standard Meals\n- Post-op Tele-consultation (1 week)")
        elif p_name == "Premium":
            st.markdown("- 24/7 Dedicated Nursing Staff\n- Personalized Diet Plan\n- Fast-track Visa Assistance\n- Post-op Tele-consultation (1 month)")
        else:
            st.markdown("- 24/7 Private Nursing Staff\n- Gourmet Chef Prepared Meals\n- Premium Visa Processing\n- Dedicated Concierge\n- Luxury Wellness Spa Session\n- Lifetime Post-op Tele-consultations")
            
        st.markdown("### ⏱️ Estimated Recovery Time")
        st.write("Average hospital stay of 7-14 days depending on patient health metrics.")
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col2:
        st.markdown(f"<div class='glass-card' style='text-align:center;'>", unsafe_allow_html=True)
        st.markdown("<p style='color:#64748b; font-weight:bold; text-transform:uppercase;'>Total Package Price</p>", unsafe_allow_html=True)
        st.markdown(f"<h1 style='color:{color}; font-size:45px; margin: 0;'>${cost:,.0f}</h1>", unsafe_allow_html=True)
        st.markdown("<p style='font-size:12px; color:#64748b; margin-top: 10px;'>*Includes hospital fees, surgeon fees, and facility charges.</p>", unsafe_allow_html=True)
        st.markdown("<hr>", unsafe_allow_html=True)
        
        if st.button("📅 Book Appointment", type="primary", use_container_width=True):
            st.success(f"Booking request for {p_name} Package sent! A medical coordinator will contact you shortly.")
            st.balloons()
            
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("### 🏥 Recommended Hospital")
        st.info("**Global Medical Center**\n\n⭐ 4.8/5.0 Rating\n\nJCI Accredited Facility")
        st.markdown("</div>", unsafe_allow_html=True)
