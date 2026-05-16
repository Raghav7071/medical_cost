import streamlit as st
import time

from database import init_db, verify_user, add_user

# Setup Page
st.set_page_config(page_title="MediGuide AI", page_icon="🏥", layout="wide", initial_sidebar_state="expanded")

# Initialize Database
init_db()

# --- Custom CSS for Glassmorphism & Sidebar UI ---
def get_css(dark_mode=False):
    bg_color = "#1e1e1e" if dark_mode else "#f0f4f8"
    text_color = "#ffffff" if dark_mode else "#1e293b"
    card_bg = "rgba(0, 0, 0, 0.6)" if dark_mode else "rgba(255, 255, 255, 0.7)"
    card_border = "rgba(255, 255, 255, 0.1)" if dark_mode else "rgba(255, 255, 255, 0.4)"
    title_color = "#60a5fa" if dark_mode else "#1e3a8a"
    
    return f"""
    <style>
        .stApp {{
            background-color: {bg_color};
            color: {text_color};
            transition: all 0.3s ease;
        }}
        .glass-card {{
            background: {card_bg};
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 1px solid {card_border};
            border-radius: 16px;
            padding: 24px;
            box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
            margin-bottom: 24px;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }}
        .metric-title {{ color: #64748b; font-size: 14px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px; }}
        .metric-value {{ color: {text_color}; font-size: 32px; font-weight: 900; }}
        .title-text {{ color: {title_color}; font-weight: 800; font-family: 'Inter', sans-serif; }}
        
        /* Main Button styling */
        .stButton>button {{
            background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
            color: white; border-radius: 8px; width: 100%; font-weight: bold; border: none; padding: 12px; transition: 0.3s;
        }}
        .stButton>button:hover {{ background: linear-gradient(135deg, #1d4ed8 0%, #1e3a8a 100%); box-shadow: 0 4px 15px rgba(37, 99, 235, 0.4); }}
        
        /* Sidebar custom button styling for navigation */
        [data-testid="stSidebar"] .stButton>button {{
            background: transparent;
            color: {text_color};
            border: 1px solid transparent;
            text-align: left;
            justify-content: flex-start;
            padding: 10px 15px;
        }}
        [data-testid="stSidebar"] .stButton>button:hover {{
            background: rgba(37, 99, 235, 0.1);
            border: 1px solid #2563eb;
            color: #2563eb;
            box-shadow: none;
        }}
    </style>
    """

# --- Session State ---
if 'user_id' not in st.session_state: st.session_state['user_id'] = None
if 'username' not in st.session_state: st.session_state['username'] = None
if 'dark_mode' not in st.session_state: st.session_state['dark_mode'] = False
if 'prediction_history' not in st.session_state: st.session_state['prediction_history'] = []

# Main App Navigation State
if "page" not in st.session_state:
    st.session_state.page = "dashboard"

# Apply CSS
st.markdown(get_css(st.session_state['dark_mode']), unsafe_allow_html=True)

# --- Auth Pages ---
if not st.session_state['user_id']:
    st.markdown("<h1 class='title-text' style='text-align:center; font-size: 3rem; margin-top: 5vh;'>MediGuide AI 🏥</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; font-size: 1.2rem; color: #64748b;'>Smart Medical Tourism & Healthcare Cost Intelligence Platform</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,1.5,1])
    with col2:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        auth_mode = st.radio("Select Action", ["Login", "Sign Up"], horizontal=True, label_visibility="collapsed")
        st.write("---")
        if auth_mode == "Login":
            user_input = st.text_input("Username")
            pass_input = st.text_input("Password", type="password")
            if st.button("Secure Login 🔒"):
                with st.spinner("Authenticating..."):
                    time.sleep(0.5)
                    uid = verify_user(user_input, pass_input)
                    if uid:
                        st.session_state['user_id'] = uid
                        st.session_state['username'] = user_input
                        st.rerun()
                    elif user_input == "admin" and pass_input == "admin123":
                        st.session_state['user_id'] = 999
                        st.session_state['username'] = "admin"
                        st.rerun()
                    else:
                        st.error("Invalid credentials.")
        else:
            new_user = st.text_input("New Username")
            new_email = st.text_input("Email Address")
            new_pass = st.text_input("New Password", type="password")
            if st.button("Create Account ✨"):
                if add_user(new_user, new_pass, new_email):
                    st.success("Account created successfully! You can now log in.")
                else:
                    st.error("Username already exists or invalid details.")
        st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# --- Main App Sidebar ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2966/2966327.png", width=60)
    st.markdown(f"### Welcome, **{st.session_state['username']}**")
    
    dark_mode = st.toggle("🌙 Dark Mode", value=st.session_state['dark_mode'])
    if dark_mode != st.session_state['dark_mode']:
        st.session_state['dark_mode'] = dark_mode
        st.rerun()
        
    st.markdown("---")
    st.markdown("### Navigation")
    
    # Custom Sidebar Navigation Buttons
    if st.button("📊 Dashboard", key="nav_dashboard"):
        st.session_state.page = "dashboard"
        st.rerun()

    if st.button("💡 Cost Prediction", key="nav_prediction"):
        st.session_state.page = "prediction"
        st.rerun()

    if st.button("📈 Analytics", key="nav_analytics"):
        st.session_state.page = "analytics"
        st.rerun()

    if st.button("🏥 Hospital Recommendation", key="nav_recommendation"):
        st.session_state.page = "recommendation"
        st.rerun()

    if st.button("📄 OCR Analyzer", key="nav_ocr"):
        st.session_state.page = "ocr"
        st.rerun()

    if st.button("🤖 AI Chatbot", key="nav_chatbot"):
        st.session_state.page = "chatbot"
        st.rerun()

    if st.button("⚖️ Packages Comparison", key="nav_packages"):
        st.session_state.page = "packages"
        st.rerun()

    st.markdown("---")
    if st.button("Logout 🚪", key="nav_logout"):
        st.session_state['user_id'] = None
        st.session_state['username'] = None
        st.rerun()

# --- Dynamic Page Routing ---
if st.session_state.page == "dashboard":
    from views import dashboard
    dashboard.render()

elif st.session_state.page == "prediction":
    from views import prediction
    prediction.render()

elif st.session_state.page == "analytics":
    from views import analytics
    analytics.render()

elif st.session_state.page == "recommendation":
    from views import recommendation
    recommendation.render()

elif st.session_state.page == "ocr":
    from views import ocr_page
    ocr_page.render()

elif st.session_state.page == "chatbot":
    from views import chatbot_page
    chatbot_page.render()

elif st.session_state.page == "packages":
    from views import packages
    packages.render()
