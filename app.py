# --- لوحة تحكم الأستاذ لحسن (مع الحماية من الأخطاء) ---
st.markdown("---")
with st.expander("🔐 لوحة تحكم الأستاذ لحسن (النتائج والإحصائيات)"):
    if st.text_input("القن السري", type="password") == "Aka2026":
        if os.path.exists("qcm_results.csv"):
            data = pd.read_csv("qcm_results.csv")
            
            # التأكد من أن الملف ليس فارغاً وأن عمود النقطة موجود
            if not data.empty and "النقطة" in data.columns:
                st.write("### 📊 التحليل الإحصائي لنتائج القسم")
                
                col_chart1, col_chart2 = st.columns(2)
                
                with col_chart1:
                    # مبيان توزيع النقط
                    fig1 = px.histogram(data, x="النقطة", title="توزيع النقط", 
                                       color_discrete_sequence=['#1a5276'],
                                       labels={'النقطة': 'المعدل', 'count': 'عدد التلاميذ'})
                    st.plotly_chart(fig1, use_container_width=True)
                
                with col_chart2:
                    # إضافة ميزة لكل تلميذ بناءً على نقطته
                    def get_miza(n):
                        try:
                            n = float(n)
                            if n >= 16: return "حسن جداً"
                            elif n >= 14: return "حسن"
                            elif n >= 12: return "مستحسن"
                            elif n >= 10: return "مقبول"
                            else: return "تعثر"
                        except: return "غير محدد"
                    
                    data['الميزة'] = data['النقطة'].apply(get_miza)
                    fig2 = px.pie(data, names='الميزة', title="نسبة الميزات في القسم", hole=0.4)
                    st.plotly_chart(fig2, use_container_width=True)

                st.write("### 📋 جدول النتائج التفصيلي")
                st.dataframe(data)
                
                csv = data.to_csv(index=False).encode('utf-8-sig')
                st.download_button("📥 تحميل ملف Excel", data=csv, file_name="نتائج_ثانوية_أقا.csv")
            else:
                st.warning("⚠️ الملف موجود ولكن لا توجد بيانات مسجلة بداخله بعد.")
        else:
            st.info("ℹ️ لم يقم أي تلميذ باجتياز الامتحان بعد، لذا لا يمكن عرض المبيانات.")
