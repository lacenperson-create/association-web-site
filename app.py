import streamlit as st
import pandas as pd
from datetime import datetime
import os
import plotly.express as px

# --- 1. التنسيق الجمالي ---
st.set_page_config(page_title="منصة التشخيص والتميز | ثانوية أقا", page_icon="🔬", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif; text-align: right; }
    .stApp { background: #f0f2f5; }
    .main-card { background: white; padding: 30px; border-radius: 15px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); margin-bottom: 20px; border-right: 8px solid #1a5276; }
    .teacher-card { background: #e8f4f8; padding: 20px; border-radius: 10px; border: 1px solid #1a5276; margin-top: 10px; }
    .stButton>button { background: #1a5276; color: white; border-radius: 20px; width: 100%; }
    </style>
    """, unsafe_allow_html=True)

if 'page' not in st.session_state: st.session_state.page = 'home'

# --- الصفحة الأولى: الواجهة الترحيبية ---
if st.session_state.page == 'home':
    st.markdown('<div class="main-card" style="text-align:center; border-right:none; border-top:8px solid #1a5276;">', unsafe_allow_html=True)
    st.title("🎓 ثانوية أقا الإعدادية")
    st.write("### منصة الأستاذ لحسن للتقويم والتشخيص")
    st.info("هذا الاختبار يهدف لتحديد مستواك ومساعدتنا على تجاوز الصعوبات معاً.")
    if st.button("ابدأ الاختبار الآن 🚀"):
        st.session_state.page = 'login'
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- الصفحة الثانية: معلومات التلميذ ---
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

# --- الصفحة الثالثة: الامتحان وركن الصعوبات ---
elif st.session_state.page == 'exam':
    st.write(f"### 🧪 التلميذ(ة): {st.session_state.info['الاسم']} | القسم: {st.session_state.info['القسم']}")
    
    with st.form("exam_form"):
        # أسئلة الـ QCM (أمثلة)
        st.markdown("#### أولاً: أسئلة الاختبار")
        q1 = st.radio("1. أين يتم انحلال الغليكوز؟", ["الميتوكوندري", "الجبلة الشفافة", "الماتريس"])
        q2 = st.radio("2. كم جزيئة ATP تنتج عن التنفس الخلوي؟", ["2", "38", "4"])
        
        st.markdown("---")
        # خانة الصعوبات (الإضافة الجديدة)
        st.markdown("#### 🚩 ركن التواصل البيداغوجي (اختياري)")
        st.write("أخبرني يا بني/ابنتي: ما هي الدروس أو المفاهيم التي تجد فيها صعوبة في المادة؟")
        student_feedback = st.text_area("أكتب هنا مشاكلك مع المادة أو أي سؤال لم تفهمه جيداً...", placeholder="مثلاً: لم أفهم جيداً دور قنوات الكالسيوم في التقلص العضلي...")

        if st.form_submit_button("إرسال الإجابات النهائية ✅"):
            # حساب النقطة
            score = 0
            if q1 == "الجبلة الشفافة": score += 1
            if q2 == "38": score += 1
            final_grade = (score / 2) * 20
            
            # حفظ البيانات بما فيها الصعوبات
            res = {
                **st.session_state.info, 
                "النقطة": round(final_grade, 2), 
                "الصعوبات": student_feedback if student_feedback else "لا توجد",
                "التوقيت": datetime.now().strftime("%Y-%m-%d %H:%M")
            }
            pd.DataFrame([res]).to_csv("results.csv", mode='a', index=False, header=not os.path.exists("results.csv"), encoding='utf-8-sig')
            st.session_state.page = 'finish'
            st.rerun()

# --- الصفحة الرابعة: شكر ---
elif st.session_state.page == 'finish':
    st.balloons()
    st.markdown('<div class="main-card" style="text-align:center;">', unsafe_allow_html=True)
    st.title("🎉 شكرًا لك!")
    st.success("تم استلام إجاباتك وملاحظاتك بنجاح. سيقوم الأستاذ لحسن بمراجعتها.")
    if st.button("خروج"):
        st.session_state.page = 'home'
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- لوحة تحكم الأستاذ لحسن (تحليل التعثرات) ---
st.markdown("---")
with st.expander("🔐 لوحة التحكم البيداغوجية (الأستاذ لحسن)"):
    if st.text_input("القن السري", type="password") == "Aka2026":
        if os.path.exists("results.csv"):
            data = pd.read_csv("results.csv")
            
            tab_stats, tab_feedback = st.tabs(["📊 نتائج القسم", "🚩 سجل تشخيص التعثرات"])
            
            with tab_stats:
                st.write("### إحصائيات النقط")
                st.dataframe(data[["الاسم", "القسم", "الرقم", "النقطة", "التوقيت"]])
                fig = px.histogram(data, x="النقطة", title="توزيع النقط", color_discrete_sequence=['#1a5276'])
                st.plotly_chart(fig, use_container_width=True)
            
            with tab_feedback:
                st.write("### 🔍 قائمة الصعوبات المسجلة من طرف التلاميذ")
                st.info("هذه الخانة تساعدك على التخطيط لحصص الدعم والمعالجة.")
                # عرض فقط التلاميذ الذين لديهم ملاحظات
                feedback_data = data[data["الصعوبات"] != "لا توجد"][["الاسم", "القسم", "الصعوبات"]]
                if not feedback_data.empty:
                    st.table(feedback_data) # عرض بشكل جدول واضح جداً
                else:
                    st.write("لم يسجل أي تلميذ صعوبات حتى الآن.")
            
            st.download_button("📥 تحميل التقرير الكامل Excel", data.to_csv(index=False).encode('utf-8-sig'), file_name="نتائج_وصعوبات_تلاميذ_أقا.csv")
        else: st.info("لا توجد بيانات حالياً.")
