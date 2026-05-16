import streamlit as st

try:
    from streamlit_mic_recorder import mic_recorder
    MIC_AVAILABLE = True
except ImportError:
    MIC_AVAILABLE = False

from chatbot.main import get_chatbot_response, get_symptom_analysis

def render():
    st.markdown("<h2 class='title-text'>🤖 AI Healthcare Chatbot</h2>", unsafe_allow_html=True)

    # API Key
    api_key = st.sidebar.text_input("Gemini API Key (optional)", type="password", key="gemini_key")

    # Chat History
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Symptom Analysis
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.subheader("🩺 Symptom Analyzer")
    symptoms = st.text_area("Describe your symptoms", placeholder="e.g., chest pain, shortness of breath, fatigue")
    if st.button("Analyze Symptoms", key="analyze_btn"):
        with st.spinner("Analyzing symptoms..."):
            result = get_symptom_analysis(symptoms, api_key)
            c1, c2, c3 = st.columns(3)
            c1.metric("Likely Condition", result.get("Disease", "N/A"))
            c2.metric("Department", result.get("Department", "N/A"))
            c3.metric("Severity", result.get("Severity", "N/A"))
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")

    # Chat Interface
    st.subheader("💬 Chat with MediGuide AI")

    # Display chat history
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # Voice Input
    if MIC_AVAILABLE:
        audio = mic_recorder(start_prompt="🎤 Speak", stop_prompt="⏹ Stop", key="mic_input")
        if audio:
            st.info("Voice input captured. (Transcription requires additional API setup)")

    # Text Input
    user_input = st.chat_input("Ask about medical tourism, costs, hospitals...")
    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)

        with st.spinner("Thinking..."):
            response = get_chatbot_response(user_input, api_key)
        st.session_state.chat_history.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.write(response)
