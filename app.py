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
