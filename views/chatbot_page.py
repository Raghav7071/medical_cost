import streamlit as st
from streamlit_mic_recorder import mic_recorder
from chatbot.main import get_chatbot_response, get_symptom_analysis

def render():
    st.markdown("<h2 class='title-text'>🤖 MediGuide Voice & Text Assistant</h2>", unsafe_allow_html=True)
    st.write("Ask our AI about treatments, visas, or symptoms.")
    
    api_key = st.text_input("Enter Gemini API Key (Optional for simulation)", type="password")
    
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.write("🎙️ **Voice Input**")
    audio = mic_recorder(start_prompt="Click to Record ⏺️", stop_prompt="Stop Recording ⏹️", key='recorder')
    if audio:
        st.success("Audio captured! (Speech-to-text processing...)")
    st.markdown("</div>", unsafe_allow_html=True)
        
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [{"role": "assistant", "content": "Hello! I am MediGuide AI. How can I assist you with your medical journey today?"}]

    st.markdown("<div class='glass-card' style='height: 400px; overflow-y: auto;'>", unsafe_allow_html=True)
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
    st.markdown("</div>", unsafe_allow_html=True)

    if prompt := st.chat_input("Type your medical question here..."):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        st.rerun()

    # Process the last message if it's from user
    if len(st.session_state.chat_history) > 0 and st.session_state.chat_history[-1]["role"] == "user":
        prompt = st.session_state.chat_history[-1]["content"]
        with st.spinner("AI is typing..."):
            response = get_chatbot_response(prompt, api_key)
        st.session_state.chat_history.append({"role": "assistant", "content": response})
        st.rerun()
