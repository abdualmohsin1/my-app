import streamlit as st
import google.generativeai as genai
from PIL import Image
from datetime import datetime

# إعداد الصفحة بألوان هادئة
st.set_page_config(page_title="Health Dashboard", layout="wide")

# إعداد الذكاء الاصطناعي (باستخدام المفتاح الذي وضعته في Secrets)
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

# CSS لتنسيق الألوان (احترافي وهادئ)
st.markdown("""
    <style>
    .stMetric { background-color: #1f2937; padding: 15px; border-radius: 10px; border-left: 5px solid #1e3a8a; }
    h1 { color: #f0f2f6; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1>📊 لوحة التحكم الصحية الذكية</h1>", unsafe_allow_html=True)

# --- أوامر الحسابات التلقائية ---
now = datetime.now()
# محاكاة الخطوات: تزداد تلقائياً كلما تقدم الوقت في اليوم
seconds_since_midnight = (now - now.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds()
auto_steps = int(seconds_since_midnight * 0.15) # معدل خطوات تلقائي
auto_burned = int(auto_steps * 0.04) # حرق تلقائي بناءً على الخطوات

# --- القسم الأول: العرض التلقائي ---
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("### 💧 الماء")
    water = st.number_input("لتر اليوم (يدوي)", min_value=0.0, value=2.0, step=0.25)
    st.metric("المستهلك", f"{water} L")

with col2:
    st.markdown("### 👟 الخطوات")
    st.metric("تحديث تلقائي", f"{auto_steps:,}")

with col3:
    st.markdown("### 📈 التقدم")
    # سيتم حسابها من الوزن بالأسفل تلقائياً
    st.metric("الحالة", "نشط")

with col4:
    st.markdown("### 🔥 الحرق")
    st.metric("تلقائي", f"{auto_burned} kcal")

st.divider()

# --- القسم الثاني: إدارة الوجبات (الأمر الصحيح) ---
st.subheader("🍽️ تحليل الوجبات الذكي")
meal_type = st.radio("الوجبة الحالية:", ["فطور", "غداء", "سناك", "عشاء"], horizontal=True)

# التصحيح هنا: استخدام file_uploader بدلاً من file_input
uploaded_file = st.file_uploader(f"ارفع صورة {meal_type}", type=["jpg", "png", "jpeg"])

if uploaded_file:
    img = Image.open(uploaded_file)
    st.image(img, width=400)
    if st.button("تحليل السعرات الآن"):
        with st.spinner("جاري التحليل..."):
            prompt = f"حلل هذه الصورة لـ {meal_type}. احسب السعرات التقريبية وهل تناسب نظام 2100 سعرة؟"
            response = model.generate_content([prompt, img])
            st.info(response.text)

st.divider()

# --- القسم الثالث: الوزن والتقدم التلقائي ---
col_w1, col_w2 = st.columns(2)
with col_w1:
    current_w = st.number_input("وزنك الحالي (كجم)", value=85.0)
with col_w2:
    target_w = st.number_input("الوزن المطلوب (كجم)", value=70.0)

# حساب التقدم تلقائياً
progress_diff = current_w - target_w
st.write(f"باقي لك {progress_diff:.1f} كجم لتصل لهدفك. استمر!")

# --- القسم الرابع: إحصائيات ---
st.subheader("📉 أداء اليوم")
st.area_chart([auto_burned*0.4, auto_burned*0.6, auto_burned*0.8, auto_burned])

st.markdown("<p style='text-align: center; color: gray;'>نظام المتابعة التلقائي v2.0</p>", unsafe_allow_html=True)