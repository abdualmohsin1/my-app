import streamlit as st
import google.generativeai as genai
from PIL import Image
from datetime import datetime

# إعداد الصفحة وتنسيق الألوان الهادئة
st.set_page_config(page_title="لوحة التحكم الصحية", layout="wide")

# إعداد الذكاء الاصطناعي
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("يرجى وضع مفتاح API في Secrets")

# تنسيق CSS احترافي
st.markdown("""
    <style>
    .stMetric { background-color: #111827; padding: 20px; border-radius: 12px; border-bottom: 4px solid #3b82f6; }
    h1, h2, h3 { color: #f3f4f6; }
    .stNumberInput, .stSelectbox { border-radius: 8px; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1>📊 لوحة المتابعة الصحية الدقيقة</h1>", unsafe_allow_html=True)

# --- القسم الأول: إدخال الأرقام الصحيحة ---
with st.sidebar:
    st.header("⚙️ ضبط بيانات اليوم")
    user_steps = st.number_input("أدخل عدد خطواتك الفعلية:", min_value=0, value=0, step=100)
    user_water = st.number_input("كم لتر شربت؟", min_value=0.0, value=0.0, step=0.25)
    st.info("الأرقام في اللوحة ستتحدث فوراً بناءً على ما تدخله هنا.")

# حسابات تلقائية بناءً على مدخلاتك
# السعرات المحروقة (معادلة تقريبية: كل 1000 خطوة تحرق حوالي 40 سعرة)
calculated_burned = int(user_steps * 0.04)

# --- القسم الثاني: عرض اللوحة (التحديث اللحظي) ---
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("### 💧 الماء")
    st.metric("الإجمالي", f"{user_water} L", delta="يومي")

with col2:
    st.markdown("### 👟 الخطوات")
    st.metric("المشي", f"{user_steps:,}", delta="خطوة")

with col3:
    st.markdown("### 📈 التقدم")
    # سيتم ربطها بالوزن في الأسفل
    st.metric("الحالة", "مستمر")

with col4:
    st.markdown("### 🔥 الحرق")
    st.metric("السعرات", f"{calculated_burned} kcal", delta="تلقائي")

st.divider()

# --- القسم الثالث: إدارة الوجبات ---
st.subheader("🍽️ تحليل الوجبات (نظام 2100 سعرة)")
meal_type = st.radio("الوجبة:", ["فطور", "غداء", "سناك", "عشاء"], horizontal=True)

uploaded_file = st.file_uploader(f"ارفع صورة {meal_type}", type=["jpg", "png", "jpeg"])

if uploaded_file:
    img = Image.open(uploaded_file)
    st.image(img, width=400)
    if st.button("تحليل الوجبة"):
        with st.spinner("جاري التحليل..."):
            prompt = f"أنا أتبع نظام 2100 سعرة، بروتين عالي، وأحب بدائل الفول والزبادي. حلل هذه الوجبة ({meal_type}) وأعطني السعرات والبروتين التقريبي."
            response = model.generate_content([prompt, img])
            st.success(response.text)

st.divider()

# --- القسم الرابع: الوزن والإحصائيات ---
col_w1, col_w2 = st.columns(2)
with col_w1:
    current_w = st.number_input("وزنك الحالي (كجم)", value=85.0)
with col_w2:
    target_w = st.number_input("الوزن المطلوب (كجم)", value=70.0)

# حساب الفرق التلقائي
diff = current_w - target_w
st.write(f"### 🎯 الهدف: باقي لك {diff:.1f} كجم للوصول للوزن المطلوب.")

# رسم بياني بسيط
st.area_chart([calculated_burned * 0.5, calculated_burned * 0.8, calculated_burned])