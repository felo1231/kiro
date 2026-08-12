import streamlit as st

st.set_page_config(page_title="AI Student Hub", page_icon="🎓", layout="centered")

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