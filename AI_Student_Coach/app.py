import streamlit as st

import streamlit as st

# 1. إخفاء قائمة التنقل العمودية الافتراضية من الشريط الجانبي بواسطة CSS
st.markdown("""
    <style>
        [data-testid="stSidebarNav"] {display: none;}
        
        /* تنسيق اختياري لجعل الأزرار تبدو كشريط تنقل أنيق */
        div[data-testid="stPageLink"] a {
            background-color: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 10px;
            padding: 8px 16px;
            text-align: center;
            transition: all 0.3s ease;
        }
        div[data-testid="stPageLink"] a:hover {
            background-color: #6C5CE7;
            color: white;
            border-color: #6C5CE7;
        }
    </style>
""", unsafe_allow_html=True)

# 2. إنشاء شريط التنقل الأفقي في صف واحد
nav_col1, nav_col2, nav_col3 = st.columns(3)

with nav_col1:
    st.page_link("app.py", label="🏠 Main Home", use_container_width=True)

with nav_col2:
    st.page_link("pages/1_🎯_Grade_Prediction.py", label="🎯 Grade Prediction", use_container_width=True)

with nav_col3:
    st.page_link("pages/2_🤖_AI_Study_Coach.py", label="🤖 AI Study Coach", use_container_width=True)

st.divider()
st.set_page_config(page_title="AI Student Hub", page_icon="🎓", layout="centered")

# تصميم الخلفية والتأثيرات الزجاجية
st.markdown("""
    <style>
    .stApp {
        background: radial-gradient(circle at 50% 20%, #1a1a3a 0%, #0c0c16 80%);
    }
    .hero-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 30px;
        text-align: center;
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        margin-top: 2rem;
    }
    .title-text {
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, #a8c0ff 0%, #3f2b96 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="hero-card">
        <h1 class="title-text">🎓 Welcome to AI Student Hub</h1>
        <p style="font-size: 1.2rem; color: #a0aec0;">Your all-in-one platform for grade prediction and personalized AI tutoring.</p>
    </div>
""", unsafe_allow_html=True)

st.markdown("### 👈 Choose a tool from the sidebar to get started:")

col1, col2 = st.columns(2)

with col1:
    st.info("### 🎯 Student Grade Prediction\nEstimate writing scores using machine learning based on study metrics.")

with col2:
    st.success("### 🤖 AI Study Coach\nGet personalized learning advice adapted to your style and level.")