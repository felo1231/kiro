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

# 1. القائمة الجانبية للتخصيص
with st.sidebar:
    st.subheader('Learning Style:')
    learning_style = st.selectbox("", ["Visual", "Hands-on", "Reading/Writing", "Auditory"], label_visibility="collapsed")

    st.divider()
    st.subheader('Response Details:')
    detail_level = st.select_slider(
        "", options=["Brief", "Medium-detailed", "Very detailed"], value="Medium-detailed",
        label_visibility="collapsed"
    )

    st.divider()
    st.subheader('Student Level:')
    student_level = st.radio("", ["Beginner", "Intermediate", "Advanced"], label_visibility="collapsed")

    st.divider()
    api_key = st.text_input("Enter Gemini API Key:", type="password")

st.markdown('<div class="chat-header">🤖 AI Study Coach</div>', unsafe_allow_html=True)
st.caption("Ask me anything about studying and learning strategies!")

# 2. تهيئة سجل المحادثات
if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض المحادثات السابقة
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 3. استقبال المدخلات من الطالب
user_query = st.chat_input("Ask me anything about studying...")

if user_query:
    if not api_key:
        st.warning("⚠️ Please enter your Gemini API Key in the sidebar to proceed.")
    else:
        # إضافة سؤال المستخدم للواجهة والسجل
        st.session_state.messages.append({"role": "user", "content": user_query})
        with st.chat_message("user"):
            st.write(user_query)

        # 4. إعداد نموذج Gemini والموجه الداخلي (System Prompt)
        try:
            ai.configure(api_key=api_key)
            try:
                model = ai.GenerativeModel("gemini-3.5-flash")
            except:
                model = ai.GenerativeModel("gemini-3.1-flash")
            system_instruction = f"""
            You are an expert AI Study Coach helping a student improve academically.
            
            Strict Rule:
            You MUST ONLY answer questions related to education, studying, learning strategies, and academic advice.
            If the question is unrelated to education (e.g., sports, movies, cooking, casual chat, general trivia), strictly reply with ONLY:
            "Sorry, I cannot assist you with this, I only can help you with questions related to education!"

            Student Persona & Customizations:
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