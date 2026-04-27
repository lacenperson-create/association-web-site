import streamlit as st
import pandas as pd
from datetime import datetime

# 1. إعدادات الصفحة والهوية البصرية
st.set_page_config(page_title="مخيم التميز 2026", page_icon="⛺", layout="wide")

# تصميم مخصص (CSS)
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { background-color: #2e7d32; color: white; width: 100%; border-radius: 8px; }
    h1 { color: #1b5e20; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# 2. وظيفة حماية الموقع (كلمة المرور)
def check_password():
    if "password_correct" not in st.session_state:
        st.session_state.password_correct = False

    if not st.session_state.password_correct:
        st.title("🔒 الدخول خاص بجمعية التخييم")
        pwd = st.text_input("أدخل كلمة المرور للمتابعة", type="password")
        if st.button("دخول"):
            if pwd == "Aka2026": # يمكنك تغيير كلمة المرور هنا
                st.session_state.password_correct = True
                st.rerun()
            else:
                st.error("❌ كلمة المرور خاطئة")
        return False
    return True

# إذا كانت كلمة المرور صحيحة، يعرض المحتوى
if check_password():
    
    # رأس الصفحة
    st.title("🌲 جمعية التخييم والتربية: رحلة العمر")
    st.write("<h4 style='text-align: center;'>نصنع ذكريات لا تُنسى ونبني جيلاً مسؤولاً</h4>", unsafe_allow_html=True)
    st.image("https://images.unsplash.com/photo-1504280390367-361c6d9f38f4?auto=format&fit=crop&w=1200&q=80")

    st.markdown("---")

    # 3. الأقسام التفاعلية
    tab1, tab2, tab3, tab4 = st.tabs(["📋 البرنامج", "🧠 اختبر نفسك", "✍️ التسجيل", "📊 إدارة الجمعية"])

    with tab1:
        st.header("برنامج التميز")
        col1, col2 = st.columns(2)
        with col1:
            st.info("☀️ **الفترة الصباحية:** رياضات جبلية، ورشات بيئية، وإسعافات أولية.")
        with col2:
            st.success("🌙 **الفترة المسائية:** سهرات تربوية، حكايات شعبية، ورصد النجوم.")

    with tab2:
        st.header("🧐 أي نوع من المغامرين أنت؟")
        choice = st.radio("ما هو أكثر شيء تحبه في الغابة؟", 
                         ["استكشاف المسارات المجهولة", "مساعدة الأصدقاء وتنظيم المخيم", "إشعال النار وتحضير الطعام"])
        
        if st.button("اكتشف شخصيتك"):
            if "استكشاف" in choice: st.warning("🏹 أنت 'المستكشف الجريء'!")
            elif "مساعدة" in choice: st.success("🤝 أنت 'القائد المتعاون'!")
            else: st.info("🔥 أنت 'خبير الحياة البرية'!")

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
            
            note = st.text_area("ملاحظات خاصة")
            submit = st.form_submit_button("إرسال الطلب")
            
            if submit:
                # حفظ البيانات في ملف CSV (قاعدة بيانات بسيطة)
                new_data = {"الاسم": name, "السن": age, "الهاتف": phone, "المدينة": city, "ملاحظات": note, "التاريخ": datetime.now().strftime("%Y-%m-%d")}
                df = pd.DataFrame([new_data])
                df.to_csv("participants.csv", mode='a', index=False, header=not st.sidebar.exists("participants.csv"))
                st.balloons()
                st.success(f"تم تسجيل {name} بنجاح!")

    with tab4:
        st.header("📂 لوحة الإدارة (للمسؤولين فقط)")
        st.write("يمكنك هنا تحميل لائحة الأطفال المسجلين لطباعتها.")
        
        try:
            data = pd.read_csv("participants.csv")
            st.dataframe(data) # عرض الجدول في الموقع
            
            # زر التحميل
            csv = data.to_csv(index=False).encode('utf-8-sig') # تدعم العربية في Excel
            st.download_button(
                label="📥 تحميل لائحة المشاركين (Excel/CSV)",
                data=csv,
                file_name='list_participants_2026.csv',
                mime='text/csv',
            )
        except:
            st.warning("لا يوجد مسجلون حالياً.")

    # التذييل
    st.markdown("---")
    st.markdown("<p style='text-align: center;'>📍 مقر الجمعية - ثانوية أقا الإعدادية | صيف 2026</p>", unsafe_allow_html=True)
