import streamlit as st
import pandas as pd
from datetime import datetime
import os  # أضفنا هذه المكتبة للتحقق من وجود الملفات

# 1. إعدادات الصفحة والهوية البصرية
st.set_page_config(page_title="مخيم التميز 2026", page_icon="⛺", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { background-color: #2e7d32; color: white; width: 100%; border-radius: 8px; }
    h1 { color: #1b5e20; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# 2. وظيفة حماية الموقع
def check_password():
    if "password_correct" not in st.session_state:
        st.session_state.password_correct = False
    if not st.session_state.password_correct:
        st.title("🔒 الدخول خاص بجمعية التخييم")
        pwd = st.text_input("أدخل كلمة المرور للمتابعة", type="password")
        if st.button("دخول"):
            if pwd == "Aka2026":
                st.session_state.password_correct = True
                st.rerun()
            else:
                st.error("❌ كلمة المرور خاطئة")
        return False
    return True

if check_password():
    st.title("🌲 جمعية التخييم والتربية: رحلة العمر")
    st.image("https://images.unsplash.com/photo-1504280390367-361c6d9f38f4?auto=format&fit=crop&w=1200&q=80")
    st.markdown("---")

    tab1, tab2, tab3, tab4 = st.tabs(["📋 البرنامج", "🧠 اختبر نفسك", "✍️ التسجيل", "📊 إدارة الجمعية"])

    with tab1:
        st.header("برنامج التميز")
        col1, col2 = st.columns(2)
        with col1: st.info("☀️ **الفترة الصباحية:** رياضات جبلية، ورشات بيئية.")
        with col2: st.success("🌙 **الفترة المسائية:** سهرات تربوية ورصد النجوم.")

    with tab2:
        st.header("🧐 أي نوع من المغامرين أنت؟")
        choice = st.radio("ما هو أكثر شيء تحبه في الغابة؟", ["استكشاف", "مساعدة الأصدقاء", "الطبخ"])
        if st.button("اكتشف شخصيتك"):
            st.success("أنت مغامر حقيقي!")

    with tab3:
        st.header("📝 استمارة التسجيل")
        with st.form("main_form"):
            c1, c2 = st.columns(2)
            with c1:
                name = st.text_input("اسم المغامر الصغير")
                age = st.slider("السن", 7, 17, 12)
            with c2:
                phone = st.text_input("رقم هاتف ولي الأمر")
                city = st.selectbox("المدينة", ["أقا", "طاطا", "أكادير", "أخرى"])
            submit = st.form_submit_button("إرسال الطلب")
            
            if submit:
                new_data = {"الاسم": name, "السن": age, "الهاتف": phone, "المدينة": city, "التاريخ": datetime.now().strftime("%Y-%m-%d")}
                df = pd.DataFrame([new_data])
                
                # تصحيح الخطأ: التحقق من وجود الملف باستخدام مكتبة os
                file_path = "participants.csv"
                file_exists = os.path.isfile(file_path)
                
                df.to_csv(file_path, mode='a', index=False, header=not file_exists, encoding='utf-8-sig')
                st.balloons()
                st.success(f"تم تسجيل {name} بنجاح!")

    with tab4:
        st.header("📂 لوحة الإدارة")
        if os.path.isfile("participants.csv"):
            data = pd.read_csv("participants.csv")
            st.dataframe(data)
            csv = data.to_csv(index=False).encode('utf-8-sig')
            st.download_button("📥 تحميل اللائحة", data=csv, file_name='list_2026.csv', mime='text/csv')
        else:
            st.warning("لا يوجد مسجلون حالياً.")

    st.markdown("---")
    st.markdown("<p style='text-align: center;'>📍 ثانوية أقا الإعدادية | 2026</p>", unsafe_allow_html=True)
