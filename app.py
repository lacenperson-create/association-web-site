import streamlit as st
import pandas as pd
from datetime import datetime
import os
import plotly.express as px # مكتبة للمبيانات الاحترافية

# 1. إعدادات الجمالية
st.set_page_config(page_title="منصة التميز الرقمي | ثانوية أقا", page_icon="📊", layout="centered")

st.markdown("""
    <style>
    .stApp { background: #f4f7f6; }
    .question-card { background-color: white; padding: 20px; border-radius: 12px; margin-bottom: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
    h1 { color: #1a5276; text-align: center; font-family: 'Cairo', sans-serif; }
    </style>
    """, unsafe_allow_html=True)

if 'page' not in st.session_state: st.session_state.page = 'login'

# --- الصفحة الأولى: المعلومات ---
if st.session_state.page == 'login':
    st.title("ثانوية أقا الإعدادية")
    st.subheader("الفرض الرقمي المحروس - مادة علوم الحياة والأرض")
    with st.container():
        st.write("### 👤 أدخل معلوماتك للبدء")
        name = st.text_input("الاسم الكامل")
        s_class = st.text_input("القسم")
        order = st.text_input("رقم الترتيب")
        if st.button("دخول للاختبار 🚀"):
            if name and s_class and order:
                st.session_state.info = {"الاسم": name, "القسم": s_class, "الرقم": order}
                st.session_state.page = 'exam'
                st.rerun()
            else: st.error("أدخل بياناتك كاملة!")

# --- الصفحة الثانية: الامتحان (12 سؤال QCM) ---
elif st.session_state.page == 'exam':
    st.title("📝 اختبار QCM التفاعلي")
    score = 0
    with st.form("exam_form"):
        # (وضعت لك هنا عينة من الأسئلة، يمكنك تكرارها لتصل لـ 12 سؤالاً كما في الكود السابق)
        q1 = st.radio("1. أين تتم مرحلة انحلال الغليكوز؟", ["الميتوكوندري", "الجبلة الشفافة", "المركب الإنزيمي"])
        q2 = st.radio("2. ما هو الناتج النهائي لانحلال الغليكوز؟", ["جزيئتان من حمض البيروفيك", "جزيئة واحدة ATP", "الإيثانول"])
        # ... بقية الأسئلة الـ 12 ...
        
        submit = st.form_submit_button("إرسال الإجابات ✅")
        if submit:
            correct_ans = ["الجبلة الشفافة", "جزيئتان من حمض البيروفيك"] # أضف بقية الأجوبة الصحيحة هنا
            user_ans = [q1, q2]
            for u, c in zip(user_ans, correct_ans):
                if u == c: score += 1
            
            final_grade = (score / 2) * 20 # عدل الرقم 2 إلى 12 حسب عدد أسئلتك
            res = {**st.session_state.info, "النقطة": round(final_grade, 2), "التاريخ": datetime.now().strftime("%Y-%m-%d %H:%M")}
            df = pd.DataFrame([res])
            df.to_csv("qcm_results.csv", mode='a', index=False, header=not os.path.exists("qcm_results.csv"), encoding='utf-8-sig')
            st.session_state.grade = round(final_grade, 2)
            st.session_state.page = 'result'
            st.rerun()

# --- الصفحة الثالثة: النتيجة للتلميذ ---
elif st.session_state.page == 'result':
    st.balloons()
    st.title("🎉 تم الإرسال!")
    st.success(f"شكراً {st.session_state.info['الاسم']}. نقطتك هي: {st.session_state.grade} / 20")
    if st.button("خروج"): 
        st.session_state.page = 'login'
        st.rerun()

# --- لوحة تحكم الأستاذ لحسن (مع المبيانات) ---
st.markdown("---")
with st.expander("🔐 لوحة تحكم الأستاذ لحسن (النتائج والإحصائيات)"):
    if st.text_input("القن السري", type="password") == "Aka2026":
        if os.path.exists("qcm_results.csv"):
            data = pd.read_csv("qcm_results.csv")
            
            # --- عرض المبيانات الإحصائية ---
            st.write("### 📊 التحليل الإحصائي لنتائج القسم")
            col_chart1, col_chart2 = st.columns(2)
            
            with col_chart1:
                # مبيان توزيع النقط
                fig1 = px.histogram(data, x="النقطة", title="توزيع النقط", color_discrete_sequence=['#1a5276'])
                st.plotly_chart(fig1, use_container_width=True)
            
            with col_chart2:
                # مبيان دائري للميزات
                def get_miza(n):
                    if n >= 16: return "حسن جداً"
                    elif n >= 14: return "حسن"
                    elif n >= 12: return "مستحسن"
                    elif n >= 10: return "مقبول"
                    else: return "تعثر"
                
                data['الميزة'] = data['النقطة'].apply(get_miza)
                fig2 = px.pie(data, names='الميزة', title="نسبة الميزات في القسم", hole=0.3)
                st.plotly_chart(fig2, use_container_width=True)

            st.write("### 📋 جدول النتائج التفصيلي")
            st.dataframe(data)
            st.download_button("📥 تحميل ملف Excel", data=data.to_csv(index=False).encode('utf-8-sig'), file_name="نتائج_ثانوية_أقا.csv")
        else:
            st.info("لا توجد بيانات حالياً.")
