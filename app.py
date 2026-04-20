import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. إعداد المفتاح
genai.configure(api_key="‫AIzaSyD6qQux8tyY_KpLK_6aNvNBeyu_OWAQoFs‬")

# 2. تعريف إعدادات الأمان (تجعل الموديل يحلل كل شيء دون قيود مفرطة)
safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
]

st.set_page_config(page_title="مساعد التغذية الذكي", page_icon="🥗")
st.title("🥗 مساعدي الغذائي (هدف 2100 سعرة)")

uploaded_file = st.file_uploader("ارفع صورة وجبتك...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='الوجبة المراد تحليلها')
    
    if st.button('تحليل الوجبة الآن 🚀'):
        with st.spinner('🔍 جاري الفحص السريع...'):
            # 3. دمج إعدادات الأمان في الموديل
            model = genai.GenerativeModel(
                model_name='models/gemini-1.5-flash',
                safety_settings=safety_settings
            )
            
            prompt = "حلل هذه الوجبة بدقة: اذكر السعرات والبروتين. هل تناسب نظام 2100 سعرة؟ كن مباشراً ومختصراً."
            
            try:
                response = model.generate_content([prompt, image])
                st.success("النتيجة:")
                st.write(response.text)
            except Exception as e:
                st.error(f"حدث خطأ: {e}")