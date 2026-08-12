import os
from pathlib import Path
import numpy as np
import pandas as pd
import streamlit as st
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
        font-weight: 800;
        color: #ffffff;
        margin-bottom: 20px;
    }
    .result-box {
        background: linear-gradient(135deg, #6366f1 0%, #06b6d4 100%);
        padding: 20px;
        border-radius: 12px;
        font-size: 1.4rem;
        font-weight: 700;
        text-align: center;
        color: white;
        margin-top: 20px;
        box-shadow: 0 4px 20px rgba(99, 102, 241, 0.4);
    }
    </style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_model():
    current_dir = Path(__file__).resolve().parent
    csv_path = current_dir.parent / "StudentsPerformance.csv"
    
    if not csv_path.exists():
        csv_path = current_dir / "StudentsPerformance.csv"
    if not csv_path.exists():
        csv_path = Path("StudentsPerformance.csv")

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

with tap1:
    model, le_gender, le_race, le_prep, df = load_model()

    st.markdown('<div class="app-title">🏆 Writing Score Prediction</div>', unsafe_allow_html=True)

    col_left, col_right = st.columns(2)

    with col_left:
        gender = st.selectbox("Gender:", sorted(df["gender"].unique().tolist()))
        race = st.selectbox("Race/Ethnicity:", sorted(df["race/ethnicity"].unique().tolist()))
        prep = st.selectbox("Test Preparation Course:", sorted(df["test preparation course"].unique().tolist()))

    with col_right:
        math_score    = st.slider("Math Score:", 0, 100, 70)
        reading_score = st.slider("Reading Score:", 0, 100, 75)

    if st.button("Predict Writing Score 🚀", use_container_width=True):
        g_enc = le_gender.transform([gender])[0]
        r_enc = le_race.transform([race])[0]
        p_enc = le_prep.transform([prep])[0]

        features = np.array([[g_enc, r_enc, p_enc, math_score, reading_score]])
        prediction = model.predict(features)[0]
        prediction = max(0, min(100, prediction))

        st.markdown(
            f'<div class="result-box">Predicted Writing Score: {prediction:.1f}</div>',
            unsafe_allow_html=True
        )