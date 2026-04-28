import streamlit as st
import pandas as pd
from datetime import datetime
import os

# 1. إعدادات الجمالية والألوان
st.set_page_config(page_title="منصة التميز الرقمي | ثانوية أقا", page_icon="🎓", layout="centered")

# تصميم CSS مخصص لجعل الواجهة "تسر الناظرين"
st.markdown("""
    <style>
    /* خلفية الصفحة */
    .stApp {
        background: linear-gradient(to bottom, #f0f4f8, #d9e2ec);
    }
    /* حاوية معلومات التلميذ */
    .student-info-card {
        background-color: white;
        padding: 30px;
        border-radius: 15px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        border-top: 8px solid #2c3e50;
        margin-bottom: 20px;
    }
    /* تصميم الأزرار */
    .stButton>button {
        background: linear-gradient(45deg, #2c3e50, #34495e);
        color: white;
        font-size: 20px;
        padding: 10px 25px;
        border-radius: 50px;
        transition: 0.3s;
    }
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    h1 { color: #2c3e50; font-family: 'Cairo', sans-serif; }
    </style>
    """, unsafe_allow_html=True)

# 2. إدارة الحالة (Navigation)
if 'page' not in st.session_state:
    st.session_state.page = 'login'

# --- الصفحة الأولى: معلومات التلميذ ---
if st.session_state.page == 'login':
    st.image("https://img.icons8.com/fluent/96/000000/education.png", width=100)
    st.title("ثانوية أقا الإعدادية")
    st.subheader("مرحباً بك في منصة الاختبارات الرقمية")
    
    st.markdown('<div class="student-info-card">', unsafe_allow_html=True)
    st.write("### 👤 تسجيل الدخول للاختبار")
    st_name = st.text_input("الاسم الكامل للتلميذ(ة)")
    st_class = st.text_input("القسم")
    st_order = st.text_input("رقم الترتيب")
    
    st.warning("⚠️ تأكد من صحة معلوماتك قبل الدخول، لا يمكنك تغييرها لاحقاً.")
    
    if st.button("🚀 ابدأ الامتحان الآن"):
        if st_name and st_class and st_order:
            st.session_state.user_name = st_name
            st.session_state.user_class = st_class
            st.session_state.user_order = st_order
            st.session_state.page = 'exam'
            st.rerun()
        else:
            st.error("من فضلك أدخل جميع المعلومات المطلوبة.")
    st.markdown('</div>', unsafe_allow_html=True)

# --- الصفحة الثانية: الامتحان ---
elif st.session_state.page == 'exam':
    # ترويسة جانبية بسيطة لمعلومات التلميذ
    st.sidebar.success(f"الممتحن: {st.session_state.user_name}")
    st.sidebar.info(f"القسم: {st.session_state.user_class} | رقم: {st.session_state.user_order}")
    
    st.title("📝 الفرض المحروس رقم 1")
    st.write(f"**المادة:** علوم الحياة والأرض | **تحت إشراف الأستاذ:** لحسن")
    
    st.markdown("---")
    
    # التمرين الثاني
    with st.expander("🔬 التمرين الثاني: تحويل الطاقة عند الخميرة", expanded=True):
        st.write("**السؤال 1:** اقترح فرضية حول نوع التفاعلات لإنتاج الطاقة عند السلالتين G و P.")
        ans1 = st.text_area("إجابتك هنا...", key="ex_q1")
        
        st.write("**السؤال 2:** حدد معللاً إجابتك الظواهر الاستقلابية المسؤولة.")
        ans2 = st.text_area("إجابتك هنا...", key="ex_q2")

    # التمرين الثالث
    with st.expander("💪 التمرين الثالث: النشاط العضلي", expanded=True):
        st.write("**السؤال 3:** حلل النتائج وفسر تطورات الحمض اللبني و PC.")
        ans3 = st.text_area("إجابتك هنا...", key="ex_q3")

    if st.button("✅ إنهاء الامتحان وإرسال الإجابات"):
        # حفظ البيانات
        result = {
            "التوقيت": datetime.now().strftime("%H:%M:%S"),
            "الاسم": st.session_state.user_name,
            "القسم": st.session_state.user_class,
            "الرقم": st.session_state.user_order,
            "س1": ans1, "س2": ans2, "س3": ans3
        }
        df = pd.DataFrame([result])
        df.to_csv("exam_results.csv", mode='a', index=False, header=not os.path.exists("exam_results.csv"), encoding='utf-8-sig')
        
        st.balloons()
        st.session_state.page = 'finish'
        st.rerun()

# --- الصفحة الثالثة: النهاية ---
elif st.session_state.page == 'finish':
    st.balloons()
    st.title("🎉 تم الإرسال بنجاح!")
    st.success(f"شكراً لك يا {st.session_state.user_name}، لقد تم حفظ إجاباتك وإرسالها للأستاذ لحسن.")
    if st.button("العودة للرئيسية"):
        st.session_state.page = 'login'
        st.rerun()

# --- لوحة تحكم الأستاذ (تظهر دائماً في الأسفل بشكل مخفي) ---
st.markdown("---")
with st.expander("🛠️ لوحة تحكم الأستاذ لحسن (للمشرف فقط)"):
    admin_pwd = st.text_input("أدخل القن السري", type="password")
    if admin_pwd == "Aka2026":
        if os.path.exists("exam_results.csv"):
            data = pd.read_csv("exam_results.csv")
            st.write("### أعمال التلاميذ المسجلة:")
            st.dataframe(data)
            csv = data.to_csv(index=False).encode('utf-8-sig')
            st.download_button("📥 تحميل النتائج في ملف Excel", data=csv, file_name='نتائج_تلاميذ_أقا.csv')
        else:
            st.info("لا توجد أعمال مصححة بعد.")
