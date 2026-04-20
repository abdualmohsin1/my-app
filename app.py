import streamlit as st
import google.generativeai as genai
from PIL import Image

# إعداد واجهة التطبيق
st.set_page_config(page_title="محلل الوجبات الذكي", layout="centered")

st.title("🥗 محلل الوجبات الذكي")
st.write("صور وجبتك وسأخبرك بالسعرات والبروتين ومدى مناسبتها لهدفك.")

# --- الجزء الجديد: إدخال السعرات المخصص ---
st.sidebar.header("إعدادات المستخدم")
user_goal = st.sidebar.number_input("أدخل هدف سعراتك اليومي:", min_value=500, max_value=5000, value=2100, step=50)
st.sidebar.write(f"الهدف الحالي: {user_goal} سعرة")
# ---------------------------------------

# إعداد مفتاح API (تأكد أنك وضعته في Secrets في Streamlit)
api_key = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=api_key)

# تحميل الصورة
uploaded_file = st.file_input("اختر صورة الوجبة...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="الوجبة التي تم رفعها", use_container_width=True)
    
    submit = st.button("تحليل الوجبة")

    if submit:
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # البرومبت المحدث ليكون تفاعلياً مع هدف المستخدم
        prompt = f"""
        أنت خبير تغذية محترف. قم بتحليل الصورة المرفقة وتقديم تقرير مفصل باللغة العربية يشمل:
        1. أسماء المكونات الموجودة في الوجبة.
        2. تقدير السعرات الحرارية لكل مكون والمجموع الكلي.
        3. كمية البروتين، الكربوهيدرات، والدهون.
        4. نصيحة قصيرة: هل هذه الوجبة مناسبة لشخص هدفه اليومي هو {user_goal} سعرة حرارية؟ 
        (اجعل الأسلوب محفزاً ومختصراً).
        """
        
        with st.spinner("جاري التحليل..."):
            response = model.generate_content([prompt, image])
            st.subheader("النتيجة:")
            st.write(response.text)