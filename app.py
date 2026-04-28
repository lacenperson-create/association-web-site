import streamlit as st
import pandas as pd
from datetime import datetime
import os

# 1. إعدادات الصفحة والهوية البصرية
st.set_page_config(page_title="منصة الفروض الرقمية - ثانوية أقا", page_icon="📝", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { background-color: #1a5276; color: white; width: 100%; border-radius: 8px; font-weight: bold; }
    h1, h2 { color: #1a5276; text-align: center; }
    .question-box { background-color: #ffffff; padding: 20px; border-radius: 10px; border-right: 5px solid #1a5276; box-shadow: 2px 2px 5px rgba(0,0,0,0.1); margin-bottom: 20px; }
    .header-box { background-color: #eaf2f8; padding: 15px; border-radius: 10px; text-align: center; margin-bottom: 25px; border: 1px solid #d4e6f1; }
    </style>
    """, unsafe_allow_html=True)

# 2. ترويسة الفرض (اسم المؤسسة والأستاذ)
st.markdown(f"""
    <div class="header-box">
        <h1>ثانوية أقا الإعدادية</h1>
        <h3>مادة علوم الحياة والأرض</h3>
        <p><b>الأستاذ: لحسن</b> | الفرض المحروس رقم 1 - الدورة الأولى</p>
    </div>
    """, unsafe_allow_html=True)

# 3. استمارة بيانات التلميذ (إلزامية)
st.subheader("👤 معلومات التلميذ(ة)")
with st.container():
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        student_name = st.text_input("الاسم الكامل")
    with col2:
        student_class = st.text_input("القسم (مثلاً: 3/1)")
    with col3:
        student_order = st.text_input("رقم الترتيب")

st.markdown("---")

# 4. محتوى الاختبار
st.header("🔬 الجزء الأول: استهلاك المادة العضوية وتدفق الطاقة")

# التمرين الثاني
st.subheader("التمرين الثاني (5 نقط)")
with st.container():
    st.markdown('<div class="question-box">', unsafe_allow_html=True)
    st.write("**السؤال 1:** بعد تحليلك للنتائج، اقترح فرضية حول نوع التفاعلات المسؤولة عن إنتاج الطاقة عند كل من السلالتين G و P.")
    ans1 = st.text_area("أكتب تحليلك وفرضيتك هنا...", key="q1")
    st.markdown('</div>', unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="question-box">', unsafe_allow_html=True)
    st.write("**السؤال 2:** حدد معللاً إجابتك الظواهر الاستقلابية المسؤولة عن تحرير الطاقة الكامنة في المادة العضوية.")
    ans2 = st.text_area("أكتب تحديدك وتعليلك هنا...", key="q2")
    st.markdown('</div>', unsafe_allow_html=True)

# التمرين الثالث
st.header("💪 الجزء الثاني: النشاط العضلي")
with st.container():
    st.markdown('<div class="question-box">', unsafe_allow_html=True)
    st.write("**السؤال 3:** حلل النتائج وأعط تفسيراً لتطورات الحمض اللبني ومركب الفوسفوكرياتين (PC) قبل وأثناء النشاط العضلي.")
    ans3 = st.text_area("أكتب التحليل والتفسير هنا...", key="q3")
    st.markdown('</div>', unsafe_allow_html=True)

# 5. زر الإرسال وحفظ البيانات
if st.button("🚀 إرسال ورقة الإجابة"):
    if student_name and student_class and student_order:
        # تجهيز البيانات
        result = {
            "التوقيت": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "الاسم الكامل": student_name,
            "القسم": student_class,
            "رقم الترتيب": student_order,
            "إجابة س1": ans1,
            "إجابة س2": ans2,
            "إجابة س3": ans3
        }
        
        # حفظ في ملف
        file_path = "student_results.csv"
        file_exists = os.path.isfile(file_path)
        df = pd.DataFrame([result])
        df.to_csv(file_path, mode='a', index=False, header=not file_exists, encoding='utf-8-sig')
        
        st.balloons()
        st.success(f"تم استلام إجاباتك بنجاح يا {student_name}. حظاً موفقاً!")
    else:
        st.error("⚠️ خطأ: يرجى ملء الاسم، القسم، ورقم الترتيب قبل إرسال الفرض.")

# 6. قسم الأستاذ (لوحة التحكم)
st.markdown("---")
with st.expander("🔐 لوحة تحكم الأستاذ لحسن"):
    pwd = st.text_input("كلمة المرور للوصول للنتائج", type="password")
    if pwd == "Aka2026":
        if os.path.isfile("student_results.csv"):
            data = pd.read_csv("student_results.csv")
            st.write("### لائحة إجابات التلاميذ:")
            st.dataframe(data)
            
            csv = data.to_csv(index=False).encode('utf-8-sig')
            st.download_button("📥 تحميل النتائج (Excel)", data=csv, file_name='نتائج_تلاميذ_أقا.csv', mime='text/csv')
        else:
            st.info("لا توجد إجابات مسجلة حالياً.")
