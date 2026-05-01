import streamlit as st
import pandas as pd
from datetime import datetime
import os
import plotly.express as px

# 1. الإعدادات الجمالية (ألوان ثانوية أقا)
st.set_page_config(page_title="منصة الأستاذ لحسن الرقمية", page_icon="🧬", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif; text-align: right; direction: rtl; }
    .stApp { background: #f8f9fa; }
    .main-card { background: white; padding: 25px; border-radius: 15px; box-shadow: 0 4px 10px rgba(0,0,0,0.05); margin-bottom: 20px; border-top: 5px solid #1a5276; }
    .stButton>button { background: #1a5276; color: white; border-radius: 25px; height: 3em; width: 100%; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

if 'page' not in st.session_state: st.session_state.page = 'home'

# --- الصفحة الأولى: الواجهة ---
if st.session_state.page == 'home':
    st.markdown('<div class="main-card" style="text-align:center;">', unsafe_allow_html=True)
    st.title("🎓 ثانوية أقا الإعدادية")
    st.write("### فضاء الرياضيات - الأستاذ لحسن")
    st.success("أهلاً بك يا بطل! هذا الاختبار سيساعدنا على فهم مستواك ومعالجة تعثراتك.")
    if st.button("انطلاق 🚀"):
        st.session_state.page = 'login'
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- الصفحة الثانية: التسجيل ---
elif st.session_state.page == 'login':
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.write("### 📝 بطاقة تعريف التلميذ")
    c1, c2, c3 = st.columns(3)
    with c1: name = st.text_input("الاسم الكامل")
    with c2: s_class = st.text_input("القسم")
    with c3: order = st.text_input("رقم الترتيب")
    
    if st.button("دخول الاختبار ✍️"):
        if name and s_class and order:
            st.session_state.info = {"الاسم": name, "القسم": s_class, "الرقم": order}
            st.session_state.page = 'exam'
            st.rerun()
        else: st.error("⚠️ المرجو ملء جميع الخانات")
    st.markdown('</div>', unsafe_allow_html=True)

# --- الصفحة الثالثة: فرض الرياضيات (الثالثة إعدادي) ---
elif st.session_state.page == 'exam':
    st.write(f"📐 **التلميذ(ة):** {st.session_state.info['الاسم']} | **القسم:** {st.session_state.info['القسم']}")
    
    with st.form("exam_form"):
        st.markdown("### 📝 اختبار QCM في الرياضيات")
        st.info("اختر الجواب الصحيح لكل سؤال (النقطة على 20)")
        
        # --- الأسئلة الـ 12 ---
        col1, col2 = st.columns(2)
        
        with col1:
            q1 = st.radio("1. ما هو ناتج $ \sqrt{49} $ ؟", ["5", "7", "9"])
            q2 = st.radio("2. ما هو تعميل التعبير $ x^2 - 9 $ ؟", ["$(x-3)(x+3)$", "$(x-3)^2$", "$(x+3)^2$"])
            q3 = st.radio("3. القيمة المقربة للعدد $ \pi $ هي:", ["3.12", "3.14", "3.16"])
            q4 = st.radio("4. ناتج $ (2\sqrt{3})^2 $ هو:", ["6", "12", "18"])
            q5 = st.radio("5. ما هو تبسيط $ \sqrt{50} $ ؟", ["$5\sqrt{2}$", "$2\sqrt{5}$", "$10\sqrt{5}$"])
            q6 = st.radio("6. الكتابة العلمية للعدد $ 0.0005 $ هي:", ["$5 \times 10^{-4}$", "$5 \times 10^4$", "$0.5 \times 10^{-3}$"])

        with col2:
            q7 = st.radio("7. ناتج $ 5^0 $ هو:", ["0", "1", "5"])
            q8 = st.radio("8. حل المعادلة $ 2x = 10 $ هو:", ["x = 2", "x = 5", "x = 8"])
            q9 = st.radio("9. مبرهنة فيثاغورس تطبق في المثلث:", ["متساوي الساقين", "قائم الزاوية", "متساوي الأضلاع"])
            q10 = st.radio("10. جيب تمام زاوية حادة (cos) يساوي:", ["المقابل / الوتر", "المجاور / الوتر", "المقابل / المجاور"])
            q11 = st.radio("11. ناتج $ (x+1)^2 $ هو:", ["$x^2+1$", "$x^2+2x+1$", "$x^2+x+1$"])
            q12 = st.radio("12. إذا كان $ \sqrt{x} = 4 $ فإن $ x $ يساوي:", ["2", "8", "16"])

        st.markdown("---")
        # خانة الصعوبات البيداغوجية
        st.markdown("#### 🚩 ركن الصعوبات")
        feedback = st.text_area("ما هي الدروس التي تجد فيها صعوبة في الرياضيات؟ (مثلاً: الجذور، النشر، التعميل...)")

        if st.form_submit_button("إرسال ورقة الإجابة ✅"):
            # --- نظام التصحيح الآلي ---
            score = 0
            # الأجوبة الصحيحة
            answers = {
                q1: "7", q2: "$(x-3)(x+3)$", q3: "3.14", q4: "12", 
                q5: "$5\sqrt{2}$", q6: "$5 \times 10^{-4}$", q7: "1", 
                q8: "5", q9: "قائم الزاوية", q10: "المجاور / الوتر", 
                q11: "$x^2+2x+1$", q12: "16"
            }
            
            for q, correct in answers.items():
                if q == correct: score += 1
            
            # حساب النقطة من 20
            final_grade = (score / 12) * 20
            
            # حماية وتجهيز البيانات
            safe_feedback = feedback.replace(";", " ").replace("\n", " ").strip()
            if not safe_feedback: safe_feedback = "لا توجد"
            
            res = {
                "الاسم": st.session_state.info['الاسم'],
                "القسم": st.session_state.info['القسم'],
                "الرقم": st.session_state.info['الرقم'],
                "النقطة": round(final_grade, 2),
                "الصعوبات": safe_feedback,
                "التوقيت": datetime.now().strftime("%Y-%m-%d %H:%M")
            }
            
            # حفظ النتائج
            df = pd.DataFrame([res])
            df.to_csv("results.csv", mode='a', index=False, header=not os.path.exists("results.csv"), sep=';', encoding='utf-8-sig')
            
            st.session_state.grade = round(final_grade, 2)
            st.session_state.page = 'finish'
            st.rerun()

# --- الصفحة الرابعة: شكر ---
elif st.session_state.page == 'finish':
    st.balloons()
    st.markdown('<div class="main-card" style="text-align:center;">', unsafe_allow_html=True)
    st.title("🎉 أحسنت!")
    st.success(f"شكراً {st.session_state.info['الاسم']}. لقد تم تسجيل إجاباتك بنجاح.")
    st.info(f"نقطتك التقريبية هي: {st.session_state.grade} / 20")
    if st.button("العودة للرئيسية"):
        st.session_state.page = 'home'
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

from fpdf import FPDF # أضف هذا السطر في أعلى الملف مع المكتبات الأخرى

# --- لوحة تحكم الأستاذ لحسن (نسخة مطورة مع PDF) ---
st.markdown("---")
with st.expander("🔐 فضاء الأستاذ لحسن (التقارير والإحصائيات)"):
    
    if "admin_logged_in" not in st.session_state:
        st.session_state.admin_logged_in = False

    if not st.session_state.admin_logged_in:
        st.write("### 🔑 تسجيل دخول المشرف")
        admin_pass = st.text_input("أدخل القن السري", type="password")
        if st.button("دخول 🔓"):
            if admin_pass == "Aka2026":
                st.session_state.admin_logged_in = True
                st.rerun()
            else: st.error("❌ كلمة المرور خاطئة")
    
    else:
        if st.button("تسجيل الخروج 🔒"):
            st.session_state.admin_logged_in = False
            st.rerun()
            
        if os.path.exists("results.csv"):
            try:
                data = pd.read_csv("results.csv", sep=';')
                
                # --- وظيفة إنشاء ملف PDF ---
                def create_pdf(df):
                    pdf = FPDF()
                    pdf.add_page()
                    # إضافة خط يدعم العربية أو الاكتفاء بالعناوين اللاتينية لضمان التوافق
                    pdf.set_font("Arial", 'B', 16)
                    pdf.cell(200, 10, txt="Class Results Report - Aka School", ln=True, align='C')
                    pdf.ln(10)
                    
                    pdf.set_font("Arial", size=10)
                    # رؤوس الجدول
                    pdf.cell(40, 10, "Name", border=1)
                    pdf.cell(20, 10, "Class", border=1)
                    pdf.cell(20, 10, "Grade", border=1)
                    pdf.cell(100, 10, "Difficulties", border=1)
                    pdf.ln()
                    
                    for i in range(len(df)):
                        pdf.cell(40, 10, str(df.iloc[i]['الاسم'])[:20], border=1)
                        pdf.cell(20, 10, str(df.iloc[i]['القسم']), border=1)
                        pdf.cell(20, 10, str(df.iloc[i]['النقطة']), border=1)
                        pdf.cell(100, 10, str(df.iloc[i]['الصعوبات'])[:50], border=1)
                        pdf.ln()
                    return pdf.output(dest='S').encode('latin-1')

                # --- أزرار التحميل ---
                col_pdf, col_excel, col_reset = st.columns([1, 1, 1])
                
                with col_pdf:
                    pdf_data = create_pdf(data)
                    st.download_button("📄 تحميل تقرير PDF", 
                                     data=pdf_data, 
                                     file_name="results_report.pdf",
                                     mime="application/pdf",
                                     use_container_width=True)
                
                with col_excel:
                    st.download_button("📊 تحميل ملف Excel", 
                                     data=data.to_csv(index=False, sep=';').encode('utf-8-sig'), 
                                     file_name="results_excel.csv",
                                     use_container_width=True)

                with col_reset:
                    if st.checkbox("تفعيل الحذف"):
                        if st.button("🗑️ مسح السجلات", type="primary"):
                            os.remove("results.csv")
                            st.rerun()

                # عرض البيانات والمبيانات
                t1, t2 = st.tabs(["📊 الإحصائيات", "📋 النتائج الكاملة"])
                with t1:
                    fig = px.histogram(data, x="النقطة", title="توزيع النقط", color_discrete_sequence=['#1a5276'])
                    st.plotly_chart(fig, use_container_width=True)
                with t2:
                    st.dataframe(data, use_container_width=True)

            except Exception as e:
                st.error(f"حدث خطأ: {e}")
        else:
            st.info("لا توجد بيانات حالياً.")
