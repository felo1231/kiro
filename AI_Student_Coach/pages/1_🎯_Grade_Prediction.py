import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

st.set_page_config(page_title="Grade Prediction", page_icon="🎯", layout="wide")

st.markdown("""
    <style>
    .stApp {
        background: radial-gradient(circle at 20% 30%, #1e1b4b 0%, #0f172a 80%);
    }
    .app-title {
        font-size: 2.2rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 20px;
    }
    .result-box {
        background: linear-gradient(135deg, #4f46e5 0%, #06b6d4 100%);
        padding: 20px;
        border-radius: 12px;
        font-size: 1.4rem;
        font-weight: 700;
        text-align: center;
        color: white;
        margin-top: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    </style>
""", unsafe_allow_html=True)

import os
from pathlib import Path

@st.cache_resource
def load_model():
    # تحديد مسار الملف بدقة سواء كان داخل المجلد الرئيسي أو بجانب مجلد pages
    current_dir = Path(__file__).resolve().parent  # مجلد pages
    parent_dir = current_dir.parent                # المجلد الرئيسي للبروجكت
    
    # البحث عن الملف في المجلد الرئيسي أو الحالي
    csv_path = parent_dir / "StudentsPerformance.csv"
    if not csv_path.exists():
        csv_path = current_dir / "StudentsPerformance.csv"
        
    df = pd.read_csv(csv_path)
    df.drop(columns=["parental level of education", "lunch"], inplace=True)

    le_gender = LabelEncoder()
    le_race   = LabelEncoder()
    le_prep   = LabelEncoder()

    df["gender_enc"]  = le_gender.fit_transform(df["gender"])
    df["race_enc"]    = le_race.fit_transform(df["race/ethnicity"])
    df["prep_enc"]    = le_prep.fit_transform(df["test preparation course"])

    X = df[["gender_enc", "race_enc", "prep_enc", "math score", "reading score"]]
    y = df["writing score"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

    model = LinearRegression()
    model.fit(X_train, y_train)

    return model, le_gender, le_race, le_prep, df