import streamlit as st
import random
import pandas as pd

# إعداد الصفحة
st.set_page_config(page_title="BlazeX Email Creator", page_icon="🔥", layout="centered")

# تهيئة سجل الإيميلات المنشأة في Session State
if "created_emails" not in st.session_state:
    st.session_state.created_emails = []

st.markdown("""
    <style>
    /* خلفية متدرجة ومتحركة للألوان */
    .stApp {
        background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
    }

    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* الحاوية الرئيسية بتأثير الزجاج شفاف النواة (Glassmorphism) */
    .main .block-container {
        background: rgba(255, 255, 255, 0.92);
        padding: 2.5rem;
        border-radius: 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.2);
        backdrop-filter: blur(8px);
        margin-top: 2rem;
        margin-bottom: 2rem;
    }

    /* عنوان الصفحة */
    .main-title {
        color: #0f172a;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-weight: 800;
        font-size: 2.3rem;
        margin-bottom: 10px;
        text-align: center;
    }

    /* زر الحساب */
    div.stButton > button {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: #ffffff;
        border-radius: 10px;
        padding: 12px 28px;
        font-weight: 700;
        font-size: 1rem;
        border: none;
        width: 100%;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(15, 23, 42, 0.25);
    }

    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(15, 23, 42, 0.35);
        color: #38bdf8;
    }
    </style>
""", unsafe_allow_html=True)

# العنوان الرئيسي
st.markdown("<h1 class='main-title'>🔥 BlazeX Email Creator 🔥</h1>", unsafe_allow_html=True)
st.divider()

# قاموس الأقسام مع الأكواد والأيقونات الخاصة بها
departments = {
    "Technology": ("dev", "💻"),
    "Marketing": ("mkt", "📢"),
    "Operation": ("op", "⚙️"),
    "Finance": ("fin", "💰"),
    "Sales": ("sl", "📈"),
    "Human Resources": ("hr", "🗄️")
}

# تقسيم المدخلات إلى عمودين
col1, col2 = st.columns(2)

with col1:
    first_name = st.text_input("Enter your first name:", placeholder="👨 Ahmed", max_chars=12)
    phone_number = st.text_input("Enter your phone number:", placeholder="📞 01121029022", max_chars=11)

with col2:
    last_name = st.text_input("Enter your last name:", placeholder="👨 Ali", max_chars=12)
    
    # عرض اسم القسم مع الأيقونة داخل القائمة
    selected_dept_label = st.selectbox(
        "Choose your department:",
        options=[f"{info[1]} {name}" for name, info in departments.items()]
    )

# --- شريط نسبة اكتمال البيانات (Live Validation) ---
valid_first = bool(first_name.strip())
valid_last = bool(last_name.strip())
valid_phone = phone_number.isdigit() and len(phone_number) == 11

completed_count = sum([valid_first, valid_last, valid_phone])
progress_ratio = completed_count / 3.0

st.caption("📋 Form Completion Status:")
st.progress(progress_ratio)

st.divider()

# زر إنشاء البريد
if st.button("🔥 Generate Business Email"):
    if valid_first and valid_last and valid_phone:
        # استخراج اسم القسم النظيف بدون أيقونة
        dept_name = selected_dept_label.split(" ", 1)[1]
        dept_code = departments[dept_name][0]
        
        # استخراج آخر رقمين وتوليد رقم عشوائي
        last_2_phone = phone_number[-2:]
        random_id = f"{random.randint(0, 99):02d}"
        
        # صيغة البريد الإلكتروني
        email = f"{first_name.strip().lower()}.{last_name.strip().lower()}.{dept_code}.{last_2_phone}.{random_id}@BlazeX.com"
        
        # حفظ الإيميل في سجل المخرجات
        st.session_state.created_emails.append({
            "First Name": first_name.strip(),
            "Last Name": last_name.strip(),
            "Phone": phone_number.strip(),
            "Department": dept_name,
            "Generated Email": email
        })

        st.balloons()
        
        # عرض النتيجة
        st.success("Business email generated successfully!")
        st.markdown("### 📧 Your Business Email:")
        
        # تفعيل التلوين التلقائي للأرقام كما في الصورة
        st.code(email, language="python")
    else:
        st.error("Please fill all fields correctly:\n- Names cannot be empty.\n- Phone number must contain exactly 11 digits.")

# --- سجل الإيميلات المنشأة + تنزيل كملف CSV ---
if st.session_state.created_emails:
    st.divider()
    st.markdown("### 📊 Session Created Emails Log")
    df_emails = pd.DataFrame(st.session_state.created_emails)
    
    st.dataframe(df_emails, use_container_width=True)
    
    csv_data = df_emails.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Emails Log (CSV)",
        data=csv_data,
        file_name="BlazeX_Generated_Emails.csv",
        mime="text/csv"
    )