import streamlit as st
import google.generativeai as ai

st.set_page_config(page_title="AI Study Coach", page_icon="🤖", layout="wide")

st.markdown("""
    <style>
    .stApp {
        background: radial-gradient(circle at 80% 20%, #2e1065 0%, #0f172a 80%);
    }
    .chat-header {
        font-size: 2.2rem;
        font-weight: 800;
        color: #ffffff;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="chat-header">🤖 AI Study Coach</div>', unsafe_allow_html=True)

# توزيع عناصر التعديل بالعرض في 4 أعمدة
st.subheader("⚙️ Customization Settings")
setting_col1, setting_col2, setting_col3, setting_col4 = st.columns(4)

with setting_col1:
    learning_style = st.selectbox("Learning Style:", ["Hands-on", "Visual", "Reading/Writing", "Auditory"])

with setting_col2:
    detail_level = st.select_slider(
        "Response Details:", options=["Brief", "Medium-detailed", "Very detailed"], value="Medium-detailed"
    )

with setting_col3:
    student_level = st.selectbox("Student Level:", ["Beginner", "Intermediate", "Advanced"])

with setting_col4:
    api_key = st.text_input("Gemini API Key:", type="password", placeholder="Paste API Key...")

st.divider()

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

user_query = st.chat_input("Ask me anything about studying...")

if user_query:
    if not api_key:
        st.warning("⚠️ Please enter your Gemini API Key in the settings above.")
    else:
        st.session_state.messages.append({"role": "user", "content": user_query})
        with st.chat_message("user"):
            st.write(user_query)

        try:
            ai.configure(api_key=api_key)
            model = ai.GenerativeModel("gemini-1.5-flash")

            system_instruction = f"""
            You are an expert AI Study Coach helping a student improve academically.
            
            Strict Rule:
            You MUST ONLY answer questions related to education, studying, learning strategies, and academic advice.
            If the question is unrelated to education, strictly reply with ONLY:
            "Sorry, I cannot assist you with this, I only can help you with questions related to education!"

            Student Persona:
            - Preferred Learning Style: {learning_style}
            - Response Detail Level: {detail_level}
            - Student Expertise Level: {student_level}

            Tailor your tone, examples, and recommendations directly to match this student's profile.
            """

            prompt = f"{system_instruction}\n\nStudent Question: {user_query}"

            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response = model.generate_content(prompt)
                    bot_reply = response.text
                    st.write(bot_reply)

            st.session_state.messages.append({"role": "assistant", "content": bot_reply})

        except Exception as e:
            st.error(f"Error connecting to Gemini API: {e}")