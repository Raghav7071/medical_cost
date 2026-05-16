import streamlit as st
import time

def render():
    st.markdown("<h2 class='title-text'>Dashboard Overview</h2>", unsafe_allow_html=True)
    st.write("Welcome to your central command center for Medical Tourism Intelligence.")
    
    # Real-time statistics cards
    st.markdown("### 📊 Live Platform Metrics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("<div class='metric-title'>Total Predictions</div>", unsafe_allow_html=True)
        st.markdown("<div class='metric-value'>1,284</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col2:
        st.markdown("<div class='glass-card' style='border-left: 5px solid #10b981;'>", unsafe_allow_html=True)
        st.markdown("<div class='metric-title'>Active Users</div>", unsafe_allow_html=True)
        st.markdown("<div class='metric-value' style='color:#10b981;'>342</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col3:
        st.markdown("<div class='glass-card' style='border-left: 5px solid #f59e0b;'>", unsafe_allow_html=True)
        st.markdown("<div class='metric-title'>OCR Scans</div>", unsafe_allow_html=True)
        st.markdown("<div class='metric-value' style='color:#f59e0b;'>856</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col4:
        st.markdown("<div class='glass-card' style='border-left: 5px solid #8b5cf6;'>", unsafe_allow_html=True)
        st.markdown("<div class='metric-title'>Hospitals Matched</div>", unsafe_allow_html=True)
        st.markdown("<div class='metric-value' style='color:#8b5cf6;'>4,192</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # Quick Actions
    st.markdown("### ⚡ Quick Actions")
    q1, q2, q3 = st.columns(3)
    with q1:
        st.info("**💡 Predict Cost**\n\nGenerate accurate medical travel budgets instantly.")
    with q2:
        st.success("**📄 Analyze Report**\n\nUpload a PDF/Image to extract medical data automatically.")
    with q3:
        st.warning("**🏥 Find Hospitals**\n\nMatch with top-tier international healthcare providers.")
        
    # Recent Activity
    st.markdown("### 🕒 Your Recent Activity")
    if len(st.session_state['prediction_history']) > 0:
        for activity in reversed(st.session_state['prediction_history'][-5:]):
            st.markdown(f"<div class='glass-card' style='padding: 15px;'><p style='margin:0;'><b>{activity['type']}</b>: {activity['details']} <span style='float:right; color:#64748b; font-size:12px;'>{activity['time']}</span></p></div>", unsafe_allow_html=True)
    else:
        st.write("No recent activity. Start exploring the platform!")
