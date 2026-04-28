import streamlit as st
import pandas as pd
from datetime import datetime
import os

# 1. إعدادات الجمالية
st.set_page_config(page_title="منصة QCM | ثانوية أقا", page_icon="🧪", layout="centered")

st.markdown("""
    <style>
    .stApp { background: linear-gradient(to bottom, #eef2f3, #8e9eab); }
    .question-card { background-color: white; padding: 20px; border-radius: 12px; border-right: 6px solid #1a5276; margin-bottom: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    .stRadio > label { font-weight: bold; color: #1a5276; }
    h1 { color: #1a5276; text-align: center; border-bottom: 2px solid #1a5276; padding-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# 2. إدارة التنقل بين الصفحات
if 'page' not in st.session_state: st.session_state.page = 'login'

# --- الصفحة الأولى: المعلومات ---
if st.session_state.page == 'login':
    st.title("ثانوية أقا الإعدادية")
    st.subheader("الأستاذ: لحسن - منصة الفروض الرقمية")
    
    with st.container():
        st.write("### 📝 أدخل معلوماتك للبدء")
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
    st.title("🧪 اختبار QCM: استهلاك المادة العضوية والعضلة")
    st.info(f"الممتحن: {st.session_state.info['الاسم']} | بالتوفيق!")

    score = 0
    
    # قائمة الأسئلة (12 سؤال)
    with st.form("exam_form"):
        # --- استهلاك المادة العضوية (6 أسئلة) ---
        st.header("I. استهلاك المادة العضوية وتدفق الطاقة")
        
        q1 = st.radio("1. أين تتم مرحلة انحلال الغليكوز؟", ["الميتوكوندري", "الجبلة الشفافة", "المركب الإنزيمي"])
        q2 = st.radio("2. ما هو الناتج النهائي لانحلال الغليكوز؟", ["جزيئتان من حمض البيروفيك", "جزيئة واحدة ATP", "الإيثانول"])
        q3 = st.radio("3. كم عدد جزيئات ATP الناتجة عن هدم جزيئة غليكوز واحدة عبر التنفس؟", ["2 ATP", "38 ATP", "4 ATP"])
        q4 = st.radio("4. التخمر اللبني ينتج عنه فضلات عضوية هي:", ["CO2 والماء", "حمض لبني", "كحول إيثيلي"])
        q5 = st.radio("5. أين تحدث دورة كريبس؟", ["الغشاء الخارجي للميتوكوندري", "الماتريس", "الحيز بيغشائي"])
        q6 = st.radio("6. دور الأكسجين في التنفس الخلوي هو:", ["إنتاج CO2", "متقبل نهائي للإلكترونات والبروتونات", "تفكيك الغليكوز"])

        # --- العضلة الهيكلية (6 أسئلة) ---
        st.header("II. العضلة والنشاط العضلي")
        
        q7 = st.radio("7. الوحدة البنيوية والوظيفية لليف العضلي هي:", ["الساركوبلازم", "الساركومير", "الميوزين"])
        q8 = st.radio("8. أي أيونات ضرورية لتحرير مواقع تثبيت الميوزين على الأكتين؟", ["Na+", "Ca2+", "K+"])
        q9 = st.radio("9. أثناء التقلص العضلي، ماذا يحدث للشريط الداكن (A)؟", ["يتقلص طوله", "يبقى طوله ثابتاً", "يختفي تماماً"])
        q10 = st.radio("10. المسلك الأسرع لتجديد ATP في العضلة هو:", ["التنفس", "الفوسفوكرياتين (PC)", "التخمر"])
        q11 = st.radio("11. ماذا تسمى الظاهرة الحرارية المرافقة للتقلص العضلي وتحدث في غياب الأكسجين؟", ["الحرارة المتأخرة", "الحرارة الأولية", "التنفس الخلوي"])
        q12 = st.radio("12. يتكون الخييط الدقيق من البروتينات التالية:", ["الأكتين، التروبونين، التروبوميوزين", "الميوزين فقط", "الأكتين والميوزين"])

        submit = st.form_submit_button("إرسال الإجابات النهائية ✅")
        
        if submit:
            # تصحيح الإجابات وحساب النقطة (مثال بسيط)
            correct_answers = ["الجبلة الشفافة", "جزيئتان من حمض البيروفيك", "38 ATP", "حمض لبني", "الماتريس", "متقبل نهائي للإلكترونات والبروتونات", 
                               "الساركومير", "Ca2+", "يبقى طوله ثابتاً", "الفوسفوكرياتين (PC)", "الحرارة الأولية", "الأكتين، التروبونين، التروبوميوزين"]
            user_answers = [q1, q2, q3, q4, q5, q6, q7, q8, q9, q10, q11, q12]
            
            for u, c in zip(user_answers, correct_answers):
                if u == c: score += 1
            
            final_grade = (score / 12) * 20
            
            # حفظ النتائج
            res = {**st.session_state.info, "النقطة/20": round(final_grade, 2), "التاريخ": datetime.now().strftime("%Y-%m-%d %H:%M")}
            df = pd.DataFrame([res])
            df.to_csv("qcm_results.csv", mode='a', index=False, header=not os.path.exists("qcm_results.csv"), encoding='utf-8-sig')
            
            st.session_state.grade = round(final_grade, 2)
            st.session_state.page = 'result'
            st.rerun()

# --- الصفحة الثالثة: النتيجة ---
elif st.session_state.page == 'result':
    st.balloons()
    st.title("🎉 أحسنت!")
    st.success(f"شكراً {st.session_state.info['الاسم']}. تم إرسال إجاباتك بنجاح.")
    st.metric("نقطتك التقريبية هي:", f"{st.session_state.grade} / 20")
    if st.button("خروج"): 
        st.session_state.page = 'login'
        st.rerun()

# --- لوحة تحكم الأستاذ لحسن ---
st.markdown("---")
with st.expander("🔐 لوحة الأستاذ لحسن (لتحميل النقط)"):
    if st.text_input("القن السري", type="password") == "Aka2026":
        if os.path.exists("qcm_results.csv"):
            data = pd.read_csv("qcm_results.csv")
            st.dataframe(data)
            st.download_button("📥 تحميل لائحة النقط (Excel)", data=data.to_csv(index=False).encode('utf-8-sig'), file_name="نتائج_ثانوية_أقا.csv")
