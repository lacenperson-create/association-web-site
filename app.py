import streamlit as st

# إضافة نظام حماية بسيط
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
                st.error("كلمة المرور خاطئة")
        return False
    return True

if check_password():
    # هنا تضع باقي كود الموقع الذي كتبناه سابقاً
    st.success("مرحباً بك في لوحة تحكم الجمعية")
    # ... (بقية الكود)
import streamlit as st

# 1. إعدادات الهوية البصرية
st.set_page_config(page_title="مخيم التميز 2026", page_icon="⛺", layout="wide")

# تصميم مخصص بالألوان (CSS بسيط)
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stButton>button { background-color: #2e7d32; color: white; border-radius: 10px; }
    h1 { color: #1b5e20; text-align: center; font-family: 'Cairo', sans-serif; }
    </style>
    """, unsafe_allow_html=True)

# 2. رأس الصفحة (Header)
st.title("🌲 جمعية التخييم والتربية: رحلة العمر تبدأ من هنا")
st.write("<h4 style='text-align: center;'>نصنع ذكريات لا تُنسى ونبني جيلاً مسؤولاً</h4>", unsafe_allow_html=True)
st.image("https://images.unsplash.com/photo-1504280390367-361c6d9f38f4?auto=format&fit=crop&w=1200&q=80", caption="أجواء الطبيعة والحرية")

st.markdown("---")

# 3. أقسام تفاعلية (Tabs)
tab1, tab2, tab3 = st.tabs(["📋 برنامج المخيم", "🧠 اختبر نفسك", "✍️ التسجيل السريع"])

with tab1:
    st.header("برنامج التميز")
    col1, col2 = st.columns(2)
    with col1:
        st.info("☀️ **الفترة الصباحية:** رياضات جبلية، ورشات بيئية، وإسعافات أولية.")
    with col2:
        st.success("🌙 **الفترة المسائية:** سهرات تربوية، حكايات شعبية، ورصد النجوم.")

with tab2:
    st.header("🧐 أي نوع من المغامرين أنت؟")
    st.write("أجب على السؤال التالي لتعرف دورك في المخيم:")
    choice = st.radio("ما هو أكثر شيء تحبه في الغابة؟", 
                     ["استكشاف المسارات المجهولة", "مساعدة الأصدقاء وتنظيم المخيم", "إشعال النار وتحضير الطعام"])
    
    if st.button("اكتشف شخصيتك"):
        if "استكشاف" in choice:
            st.warning("🏹 أنت 'المستكشف الجريء'.. مكانك في مقدمة الرحلة!")
        elif "مساعدة" in choice:
            st.success("🤝 أنت 'القائد المتعاون'.. الجمعية تعتمد عليك في التنظيم!")
        else:
            st.info("🔥 أنت 'خبير الحياة البرية'.. الجميع سينتظر مهاراتك!")

with tab3:
    st.header("📝 انضم إلى مغامرتنا")
    with st.form("pro_form"):
        c1, c2 = st.columns(2)
        with c1:
            name = st.text_input("اسم المغامر الصغير")
            age = st.slider("السن", 7, 17, 12)
        with c2:
            phone = st.text_input("رقم هاتف الوالي")
            city = st.selectbox("المدينة", ["أقا", "طاطا", "أكادير", "مدينة أخرى"])
        
        note = st.text_area("ملاحظات خاصة (حالة صحية أو مواهب)")
        submit = st.form_submit_button("إرسال الطلب")
        
        if submit:
            st.balloons()
            st.success(f"تم تسجيل {name} بنجاح! استعد للمغامرة.")

# 4. التذييل (Footer)
st.markdown("---")
st.markdown("<p style='text-align: center;'>📍 مقر الجمعية - ثانوية أقا الإعدادية | صيف 2026</p>", unsafe_allow_html=True)
