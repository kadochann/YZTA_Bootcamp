import streamlit as st
import pandas as pd
from src.db.database import SessionLocal
from src.db.models import Patient
import numpy as np

st.set_page_config(page_title="MediTriaj | İstatistikler", page_icon="📊", layout="wide")

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.utils.styles import MAIN_CSS
st.markdown(MAIN_CSS, unsafe_allow_html=True)

with st.container(key="navbar"):
    col_title, col_nav = st.columns([3, 4], vertical_alignment="center")

    with col_title:
        st.markdown(
            """
            <div style="display:flex; align-items:center; gap:12px; padding: 5px 0;">
                <div>
                    <div style="font-size:2.7rem; font-weight:800; color:#ffffff; line-height:1.1; letter-spacing:-0.5px;">MediTriaj</div>
                    <div style="font-size:1.15rem; color:#B8C8E0; font-weight:600; margin-top:4px;">Akıllı Ön-Triyaj ve Doktor Karar Destek Paneli</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_nav:
        c1, c2, c3 = st.columns(3)
        with c1:
            st.page_link("Ana_Sayfa.py", label="🏠 Ana Sayfa", use_container_width=True)
        with c2:
            st.page_link("pages/3_Patients.py", label="👥 Hastalar", use_container_width=True)
        with c3:
            st.page_link("pages/4_Statistics.py", label="📊 İstatistikler", use_container_width=True)

st.markdown("<hr style='margin-top: 5px; margin-bottom: 20px; border-color: #E2E8F0;'>", unsafe_allow_html=True)

st.title("İstatistikler")

@st.cache_data(ttl=5)
def get_stats_data():
    db = SessionLocal()
    try:
        patients = db.query(Patient).all()
        return [{
            "id": p.id,
            "age": p.age,
            "urgency_score": p.urgency_score,
            "created_at": p.created_at
        } for p in patients]
    finally:
        db.close()

data = get_stats_data()
df = pd.DataFrame(data)

if df.empty:
    st.info("Henüz hasta verisi bulunmamaktadır.")
else:
    # Handle timezone naive/aware comparison
    df['created_at'] = pd.to_datetime(df['created_at'])
    now = pd.Timestamp.now()
    if df['created_at'].dt.tz is not None:
        now = now.tz_localize('UTC').tz_convert(df['created_at'].dt.tz)
        
    last_24h_df = df[df['created_at'] >= (now - pd.Timedelta(days=1))]

    # Summary cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"<div style='padding:20px; border-radius:12px; background:#ffffff; border:1px solid #E2E8F0; box-shadow:0 2px 8px rgba(15,37,68,0.05); text-align:center;'><div style='font-size:1.1rem; color:#64748B; font-weight:600;'>Toplam Hasta</div><div style='font-size:2.5rem; font-weight:800; color:#0F2544;'>{len(df)}</div></div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div style='padding:20px; border-radius:12px; background:#ffffff; border:1px solid #E2E8F0; box-shadow:0 2px 8px rgba(15,37,68,0.05); text-align:center;'><div style='font-size:1.1rem; color:#64748B; font-weight:600;'>Son 24 Saat</div><div style='font-size:2.5rem; font-weight:800; color:#0F2544;'>{len(last_24h_df)}</div></div>", unsafe_allow_html=True)
    with col3:
        avg_urgency = df['urgency_score'].mean()
        st.markdown(f"<div style='padding:20px; border-radius:12px; background:#ffffff; border:1px solid #E2E8F0; box-shadow:0 2px 8px rgba(15,37,68,0.05); text-align:center;'><div style='font-size:1.1rem; color:#64748B; font-weight:600;'>Ortalama Aciliyet Skoru</div><div style='font-size:2.5rem; font-weight:800; color:#0F2544;'>{avg_urgency:.1f}</div></div>", unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Charts
    c1, c2 = st.columns(2)
    
    with c1:
        st.subheader("Yaş Dağılımı")
        bins = [0, 1, 5, 12, 17, 29, 44, 59, 74, 150]
        labels = ["0–1", "2–5", "6–12", "13–17", "18–29", "30–44", "45–59", "60–74", "75+"]
        
        # Use pandas cut to categorize
        df['age_group'] = pd.cut(df['age'], bins=bins, labels=labels, right=True, include_lowest=True)
        age_counts = df['age_group'].value_counts().reindex(labels, fill_value=0)
        
        st.bar_chart(age_counts)
        
    with c2:
        st.subheader("Aciliyet Dağılımı")
        
        def urgency_group(score):
            if score <= 3:
                return "1-3 (Yeşil)"
            elif score <= 6:
                return "4-6 (Turuncu)"
            else:
                return "7-10 (Kırmızı)"
                
        df['urgency_cat'] = df['urgency_score'].apply(urgency_group)
        urg_order = ["1-3 (Yeşil)", "4-6 (Turuncu)", "7-10 (Kırmızı)"]
        urg_counts = df['urgency_cat'].value_counts().reindex(urg_order, fill_value=0)
        
        import altair as alt
        chart_df = pd.DataFrame({
            "Aciliyet Seviyesi": urg_order,
            "Hasta Sayısı": urg_counts.values
        })
        
        chart = alt.Chart(chart_df).mark_bar().encode(
            x=alt.X("Aciliyet Seviyesi", sort=urg_order, axis=alt.Axis(labelAngle=0)),
            y="Hasta Sayısı",
            color=alt.Color(
                "Aciliyet Seviyesi", 
                scale=alt.Scale(domain=urg_order, range=["#10B981", "#F59E0B", "#DC2626"]),
                legend=None
            )
        ).properties(height=350)
        
        st.altair_chart(chart, use_container_width=True)
