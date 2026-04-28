import streamlit as st
import pandas as pd
from datetime import datetime
import os
import plotly.express as px

# --- الإعدادات الجمالية ---
st.set_page_config(page_title="منصة ثانوية أقا الرقمية", page_icon="🔬", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif; text-align: right; }
    .stApp { background: #f0f2f5; }
    .main-card { background: white; padding: 30px; border-radius: 15px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); margin-bottom: 20px; border-right: 8px solid #1a5276; }
    </style>
    """, unsafe_allow_html=True)

if 'page' not in st.session_state: st.session_state.page = 'home'

# --- الصفحة الأولى ---
if st.session_state.page == 'home':
    st.markdown('<div class="main-card" style="text-align:center; border-right:none; border-top:8px solid #1a5276;">', unsafe_allow_html=True)
    st.title("🎓 ثانوية أقا الإعدادية")
    st.write("### منصة الأستاذ لحسن للتقويم والتشخيص")
    if st.button("ابدأ الاختبار الآن 🚀"):
        st.session_state.page = 'login'
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- الصفحة الثانية ---
elif st.session_state.page == 'login':
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.write("### 📝 بيانات التلميذ")
    name = st.text_input("الاسم الكامل")
    s_class = st.text_input("القسم")
    order = st.text_input("رقم الترتيب")
    if st.button("دخول للامتحان ✍️"):
        if name and s_class and order:
            st.session_state.info = {"الاسم": name, "القسم": s_class, "الرقم": order}
            st.session_state.page = 'exam'
            st.rerun()
        else: st.error("يرجى ملء كافة البيانات")
    st.markdown('</div>', unsafe_allow_html=True)

# --- الصفحة الثالثة ---
elif st.session_state.page == 'exam':
    st.write(f"### 🧪 الممتحن: {st.session_state.info['الاسم']}")
    with st.form("exam_form"):
        # عينة لأسئلة 
        q1 = st.radio("1. أين يتم انحلال الغليكوز؟", ["الميتوكوندري", "الجبلة الشفافة", "الماتريس"])
        q2 = st.radio("2. كم جزيئة ATP تنتج عن التنفس الخلوي؟", ["2", "38", "4"])
        
        st.markdown("---")
        st.markdown("#### 🚩 ركن الصعوبات (اختياري)")
        student_feedback = st.text_area("ما هي المفاهيم التي تجد فيها صعوبة؟")

        if st.form_submit_button("إرسال الإجابات ✅"):
            score = 0
            if q1 == "الجبلة الشفافة": score += 1
            if q2 == "38": score += 1
            final_grade = (score / 2) * 20
            
            # تنظيف النص من أي فواصل أو سطور قد تسبب ParserError
            clean_feedback = student_feedback.replace("\n", " ").replace(",", " ").replace("\t", " ")
            
            res = {
                "الاسم": st.session_state.info['الاسم'],
                "القسم": st.session_state.info['القسم'],
                "الرقم": st.session_state.info['الرقم'],
                "النقطة": round(final_grade, 2), 
                "الصعوبات": clean_feedback if clean_feedback.strip() else "لا توجد",
                "التوقيت": datetime.now().strftime("%Y-%m-%d %H:%M")
            }
            
            file_path = "results.csv"
            df = pd.DataFrame([res])
            # نستخدم الفاصلة المنقوطة (sep=';') لتجنب مشاكل الفاصلة العادية
            df.to_csv(file_path, mode='a', index=False, header=not os.path.exists(file_path), sep=';', encoding='utf-8-sig')
            
            st.session_state.page = 'finish'
            st.rerun()

# --- الصفحة الرابعة ---
elif st.session_state.page == 'finish':
    st.balloons()
    st.title("🎉 تم الإرسال بنجاح!")
    if st.button("العودة للرئيسية"):
        st.session_state.page = 'home'
        st.rerun()

# --- لوحة تحكم الأستاذ لحسن ---
st.markdown("---")
with st.expander("🔐 لوحة التحكم البيداغوجية"):
    if st.text_input("القن السري", type="password") == "Aka2026":
        if os.path.exists("results.csv"):
            try:
                # نستخدم نفس الفاصلة المنقوطة للقراءة
                data = pd.read_csv("results.csv", sep=';')
                
                tab_stats, tab_feedback = st.tabs(["📊 النتائج", "🔍 سجل الصعوبات"])
                
                with tab_stats:
                    st.dataframe(data)
                    if "النقطة" in data.columns:
                        fig = px.histogram(data, x="النقطة", title="توزيع النقط")
                        st.plotly_chart(fig)
                
                with tab_feedback:
                    # عرض الصعوبات بشكل واضح
                    feedback_list = data[data["الصعوبات"] != "لا توجد"][["الاسم", "الصعوبات"]]
                    st.table(feedback_list)
                    
            except Exception as e:
                st.error(f"حدث خطأ في قراءة البيانات: {e}")
                st.info("نصيحة: قد يكون هناك سطر تالف في الملف، جرب مسح ملف results.csv من GitHub وابدأ من جديد.")
        else:
            st.info("لا توجد بيانات حالياً.")
