import streamlit as st
import google.generativeai as genai
from PIL import Image

# إعداد الصفحة وتغيير الثيم لألوان هادئة واحترافية
st.set_page_config(page_title="Health Dashboard", layout="wide")

# تصميم CSS مخصص للألوان (أزرق غامق، رمادي، أسود)
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    h1 { color: #f0f2f6; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    .stMetric { background-color: #1f2937; padding: 15px; border-radius: 10px; border-left: 5px solid #3b82f6; }
    div[data-testid="stExpander"] { border: none; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center;'>📊 لوحة المتابعة الصحية</h1>", unsafe_allow_html=True)

# --- القسم الأول: الدوائر الأربعة (توزيع أفقي) ---
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("### 💧 الماء")
    water = st.select_slider("لتر/يوم", options=[i/4 for i in range(21)], value=2.0)
    st.metric("المستهلك", f"{water} L")

with col2:
    st.markdown("### 👟 الخطوات")
    steps = st.number_input("العدد اليومي", value=5000, step=500)
    st.metric("النشاط", f"{steps:,}")

with col3:
    st.markdown("### 📈 التقدم")
    # سيتم ربطها بالوزن في الأسفل
    st.metric("الحالة", "مستمر", delta="-2kg")

with col4:
    st.markdown("### 🔥 الحرق")
    burned = st.number_input("سعرة محروقة", value=300)
    st.metric("الإجمالي", f"{burned} kcal")

st.markdown("---")

# --- القسم الثاني: قائمة الوجبات (فطور، غداء، عشاء، سناك) ---
st.subheader("🍽️ إدارة الوجبات")
meal_type = st.radio("اختر الوجبة الحالية:", ["فطور", "غداء", "سناك", "عشاء"], horizontal=True)

uploaded_file = st.file_input(f"ارفع صورة ({meal_type}) للتحليل الذكي", type=["jpg", "png", "jpeg"])

if uploaded_file:
    img = Image.open(uploaded_file)
    st.image(img, width=400)
    if st.button("تحليل الوجبة بالسيرفر"):
        st.write("جاري المعالجة...") # هنا سيعمل كود Gemini عند وضع الـ Secrets

st.markdown("---")

# --- القسم الثالث: الوزن الحالي والمطلوب ---
col_w1, col_w2 = st.columns(2)

with col_w1:
    current_w = st.number_input("الوزن الحالي (كجم)", value=85.0)

with col_w2:
    target_w = st.number_input("الوزن المطلوب (كجم)", value=75.0)

st.markdown("---")

# --- القسم الرابع: إحصائيات ---
st.subheader("📉 الإحصائيات والأداء")
chart_data = [87, 86.5, 86, 85.5, current_w] # مثال لخط بياني هادئ
st.line_chart(chart_data)

st.markdown("<p style='text-align: center; color: gray;'>نظام المتابعة الذكي - الإصدار 1.0</p>", unsafe_allow_html=True)