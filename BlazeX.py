import streamlit as st
import random

# إعداد شكل الصفحة والعنوان الرئيسي
st.set_page_config(page_title="BlazeX Email Creator", page_icon="🔥")

st.markdown("<h1 style='text-align: center;'>🔥 BlazeX Email Creator 🔥</h1>", unsafe_allow_html=True)
st.write("---")

# قاموس الأقسام والأكواد الخاصة بها
departments = {
    "Technology": "dev",
    "Marketing": "mkt",
    "Operation": "op",
    "Finance": "fin",
    "Sales": "sl",
    "Human Resources": "hr"
}

# تقسيم الواجهة إلى عمودين لتطابق شكل التصميم
col1, col2 = st.columns(2)

with col1:
    first_name = st.text_input(
        "Enter your first name:", 
        max_chars=12, 
        icon="🧑", 
        placeholder="Ahmed"
    )
    phone_number = st.text_input(
        "Enter your phone number:", 
        max_chars=11, 
        icon="📞", 
        placeholder="01121029022"
    )

with col2:
    last_name = st.text_input(
        "Enter your last name:", 
        max_chars=12, 
        icon="🧑", 
        placeholder="Ali"
    )
    selected_dept = st.selectbox(
        "Choose your department:", 
        options=list(departments.keys()), 
        icon="🏢"
    )

st.write("---")

# زر إنشاء البريد الإلكتروني
if st.button("🔥 Generate Business Email"):
    # التحقق من إدخال كافة البيانات
    if not first_name or not last_name or len(phone_number) != 11:
        st.error("Please fill in all fields correctly (Phone number must be exactly 11 digits).")
    else:
         # استخراج كود القسم
         dept_code = departments[selected_dept]

         # استخراج آخر رقمين من رقم الهاتف
         last_2_phone = phone_number[-2:]

         # توليد رقم عشوائي مكون من خانتين (00 - 99)
         random_id = f"{random.randint(0, 99):02d}"
 
         # صيغة البريد الإلكتروني
         email = f"{first_name.strip().lower()}.{last_name.strip().lower()}.{dept_code}.{last_2_phone}.{random_id}@BlazeX.com"

         # رسالة النجاح
         st.success("Business email generated successfully!")
 
         # عرض البريد الإلكتروني الناتج
         st.subheader("📧 Your Business Email:")

        # استخدام st.code لتفعيل ميزة النسخ السريع (Bonus Part)
        st.code(email, language=None)