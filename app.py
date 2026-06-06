import streamlit as st
import pandas as pd
from datetime import datetime
import os
import plotly.express as px

# 1. الإعدادات الجمالية المتقدمة
st.set_page_config(page_title="منصة الأستاذ لحسن الرقمية", page_icon="📐", layout="wide")

# تحسين الـ CSS لإعطاء مظهر عصري
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    
    html, body, [class*="css"] { 
        font-family: 'Cairo', sans-serif; 
        text-align: right; 
        direction: rtl; 
    }
    
    .stApp {
        background-color: #f8f9fa;
        background-image: radial-gradient(#2c3e50 0.5px, transparent 0.5px);
        background-size: 30px 30px;
        opacity: 0.95;
    }
    
    .main-card {
        background: white;
        padding: 40px;
        border-radius: 25px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.05);
        margin-bottom: 25px;
        border-top: 10px solid #1a5276;
        transition: transform 0.3s ease;
    }
    
    .main-card:hover {
        transform: translateY(-5px);
    }

    .math-header {
        color: #1a5276;
        font-weight: 700;
        border-right: 5px solid #1a5276;
        padding-right: 15px;
        margin-bottom: 25px;
    }

    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #1a5276 0%, #2980b9 100%);
        color: white;
        border-radius: 15px;
        padding: 10px 25px;
        border: none;
        transition: 0.3s;
    }
    </style>
    """, unsafe_allow_html=True)

# إدارة الحالة (Session State)
if 'page' not in st.session_state: st.session_state.page = 'home'
if 'score' not in st.session_state: st.session_state.score = 0

# --- الصفحة الأولى: الواجهة الترحيبية ---
if st.session_state.page == 'home':
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div class="main-card" style="text-align:center;">', unsafe_allow_html=True)
        st.image("https://img.freepik.com/free-vector/math-cosmology-concept-landing-page_23-2148181463.jpg", use_container_width=True)
        st.title("🏛️ ثانوية أقا الإعدادية")
        st.markdown("<h2 style='color:#1a5276;'>🧮 فضاء الرياضيات الرقمي</h2>", unsafe_allow_html=True)
        st.write("### تحت إشراف الأستاذ لحسن")
        st.success("🎯 منصة تفاعلية لدعم مكتسباتكم في مادة الرياضيات")
        
        if st.button("بدء التحدي الرقمي 🚀"):
            st.session_state.page = 'login'
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# --- الصفحة الثانية: التسجيل ---
elif st.session_state.page == 'login':
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.markdown("<h3 class='math-header'>📝 بطاقة تعريف التلميذ(ة)</h3>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1: name = st.text_input("الاسم الكامل باللغة العربية")
    with c2: s_class = st.selectbox("القسم", ["3/1", "3/2", "3/3", "3/4", "3/5", "3/6"])
    with c3: order = st.number_input("رقم الترتيب", 1, 45, 1)
    
    if st.button("تأكيد الهوية والدخول ✍️"):
        if name and len(name) > 5:
            st.session_state.info = {"الاسم": name, "القسم": s_class, "الرقم": order}
            st.session_state.page = 'exam'
            st.rerun()
        else: st.warning("⚠️ المرجو كتابة الاسم الكامل (ثلاثي) للمتابعة")
    st.markdown('</div>', unsafe_allow_html=True)

# --- الصفحة الثالثة: الاختبار ---
elif st.session_state.page == 'exam':
    st.markdown(f"""
        <div style='background:#1a5276; color:white; padding:15px; border-radius:15px; text-align:center; margin-bottom:20px; box-shadow: 0 4px 12px rgba(0,0,0,0.1);'>
            <b>📍 وضع الاختبار النشط</b> | التلميذ: {st.session_state.info['الاسم']} | القسم: {st.session_state.info['القسم']}
        </div>
    """, unsafe_allow_html=True)
    
    with st.form("exam_form"):
        st.markdown("<h3 class='math-header'>📐 تحدي الذكاء الرياضي</h3>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("##### 💠 محور الجذور المربعة")
            q1 = st.radio("1. ما هو ناتج $ \sqrt{49} $ ؟", ["5", "7", "9"])
            q5 = st.radio("2. ما هو تبسيط $ \sqrt{50} $ ؟", ["$5\sqrt{2}$", "$2\sqrt{5}$", "$10\sqrt{5}$"])
            
            st.markdown("##### 💠 محور النشر والتعميل")
            q2 = st.radio("3. تعميل التعبير $ x^2 - 9 $ هو:", ["$(x-3)(x+3)$", "$(x-3)^2$", "$(x+3)^2$"])
            q11 = st.radio("4. ناتج $ (x+1)^2 $ هو:", ["$x^2+1$", "$x^2+2x+1$", "$x^2+x+1$"])

        with col2:
            st.markdown("##### 💠 محور الهندسة والحساب المثلثي")
            q9 = st.radio("5. مبرهنة فيثاغورس تطبق في المثلث:", ["متساوي الساقين", "قائم الزاوية", "متساوي الأضلاع"])
            q10 = st.radio("6. جيب تمام زاوية حادة (cos) يساوي:", ["المقابل / الوتر", "المجاور / الوتر", "المقابل / المجاور"])
            
            st.markdown("##### 💠 محور القوى والمعادلات")
            q7 = st.radio("7. ناتج القوة $ 5^0 $ هو:", ["0", "1", "5"])
            q12 = st.radio("8. إذا كان $ \sqrt{x} = 4 $ فإن قيمة $ x $ هي:", ["2", "8", "16"])

        st.divider()
        feedback = st.text_area("✍️ ماهي الصعوبات التي توجهها في الرياضيات؟ أخبر الأستاذ هنا:")

        if st.form_submit_button("إرسال ورقة الإجابة ✅"):
            score = 0
            answers = { q1: "7", q2: "$(x-3)(x+3)$", q5: "$5\sqrt{2}$", q7: "1", q9: "قائم الزاوية", q10: "المجاور / الوتر", q11: "$x^2+2x+1$", q12: "16" }
            for q, correct in answers.items():
                if q == correct: score += 1
            
            final_grade = (score / len(answers)) * 20
            res = {
                "الاسم": st.session_state.info['الاسم'],
                "القسم": st.session_state.info['القسم'],
                "الرقم": st.session_state.info['الرقم'],
                "النقطة": round(final_grade, 2),
                "الصعوبات": feedback if feedback else "لا توجد",
                "التوقيت": datetime.now().strftime("%Y-%m-%d %H:%M")
            }
            pd.DataFrame([res]).to_csv("results.csv", mode='a', index=False, header=not os.path.exists("results.csv"), sep=';', encoding='utf-8-sig')
            st.session_state.grade = round(final_grade, 2)
            st.session_state.page = 'finish'
            st.rerun()

# --- الصفحة الرابعة: الخاتمة ---
elif st.session_state.page == 'finish':
    st.balloons()
    st.markdown('<div class="main-card" style="text-align:center;">', unsafe_allow_html=True)
    st.image("https://cdn-icons-png.flaticon.com/512/190/190411.png", width=100)
    st.title("🎉 مبارك النجاح في التحدي!")
    
    score_color = "#27ae60" if st.session_state.grade >= 10 else "#e74c3c"
    st.markdown(f"<h1 style='color:{score_color};'>{st.session_state.grade} / 20</h1>", unsafe_allow_html=True)
    
    st.info(f"البطل(ة) {st.session_state.info['الاسم']}، تم تسجيل إجاباتك بنجاح في قاعدة بيانات الأستاذ لحسن.")
    
    if st.button("الخروج والعودة للرئيسية"):
        st.session_state.page = 'home'
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- لوحة تحكم الأستاذ ---
st.markdown("<br><br>", unsafe_allow_html=True)
with st.expander("🛠️ لوحة تحكم الإدارة (خاصة بالأستاذ)"):
    admin_pass = st.text_input("أدخل القن السري للمشاهدة", type="password")
    if admin_pass == "Aka2026":
        if os.path.exists("results.csv"):
            data = pd.read_csv("results.csv", sep=';', encoding='utf-8-sig')
            
            # إحصائيات سريعة
            c_1, c_2, c_3 = st.columns(3)
            c_1.metric("إجمالي التلاميذ", len(data))
            c_2.metric("متوسط النقط", f"{round(data['النقطة'].mean(), 2)}")
            c_3.metric("نسبة النجاح (+10)", f"{len(data[data['النقطة'] >= 10]) / len(data) * 100:.1f}%")

            t1, t2, t3 = st.tabs(["📊 التحليل البياني", "📋 جدول البيانات", "⚙️ الإدارة"])
            
            with t1:
                col_a, col_b = st.columns(2)
                with col_a:
                    fig1 = px.histogram(data, x="النقطة", title="توزيع المستويات", color_discrete_sequence=['#1a5276'])
                    st.plotly_chart(fig1, use_container_width=True)
                with col_b:
                    fig2 = px.box(data, x="القسم", y="النقطة", title="مقارنة الأقسام", color="القسم")
                    st.plotly_chart(fig2, use_container_width=True)
            
            with t2:
                st.dataframe(data.style.highlight_max(subset=['النقطة'], color='#d4edda'), use_container_width=True)
                st.download_button("📥 تحميل التقرير (Excel)", data.to_csv(index=False).encode('utf-8-sig'), "نتائج_الرياضيات.csv")
                
            with t3:
                if st.button("⚠️ مسح جميع البيانات"):
                    os.remove("results.csv")
                    st.warning("تم حذف قاعدة البيانات.")
                    st.rerun()
        else:
            st.info("لم يتم تسجيل أي بيانات بعد.")
