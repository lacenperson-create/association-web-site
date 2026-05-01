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
    st.write("### فضاء علوم الحياة والأرض - الأستاذ لحسن")
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

# --- الصفحة الثالثة: الفرض وجمع الصعوبات ---
elif st.session_state.page == 'exam':
    st.write(f"🔬 **الممتحن:** {st.session_state.info['الاسم']} | **القسم:** {st.session_state.info['القسم']}")
    
    with st.form("exam_form"):
        # أسئلة نموذجية (يمكنك تعديلها لـ 12 سؤالاً)
        st.markdown("#### ❓ الأسئلة")
        q1 = st.radio("1. أين يتم انحلال الغليكوز؟", ["الميتوكوندري", "الجبلة الشفافة", "الماتريس"])
        q2 = st.radio("2. كم عدد ATP الناتج عن التنفس الخلوي؟", ["2 ATP", "38 ATP", "4 ATP"])
        
        st.markdown("---")
        # خانة الصعوبات (معدلة لتجنب الأخطاء البرمجية)
        st.markdown("#### 🚩 ركن الصعوبات البيداغوجية")
        st.write("ما هي الدروس أو الفقرات التي تجد فيها صعوبة في المادة؟")
        feedback = st.text_area("عبر هنا بكل صراحة عن مشاكلك مع المادة...")

        if st.form_submit_button("إرسال ورقة الإجابة ✅"):
            # التصحيح
            score = 0
            if q1 == "الجبلة الشفافة": score += 1
            if q2 == "38 ATP": score += 1
            final_grade = (score / 2) * 20
            
            # حماية البيانات: إزالة أي رموز قد تفسد ملف CSV
            safe_feedback = feedback.replace(";", " ").replace("\n", " ").strip()
            if not safe_feedback: safe_feedback = "لا توجد"
            
            # تجهيز السجل
            res = {
                "الاسم": st.session_state.info['الاسم'],
                "القسم": st.session_state.info['القسم'],
                "الرقم": st.session_state.info['الرقم'],
                "النقطة": round(final_grade, 2),
                "الصعوبات": safe_feedback,
                "التوقيت": datetime.now().strftime("%Y-%m-%d %H:%M")
            }
            
            # الحفظ باستخدام فاصلة منقوطة لضمان عدم حدوث ParserError
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

# --- لوحة تحكم الأستاذ لحسن (نسخة مطورة بزر دخول) ---
st.markdown("---")
with st.expander("🔐 فضاء الأستاذ لحسن (لوحة القيادة)"):
    
    # التحقق مما إذا كان الأستاذ قد سجل دخوله بالفعل في هذه الجلسة
    if "admin_logged_in" not in st.session_state:
        st.session_state.admin_logged_in = False

    if not st.session_state.admin_logged_in:
        # واجهة تسجيل الدخول للأستاذ
        st.write("### 🔑 تسجيل دخول المشرف")
        admin_pass = st.text_input("أدخل القن السري للمتابعة", type="password")
        
        if st.button("تسجيل الدخول 🔓"):
            if admin_pass == "Aka2026":
                st.session_state.admin_logged_in = True
                st.success("تم التحقق بنجاح!")
                st.rerun()
            else:
                st.error("❌ القن السري غير صحيح، حاول مرة أخرى.")
    
    else:
        # الخروج من لوحة التحكم
        if st.button("تسجيل الخروج 🔒", key="logout_btn"):
            st.session_state.admin_logged_in = False
            st.rerun()
            
        st.markdown("---")
        
        # عرض البيانات بعد تسجيل الدخول الناجح
        if os.path.exists("results.csv"):
            try:
                data = pd.read_csv("results.csv", sep=';')
                
                # أزرار الإدارة
                col_down, col_reset = st.columns([3, 1])
                with col_down:
                    st.download_button("📥 تحميل ملف النتائج (Excel)", 
                                     data.to_csv(index=False, sep=';').encode('utf-8-sig'), 
                                     file_name=f"نتائج_أقا_{datetime.now().strftime('%d_%m')}.csv",
                                     use_container_width=True)
                
                with col_reset:
                    if st.checkbox("تفعيل الحذف ⚠️"):
                        if st.button("🗑️ مسح السجلات", type="primary"):
                            os.remove("results.csv")
                            st.success("تم تصفير البيانات.")
                            st.rerun()

                # التبويبات الإحصائية
                t1, t2, t3 = st.tabs(["📊 الإحصائيات", "🔍 رصد التعثرات", "📋 الجدول الكامل"])
                
                with t1:
                    st.write("### تحليل مستوى القسم")
                    fig = px.histogram(data, x="النقطة", title="توزيع النقط",
                                       color_discrete_sequence=['#1a5276'], template="plotly_white")
                    st.plotly_chart(fig, use_container_width=True)
                    
                    c1, c2 = st.columns(2)
                    c1.metric("عدد المشاركين", f"{len(data)} تلميذ")
                    c2.metric("متوسط النقط", f"{data['النقطة'].mean():.2f} / 20")

                with t2:
                    st.write("### 🔍 سجل الصعوبات البيداغوجية")
                    struggles = data[data["الصعوبات"] != "لا توجد"][["الاسم", "القسم", "الصعوبات"]]
                    if not struggles.empty:
                        st.table(struggles)
                    else:
                        st.info("لا توجد ملاحظات حالياً.")

                with t3:
                    st.dataframe(data, use_container_width=True)

            except Exception as e:
                st.error(f"⚠️ خطأ في الملف: {e}")
                if st.button("إصلاح الملف (مسحه)"):
                    os.remove("results.csv")
                    st.rerun()
        else:
            st.info("ℹ️ لا توجد بيانات مسجلة حالياً.")
