"""
pages/3_📊_Istatistikler.py  ─  Genel İstatistikler ve Hasta Geçmişi
"""

import streamlit as st
import pandas as pd
import sys, os
from datetime import datetime, timedelta
import random

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.utils.styles import MAIN_CSS
from src.utils.mock_data import get_mock_istatistikler, get_mock_hastalar, BRANSLAR, aciliyet_seviyesi

st.set_page_config(
    page_title="İstatistikler | MediTriaj",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)
st.markdown(MAIN_CSS, unsafe_allow_html=True)

# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        """
        <div style='text-align:center; padding: 12px 0 24px 0;'>
            <div style='font-size:2.8rem;'>🩺</div>
            <div style='font-size:1.15rem; font-weight:700;'>MediTriaj</div>
            <div style='font-size:0.78rem; opacity:0.65; margin-top:2px;'>YZTA Bootcamp 2026 · Grup 131</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("---")
    st.markdown(
        """
        <div style='font-size:0.82rem; opacity:0.75; line-height:1.8; padding:0 4px;'>
        <b>📊 Bu sayfada:</b><br>
        • Branş dağılımı<br>
        • Günlük hasta trendi<br>
        • Aciliyet dağılımı<br>
        • Geçmiş kayıt tablosu
        </div>
        """,
        unsafe_allow_html=True,
    )

# ── Başlık ────────────────────────────────────────────────────────────────────
st.markdown(
    """
    <div style="margin-bottom:24px;">
        <span style="font-size:1.8rem; font-weight:700; color:#0F2544;">📊 Genel İstatistikler</span><br>
        <span style="color:#64748B; font-size:0.95rem;">Sistem geneli hasta akışı ve triyaj verileri</span>
    </div>
    """,
    unsafe_allow_html=True,
)

istat = get_mock_istatistikler()

# ── KPI kartları ──────────────────────────────────────────────────────────────
k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("👥 Toplam Hasta",    istat["toplam_hasta"], delta="↑12 bu ay")
k2.metric("📅 Bugün",           istat["bugun_hasta"],  delta="↑3 dün")
k3.metric("⚡ Ort. Aciliyet",   f"{istat['ort_aciliyet']}/10")
k4.metric("🏥 En Sık Branş",   istat["en_sik_brans"])
k5.metric("✅ Tamamlanan",      231, delta="93%")

st.markdown("<br>", unsafe_allow_html=True)

# ── Grafikler ─────────────────────────────────────────────────────────────────
g1, g2 = st.columns([1.2, 0.8], gap="large")

with g1:
    st.markdown('<div class="section-title">📈 Günlük Hasta Trendi (Son 14 Gün)</div>', unsafe_allow_html=True)
    gunluk_df = pd.DataFrame(
        list(istat["gunluk_hasta"].items()),
        columns=["Tarih", "Hasta Sayısı"],
    )
    st.line_chart(gunluk_df.set_index("Tarih"), height=260, use_container_width=True)

with g2:
    st.markdown('<div class="section-title">🎯 Aciliyet Dağılımı</div>', unsafe_allow_html=True)
    acil_df = pd.DataFrame(
        list(istat["aciliyet_dagilim"].items()),
        columns=["Seviye", "Hasta"],
    )
    st.bar_chart(acil_df.set_index("Seviye"), height=260, use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Branş dağılımı ────────────────────────────────────────────────────────────
st.markdown('<div class="section-title">🏥 Branş Bazlı Hasta Dağılımı</div>', unsafe_allow_html=True)

brans_items = sorted(istat["brans_dagilim"].items(), key=lambda x: -x[1])
maks = max(v for _, v in brans_items)

cols = st.columns(2)
for i, (brans, sayi) in enumerate(brans_items):
    oran = int(sayi / maks * 100)
    icon = BRANSLAR[brans]["icon"]
    renk = BRANSLAR[brans]["renk"]
    yuzde = round(sayi / sum(istat["brans_dagilim"].values()) * 100, 1)

    with cols[i % 2]:
        st.markdown(
            f"""
            <div style="margin-bottom:16px;">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:5px;">
                    <span style="font-size:0.9rem; font-weight:500;">{icon} {brans}</span>
                    <span style="font-size:0.82rem; color:#64748B;">{sayi} hasta &nbsp;·&nbsp; {yuzde}%</span>
                </div>
                <div style="background:#E2E8F0; border-radius:999px; height:10px; overflow:hidden;">
                    <div style="background:{renk}; width:{oran}%; height:10px; border-radius:999px;
                                transition: width 0.5s ease;"></div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.markdown("<br>", unsafe_allow_html=True)

# ── Geçmiş Kayıtlar Tablosu ───────────────────────────────────────────────────
st.markdown('<div class="section-title">📋 Geçmiş Triyaj Kayıtları</div>', unsafe_allow_html=True)

# Mock geçmiş veri üret
random.seed(42)
brans_list = list(BRANSLAR.keys())

gecmis_rows = []
for i in range(40):
    tarih = datetime.today() - timedelta(days=random.randint(0, 30))
    skor  = random.randint(1, 10)
    brans = random.choice(brans_list)
    seviye = aciliyet_seviyesi(skor)
    gecmis_rows.append({
        "Tarih":       tarih.strftime("%d.%m.%Y"),
        "Saat":        tarih.strftime("%H:%M"),
        "Hasta ID":    f"H-{2026}-{str(i+1).zfill(3)}",
        "Yaş":         random.randint(18, 80),
        "Branş":       f"{BRANSLAR[brans]['icon']} {brans}",
        "Aciliyet":    skor,
        "Seviye":      seviye["label"],
    })

gecmis_df = pd.DataFrame(gecmis_rows).sort_values("Tarih", ascending=False)

# Filtre satırı
fc1, fc2, fc3 = st.columns([1, 1, 2])
with fc1:
    min_skor, max_skor = st.slider("Aciliyet Aralığı", 1, 10, (1, 10))
with fc2:
    secili_brans = st.multiselect(
        "Branş Filtresi",
        [f"{BRANSLAR[b]['icon']} {b}" for b in brans_list],
        default=[],
        placeholder="Tümü",
    )

filtreli_df = gecmis_df[
    (gecmis_df["Aciliyet"] >= min_skor) & (gecmis_df["Aciliyet"] <= max_skor)
]
if secili_brans:
    filtreli_df = filtreli_df[filtreli_df["Branş"].isin(secili_brans)]

st.dataframe(
    filtreli_df,
    use_container_width=True,
    hide_index=True,
    column_config={
        "Aciliyet": st.column_config.ProgressColumn(
            "Aciliyet",
            min_value=0,
            max_value=10,
            format="%d/10",
        ),
        "Tarih":    st.column_config.TextColumn("📅 Tarih"),
        "Hasta ID": st.column_config.TextColumn("🪪 Hasta ID"),
        "Branş":    st.column_config.TextColumn("🏥 Branş"),
        "Seviye":   st.column_config.TextColumn("⚡ Seviye"),
    },
)

st.markdown(
    f"<div style='font-size:0.8rem; color:#94A3B8; margin-top:8px;'>"
    f"Toplam {len(filtreli_df)} kayıt gösteriliyor.</div>",
    unsafe_allow_html=True,
)

# ── Alt uyarı ─────────────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
st.markdown(
    """
    <div class="ethical-warning">
        📊 <b>Not:</b> Yukarıdaki tüm veriler demo (sahte) verilerdir. Gerçek kullanımda bu veriler
        veritabanından (SQLite/SQL Server) çekilecektir.
    </div>
    """,
    unsafe_allow_html=True,
)