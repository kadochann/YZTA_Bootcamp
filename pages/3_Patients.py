import streamlit as st
import pandas as pd
import json
from src.db.database import SessionLocal
from src.db.models import Patient
from datetime import datetime, timedelta

st.set_page_config(page_title="MediTriaj | Hastalar", page_icon="👥", layout="wide")

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

st.markdown("""
<style>
.patient-card {
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 10px;
    padding: 16px;
    margin-bottom: 12px;
    cursor: pointer;
    transition: all 0.2s ease;
}
.patient-card:hover {
    background: rgba(255, 255, 255, 0.08);
    border-color: rgba(255, 255, 255, 0.3);
}
</style>
""", unsafe_allow_html=True)

st.title("Hastalar")

# Fetch data
@st.cache_data(ttl=5)
def get_patients():
    db = SessionLocal()
    try:
        patients = db.query(Patient).all()
        # Convert to dict for caching
        return [{
            "id": p.id,
            "full_name": p.full_name,
            "national_id": p.national_id,
            "age": p.age,
            "sex": p.sex,
            "complaints": p.complaints,
            "urgency_score": p.urgency_score,
            "top_prediction": p.top_prediction,
            "differentials": p.differentials,
            "evidences": p.evidences,
            "initial_evidence": p.initial_evidence,
            "created_at": p.created_at
        } for p in patients]
    finally:
        db.close()

patients_data = get_patients()
df = pd.DataFrame(patients_data)

total_count = len(df)

# Filters Expander
with st.expander("Filtreleme ve Sıralama Seçenekleri", expanded=False):
    col_f1, col_f2 = st.columns(2)
    
    with col_f1:
        st.markdown("**Genel Seçenekler**")
        filter_24h = st.checkbox("Son 24 Saat")
        sort_urgency = st.checkbox("Aciliyete Göre Sırala (Yüksekten Düşüğe)", value=False)
        
    with col_f2:
        st.markdown("**Yaş Grupları**")
        age_ranges = {
            "0–1": (0, 1),
            "2–5": (2, 5),
            "6–12": (6, 12),
            "13–17": (13, 17),
            "18–29": (18, 29),
            "30–44": (30, 44),
            "45–59": (45, 59),
            "60–74": (60, 74),
            "75+": (75, 150)
        }
        
        selected_age_groups = []
        age_cols = st.columns(2)
        
        for i, (label, (min_a, max_a)) in enumerate(age_ranges.items()):
            if not df.empty:
                count = len(df[(df['age'] >= min_a) & (df['age'] <= max_a)])
                pct = (count / total_count * 100) if total_count > 0 else 0
                display_label = f"{label} ({count} - %{pct:.1f})"
            else:
                display_label = f"{label} (0 - %0.0)"
                
            with age_cols[i % 2]:
                if st.checkbox(display_label, key=f"age_{label}"):
                    selected_age_groups.append(label)

if not df.empty:
    if filter_24h:
        one_day_ago = datetime.now() - timedelta(days=1)
        # Handle timezone naive/aware comparison if needed. Streamlit pd is typically naive
        df['created_at'] = pd.to_datetime(df['created_at'])
        try:
            one_day_ago = one_day_ago.astimezone(df['created_at'].dt.tz)
        except Exception:
            pass
        df = df[df['created_at'] >= one_day_ago]
    
    if selected_age_groups:
        conditions = []
        for group in selected_age_groups:
            min_a, max_a = age_ranges[group]
            conditions.append((df['age'] >= min_a) & (df['age'] <= max_a))
        import numpy as np
        df = df[np.logical_or.reduce(conditions)]
    
    # Calculate Age Group Stats
    total_count = len(df)
    
    if sort_urgency:
        df = df.sort_values(by='urgency_score', ascending=False)
    else:
        df = df.sort_values(by='created_at', ascending=False)

st.write(f"Toplam {len(df) if not df.empty else 0} hasta listeleniyor.")

if df.empty:
    st.info("Kayıtlı hasta bulunamadı.")
else:
    # Render Patient Details Dialog
    @st.dialog("Hasta Detayları", width="large")
    def show_patient_details(p):
        st.subheader(f"{p['full_name']} ({p['age']} Yaş - {p['sex']})")
        st.write(f"**TC Kimlik No:** {p['national_id'] or '-'}")
        
        c1, c2 = st.columns(2)
        with c1:
            st.metric("Aciliyet Skoru", f"{p['urgency_score']} / 10")
            st.write("**Kayıt Tarihi:**", pd.to_datetime(p['created_at']).strftime('%d.%m.%Y %H:%M'))
        with c2:
            st.write("**Klinik İfadeler (Semptomlar):**")
            for c in p.get('complaints', []):
                st.markdown(f"- {c}")
        
        st.divider()
        st.write("**Tahmin:**")
        top_pred = p.get('top_prediction', {})
        if top_pred:
            st.write(f"{top_pred.get('pathology', 'Bilinmiyor')} (%{top_pred.get('probability', 0)*100:.1f})")
        
        st.write("**Ayırıcı Tanılar:**")
        diffs = p.get('differentials', [])
        for d in diffs:
            st.write(f"- {d.get('pathology')} (%{d.get('probability', 0)*100:.1f})")
        
        st.divider()
        ie = p.get('initial_evidence')
        evs = p.get('evidences') or []
        if ie or evs:
            st.write("**Kanıt Analizi (Evidence Mapping):**")
            if ie:
                st.markdown(f"🎯 **Başlangıç Kanıtı:** `{ie}`")
            if evs:
                st.write("**Tespit Edilen Kanıtlar:**")
                cols = st.columns(3)
                for i, ev in enumerate(evs):
                    cols[i % 3].markdown(f"`{ev}`")

    # Render cards
    for _, row in df.iterrows():
        with st.container():
            col1, col2 = st.columns([4, 1])
            with col1:
                st.markdown(f"**{row['full_name']}** - {row['age']} Yaş - {row['sex']}")
                pred_name = row.get('top_prediction', {}).get('pathology', '')
                st.markdown(f"<span style='color: #64748B;'>Tahmin: {pred_name}</span>", unsafe_allow_html=True)
            with col2:
                urgency = row['urgency_score']
                color = "#10B981" if urgency < 5 else "#F59E0B" if urgency < 8 else "#DC2626"
                st.markdown(f"<div style='text-align:right; font-weight:bold; color:{color};'>Skor: {urgency}</div>", unsafe_allow_html=True)
                st.markdown(f"<div style='text-align:right; font-size: 0.8rem;'>{pd.to_datetime(row['created_at']).strftime('%d.%m.%Y %H:%M')}</div>", unsafe_allow_html=True)
            
            if st.button(f"Detayları Gör", key=f"btn_{row['id']}"):
                show_patient_details(row.to_dict())
            
            st.markdown("<hr style='margin: 8px 0;'>", unsafe_allow_html=True)
