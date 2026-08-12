import streamlit as st
import pandas as pd
import plotly.express as px

# إعداد الصفحة
st.set_page_config(
    page_title="Products Sales Dashboard",
    page_icon="📊",
    layout="wide"
)

# خلفية احترافية وتأثيرات زجاجية ناعمة تتوافق مع الألوان المطلوبة
st.markdown("""
    <style>
    /* خلفية متدرجة مظلمة مع شبكة أنيقة */
    .stApp {
        background: radial-gradient(circle at 50% 10%, #1a2628 0%, #0B0F0A 70%);
    }

    /* تحسين شكل بطاقات القياس */
    div[data-testid="stMetric"] {
        background: rgba(26, 31, 23, 0.7);
        border: 1px solid rgba(75, 205, 217, 0.25);
        padding: 18px;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
        backdrop-filter: blur(10px);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }

    div[data-testid="stMetric"]:hover {
        transform: translateY(-3px);
        border-color: #4bcdd9;
    }

    div[data-testid="stMetricLabel"] {
        color: #A0AEC0 !important;
        font-weight: 600;
        font-size: 0.95rem;
    }

    div[data-testid="stMetricValue"] {
        color: #FFFFFF !important;
        font-weight: 700;
    }

    /* تحسين العنوان */
    .main-header {
        text-align: center;
        font-size: 2.2rem;
        font-weight: 800;
        color: #FFFFFF;
        margin-bottom: 1.5rem;
    }
    </style>
""", unsafe_allow_html=True)

# عنوان التطبيق
st.markdown("<h1 class='main-header'>📊 Products Sales Dashboard</h1>", unsafe_allow_html=True)

# قراءة البيانات مع معالجة الأخطاء وإتاحة الرفع الاحتياطي
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("sales.csv")
        return df
    except FileNotFoundError:
        return None

df_raw = load_data()

if df_raw is None:
    st.info("💡 لم يتم العثور على ملف `sales.csv` تلقائياً. يمكنك رفعه أدناه:")
    uploaded_file = st.file_uploader("Upload sales.csv", type=["csv"])
    if uploaded_file is not None:
        df_raw = pd.read_csv(uploaded_file)
    else:
        st.stop()

# معالجة عمود التاريخ
df = df_raw.copy()
df['date'] = pd.to_datetime(df['date'])

# --- Bonus Part: قائمة اختيار مندوب المبيعات ---
representatives = ["All Representatives"] + list(df['sales_representative'].unique())
selected_rep = st.selectbox("📊 Select Sales Representative:", options=representatives)

# تصفية البيانات بحسب الاختيار
if selected_rep != "All Representatives":
    filtered_df = df[df['sales_representative'] == selected_rep]
else:
    filtered_df = df

# حساب الإحصائيات الثلاث
total_sales = filtered_df['sales'].sum()
avg_sales = filtered_df['sales'].mean()
highest_sale = filtered_df['sales'].max()

# عرض الإحصائيات في 3 أعمدة
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="💰 Total Sales",
        value=f"{total_sales:,.2f} EGP"
    )

with col2:
    st.metric(
        label="📈 Average Sales",
        value=f"{avg_sales:,.2f} EGP"
    )

with col3:
    st.metric(
        label="🏆 Highest Sale",
        value=f"{highest_sale:,.2f} EGP"
    )

st.markdown("<br>", unsafe_allow_html=True)

# --- الرسم البياني 1 والرسم البياني 2 ---
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.subheader("📊 Sales per Region")
    region_sales = filtered_df.groupby('region', as_index=False)['sales'].sum()
    
    fig_bar = px.bar(
        region_sales,
        x='region',
        y='sales',
        color_discrete_sequence=["#4bcdd9"],
        template="plotly_dark"
    )
    fig_bar.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis_title="",
        yaxis_title="Sales (EGP)",
        margin=dict(l=20, r=20, t=30, b=20)
    )
    st.plotly_chart(fig_bar, use_container_width=True)

with chart_col2:
    st.subheader("📈 Sales Over Time")
    time_sales = filtered_df.groupby('date', as_index=False)['sales'].sum().sort_values('date')
    
    fig_line = px.line(
        time_sales,
        x='date',
        y='sales',
        color_discrete_sequence=["#4bcdd9"],
        template="plotly_dark"
    )
    fig_line.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis_title="",
        yaxis_title="Sales (EGP)",
        margin=dict(l=20, r=20, t=30, b=20)
    )
    st.plotly_chart(fig_line, use_container_width=True)

# --- ميزات إضافية للمركز الأول ---
st.divider()

col_exp1, col_exp2 = st.columns([3, 1])

with col_exp1:
    with st.expander("🔍 View & Search Raw Sales Data Table"):
        st.dataframe(filtered_df, use_container_width=True)

with col_exp2:
    csv_bytes = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Export Report (CSV)",
        data=csv_bytes,
        file_name=f"sales_report_{selected_rep.replace(' ', '_')}.csv",
        mime="text/csv",
        use_container_width=True
    )