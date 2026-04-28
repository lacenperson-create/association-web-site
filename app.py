import streamlit as st
import pandas as pd
from datetime import datetime
import os
import plotly.express as px

# --- 1. إعدادات الهوية والجمالية ---
st.set_page_config(page_title="منصة التميز | ثانوية أقا", page_icon="🎓", layout="wide")

st.markdown("""
    <style>
    /* الخطوط والخلفية */
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif; }
    .stApp { background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); }
    
    /* بطاقة المعلومات */
    .main-card {
        background: white; padding: 40px; border-radius: 20px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.1); border-top: 10px solid #1a5276;
        text-align: center; max-width: 800px; margin: auto;
    }
    
    /* أزرار مخصصة */
    .stButton>button {
        background: linear-gradient(90deg, #1a5276, #2980b9);
        color: white; border: none; padding: 15px 30px;
        border-radius: 30px; font-weight: bold; width: 100%; transition: 0.3s;
    }
    .stButton>button:hover { transform: translateY(-3px); box-shadow: 0 10px 20px rgba(0,0,0,0.2); }
    
    /* إحصائيات الأستاذ */
    .stat-card {
        background: white; padding: 20px; border-radius: 15px;
        border-right: 5px solid #1a5276; text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

# إدارة الصفحات
if 'page' not in st.session_state: st.session_state.page = 'home'

# --- الصفحة الأولى: الواجهة الترحيبية ---
if st.session_state.page == 'home':
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.title("🎓 ثانوية أقا الإعدادية")
    st.subheader("مرحباً بكم في منصة الأستاذ لحسن للاختبارات الرقمية")
    st.write("اختبار QCM تفاعلي في مادة علوم الحياة والأرض")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("السهولة", "📱 هاتف")
    col2.metric("السرعة", "⚡ فوري")
    col3.metric("الدقة", "🎯 آلي")
    
    if st.button("إبدأ الرحلة الآن 🚀"):
        st.session_state.page = 'login'
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- الصفحة الثانية: تسجيل التلميذ ---
elif st.session_state.page == 'login':
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.write("### 📝 سجل معلوماتك للدخول")
    name = st.text_input("الاسم الكامل")
    s_class = st.text_input("القسم")
    order = st.text_input("رقم الترتيب")
    
    if st.button("دخول للامتحان ✍️"):
        if name and s_class and order:
            st.session_state.info = {"الاسم": name, "القسم": s_class, "الرقم": order}
            st.session_state.page = 'exam'
            st.rerun()
        else: st.error("من فضلك أكمل جميع الحقول")
    st.markdown('</div>', unsafe_allow_html=True)

# --- الصفحة الثالثة: الامتحان ---
elif st.session_state.page == 'exam':
    st.markdown(f"### 🧪 الممتحن: {st.session_state.info['الاسم']} | القسم: {st.session_state.info['القسم']}")
    score = 0
    with st.form("quiz_form"):
        st.info("أجب بتركيز، لديك محاولة واحدة فقط.")
        # عينة لـ 3 أسئلة (يمكنك تكرارها لـ 12)
        q1 = st.radio("1. أين تتم مرحلة انحلال الغليكوز؟", ["الميتوكوندري", "الجبلة الشفافة", "الماتريس"])
        q2 = st.radio("2. ما هو الناتج النهائي لانحلال الغليكوز؟", ["جزيئتان حمض البيروفيك", "الماء فقط", "CO2"])
        q3 = st.radio("3. كم عدد جزيئات ATP الناتجة عن هدم غليكوز واحد عبر التنفس؟", ["2 ATP", "38 ATP", "4 ATP"])
        
        if st.form_submit_button("إرسال الإجابات ✅"):
            corrects = ["الجبلة الشفافة", "جزيئتان حمض البيروفيك", "38 ATP"]
            for u, c in zip([q1, q2, q3], corrects):
                if u == c: score += 1
            
            final_grade = (score / 3) * 20
            res = {**st.session_state.info, "النقطة": round(final_grade, 2), "التاريخ": datetime.now().strftime("%Y-%m-%d %H:%M")}
            pd.DataFrame([res]).to_csv("results.csv", mode='a', index=False, header=not os.path.exists("results.csv"), encoding='utf-8-sig')
            st.session_state.grade = round(final_grade, 2)
            st.session_state.page = 'finish'
            st.rerun()

# --- الصفحة الرابعة: النهاية ---
elif st.session_state.page == 'finish':
    st.balloons()
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.title("🎉 أحسنت!")
    st.success(f"لقد أنهيت الاختبار بنجاح يا {st.session_state.info['الاسم']}")
    st.metric("نقطتك المستحقة", f"{st.session_state.grade} / 20")
    if st.button("العودة للرئيسية"):
        st.session_state.page = 'home'
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- لوحة تحكم الأستاذ لحسن (السر السري) ---
st.markdown("---")
with st.expander("🔐 لوحة التحكم الإحصائية (الأستاذ لحسن)"):
    if st.text_input("كلمة السر", type="password") == "Aka2026":
        if os.path.exists("results.csv"):
            data = pd.read_csv("results.csv")
            
            # ملخص سريع (Cards)
            c1, c2, c3 = st.columns(3)
            c1.markdown(f'<div class="stat-card"><h3>👥 المسجلين</h3><h2>{len(data)}</h2></div>', unsafe_allow_html=True)
            c2.markdown(f'<div class="stat-card"><h3>📈 متوسط القسم</h3><h2>{data["النقطة"].mean():.2f}</h2></div>', unsafe_allow_html=True)
            c3.markdown(f'<div class="stat-card"><h3>🔝 أعلى نقطة</h3><h2>{data["النقطة"].max()}</h2></div>', unsafe_allow_html=True)
            
            # المبيانات
            st.write("### 📊 تحليل النتائج")
            fig1 = px.histogram(data, x="النقطة", title="توزيع النقط", nbins=10, color_discrete_sequence=['#1a5276'])
            st.plotly_chart(fig1, use_container_width=True)
            
            st.dataframe(data)
            st.download_button("📥 تحميل النتائج Excel", data.to_csv(index=False).encode('utf-8-sig'), file_name="نتائج_أقا.csv")
        else: st.info("لا توجد بيانات حالياً.")
