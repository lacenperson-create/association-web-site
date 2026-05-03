import streamlit as st
import pandas as pd
from datetime import datetime
import os
import plotly.express as px

# 1. الإعدادات الجمالية المتقدمة
st.set_page_config(page_title="منصة الأستاذ لحسن الرقمية", page_icon="📐", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    
    html, body, [class*="css"] { 
        font-family: 'Cairo', sans-serif; 
        text-align: right; 
        direction: rtl; 
    }
    
    /* خلفية رياضية خفيفة */
    .stApp {
        background-color: #f0f2f6;
        background-image: radial-gradient(#1a5276 0.5px, transparent 0.5px);
        background-size: 30px 30px;
        background-opacity: 0.05;
    }
    
    .main-card {
        background: rgba(255, 255, 255, 0.95);
        padding: 30px;
        border-radius: 20px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        margin-bottom: 25px;
        border-right: 8px solid #1a5276;
    }
    
    .math-header {
        color: #1a5276;
        border-bottom: 2px solid #eaeaea;
        padding-bottom: 10px;
        margin-bottom: 20px;
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #1a5276 0%, #2980b9 100%);
        color: white;
        border-radius: 12px;
        border: none;
        transition: all 0.3s;
        font-weight: bold;
        font-size: 18px;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(26, 82, 118, 0.3);
    }
    </style>
    """, unsafe_allow_html=True)

if 'page' not in st.session_state: st.session_state.page = 'home'

# --- الصفحة الأولى: الواجهة الترحيبية ---
if st.session_state.page == 'home':
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div class="main-card" style="text-align:center;">', unsafe_allow_html=True)
        # صورة ترحيبية رياضية (يمكنك استبدال الرابط بصورة logo.png إذا رفعتها)
        st.image("https://img.freepik.com/free-vector/math-cosmology-concept-landing-page_23-2148181463.jpg", use_container_width=True)
        st.title("🏛️ ثانوية أقا الإعدادية")
        st.markdown("<h2 style='color:#1a5276;'>🧮 فضاء الرياضيات الرقمي</h2>", unsafe_allow_html=True)
        st.write("#### تحت إشراف الأستاذ لحسن")
        st.info("مرحباً بك في المنصة الذكية لتقييم المكتسبات ودعم التعثرات في مادة الرياضيات.")
        
        if st.button("ابدأ رحلة التحدي الآن 🚀"):
            st.session_state.page = 'login'
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# --- الصفحة الثانية: التسجيل ---
elif st.session_state.page == 'login':
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.markdown("<h3 class='math-header'>📝 معلومات الفارس(ة)</h3>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1: name = st.text_input("الاسم الكامل باللغة العربية")
    with c2: s_class = st.selectbox("القسم", ["3/1", "3/2", "3/3", "3/4", "3/5", "3/6"])
    with c3: order = st.number_input("رقم الترتيب", min_value=1, max_value=45, step=1)
    
    if st.button("تأكيد الدخول ✍️"):
        if name:
            st.session_state.info = {"الاسم": name, "القسم": s_class, "الرقم": order}
            st.session_state.page = 'exam'
            st.rerun()
        else: st.error("⚠️ المرجو كتابة اسمك للمتابعة")
    st.markdown('</div>', unsafe_allow_html=True)

# --- الصفحة الثالثة: الاختبار ---
elif st.session_state.page == 'exam':
    st.markdown(f"""
        <div style='background:#1a5276; color:white; padding:10px; border-radius:10px; text-align:center; margin-bottom:20px;'>
            ✅ أنت الآن في وضع الاختبار | التلميذ: {st.session_state.info['الاسم']} | القسم: {st.session_state.info['القسم']}
        </div>
    """, unsafe_allow_html=True)
    
    with st.form("exam_form"):
        st.markdown("<h3 class='math-header'>📐 تحدي الذكاء الرياضي (QCM)</h3>", unsafe_allow_html=True)
        
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

        st.markdown("---")
        st.markdown("#### 🚩 ركن التواصل البيداغوجي")
        feedback = st.text_area("أستاذي، أحتاج للمساعدة في دروس: (اكتب هنا ما يواجهك من صعوبات)")

        if st.form_submit_button("إرسال ورقة الإجابة ✅"):
            # نظام التصحيح (بناءً على 8 أسئلة كمثال للتبسيط)
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
            df = pd.DataFrame([res])
            df.to_csv("results.csv", mode='a', index=False, header=not os.path.exists("results.csv"), sep=';', encoding='utf-8-sig')
            
            st.session_state.grade = round(final_grade, 2)
            st.session_state.page = 'finish'
            st.rerun()

# --- الصفحة الرابعة: الخاتمة ---
elif st.session_state.page == 'finish':
    st.balloons()
    st.markdown('<div class="main-card" style="text-align:center;">', unsafe_allow_html=True)
    st.image("https://cdn-icons-png.flaticon.com/512/190/190411.png", width=100)
    st.title("🎉 عمل رائع!")
    st.success(f"البطل(ة) {st.session_state.info['الاسم']}، لقد أنهيت المهمة بنجاح.")
    
    c1, c2 = st.columns(2)
    with c1: st.metric("نقطتك المستحقة", f"{st.session_state.grade} / 20")
    with c2: st.info("سيقوم الأستاذ لحسن بمراجعة إجاباتك قريباً.")
    
    if st.button("الخروج والعودة للرئيسية"):
        st.session_state.page = 'home'
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- لوحة تحكم الأستاذ (بدون تغيير في المنطق، فقط تحسين الواجهة) ---
st.markdown("<br><br>", unsafe_allow_html=True)
with st.expander("🛠️ لوحة تحكم الأستاذ (خاص)"):
    # ... (نفس كود الإدارة السابق مع القن Aka2026)
    admin_pass = st.text_input("القن السري", type="password")
    if admin_pass == "Aka2026":
        if os.path.exists("results.csv"):
            data = pd.read_csv("results.csv", sep=';', encoding='utf-8-sig')
            st.write("### 📈 ملخص أداء المؤسسة")
            st.dataframe(data)
            # زر التحميل المنسق (كما في الكود السابق)
            st.download_button("📥 تحميل التقرير الرسمي", data.to_csv(index=False, sep=';').encode('utf-8-sig'), "report.csv")
            # --- داخل لوحة تحكم الأستاذ بعد التأكد من تسجيل الدخول وقراءة البيانات ---
if os.path.exists("results.csv"):
    try:
        data = pd.read_csv("results.csv", sep=';', encoding='utf-8-sig')
        
        # --- 1. فقرة المؤشرات السريعة ---
        st.markdown("### 📊 لوحة قيادة الأداء")
        col_m1, col_m2, col_m3, col_m4 = st.columns(4)
        
        with col_m1:
            st.metric("عدد المشاركين", f"{len(data)} تلميذ")
        with col_m2:
            st.metric("متوسط النقط", f"{round(data['النقطة'].mean(), 2)} / 20")
        with col_m3:
            st.metric("أعلى نقطة", f"{data['النقطة'].max()} / 20")
        with col_m4:
            st.metric("أدنى نقطة", f"{data['النقطة'].min()} / 20")

        st.divider()

        # --- 2. فقرة الرسوم البيانية ---
        tab_charts, tab_struggles, tab_details = st.tabs(["📈 تحليل النقط", "🔍 رصد التعثرات", "📋 لائحة النتائج"])

        with tab_charts:
            col_chart1, col_chart2 = st.columns(2)
            
            with col_chart1:
                # مبيان توزيع النقط
                fig_hist = px.histogram(data, x="النقطة", 
                                       title="توزيع معدلات التلاميذ",
                                       labels={'النقطة': 'المعدل', 'count': 'عدد التلاميذ'},
                                       color_discrete_sequence=['#1a5276'],
                                       template="plotly_white")
                st.plotly_chart(fig_hist, use_container_width=True)
            
            with col_chart2:
                # مبيان المقارنة حسب الأقسام
                avg_by_class = data.groupby('القسم')['النقطة'].mean().reset_index()
                fig_bar = px.bar(avg_by_class, x='القسم', y='النقطة', 
                                title="متوسط النقط حسب الأقسام",
                                color='النقطة', 
                                color_continuous_scale='RdYlGn')
                st.plotly_chart(fig_bar, use_container_width=True)

        with tab_struggles:
            st.markdown("#### 🚩 سجل الصعوبات المصرح بها")
            # استخراج الكلمات المفتاحية الأكثر تكراراً في التعثرات
            struggles_list = data[data["الصعوبات"] != "لا توجد"][["الاسم", "القسم", "الصعوبات"]]
            if not struggles_list.empty:
                st.dataframe(struggles_list, use_container_width=True)
            else:
                st.info("لم يتم تسجيل أي صعوبات من طرف التلاميذ حتى الآن.")

        with tab_details:
            st.markdown("#### 📄 الجدول الكامل للنتائج")
            st.dataframe(data, use_container_width=True)

    except Exception as e:
        st.error(f"حدث خطأ أثناء تحليل البيانات: {e}")
