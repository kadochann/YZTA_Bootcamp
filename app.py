"""
app.py  ─  Ana giriş noktası & Anasayfa
Çalıştırmak için:  streamlit run app.py
"""

import streamlit as st
import sys, os

# ── Proje kök dizinini Python path'e ekle ────────────────────────────────────
sys.path.insert(0, os.path.dirname(__file__))

from src.utils.styles import MAIN_CSS
from src.utils.mock_data import get_mock_istatistikler, BRANSLAR

# ── Sayfa konfigürasyonu ─────────────────────────────────────────────────────
st.set_page_config(
    page_title="MediTriaj | Akıllı Ön-Triyaj Sistemi",
    page_icon="🩺",
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
            <div style='font-size:1.15rem; font-weight:700; letter-spacing:0.5px;'>MediTriaj</div>
            <div style='font-size:0.78rem; opacity:0.65; margin-top:2px;'>YZTA Bootcamp 2026 · Grup 131</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("---")
    st.markdown(
        """
        <div style='font-size:0.78rem; opacity:0.55; line-height:1.6; padding: 0 4px;'>
        <b>Takım</b><br>
        Kadriye Harmancı<br>
        Yahya Fuat Gökkuş<br>
        Meryem Akbaba
        </div>
        """,
        unsafe_allow_html=True,
    )

# ── Hero Banner ──────────────────────────────────────────────────────────────
st.markdown(
    """
    <div class="hero-banner">
        <h1>🩺 Akıllı Ön-Triyaj ve Doktor Karar Destek Paneli</h1>
        <p>
            Hastaların randevu öncesinde şikayetlerini güvenli biçimde iletmesini,<br>
            hekimlerin ise muayeneye hazırlıklı başlamasını sağlayan yapay zeka destekli platform.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ── Özet Metrikler ───────────────────────────────────────────────────────────
istat = get_mock_istatistikler()

col1, col2, col3, col4 = st.columns(4)
col1.metric("👥 Toplam Kayıtlı Hasta",  istat["toplam_hasta"])
col2.metric("📅 Bugünkü Randevular",     istat["bugun_hasta"], delta="↑ 3 dün")
col3.metric("⚡ Ort. Aciliyet Skoru",    f"{istat['ort_aciliyet']}/10")
col4.metric("🏥 En Sık Yönlendirme",    istat["en_sik_brans"])

st.markdown("<br>", unsafe_allow_html=True)

# ── Sistem Açıklaması ────────────────────────────────────────────────────────
col_a, col_b = st.columns([1, 1], gap="large")

with col_a:
    st.markdown('<div class="section-title">🔄 Nasıl Çalışır?</div>', unsafe_allow_html=True)

    steps = [
        ("1️⃣", "Hasta Girişi",       "Hasta randevu öncesinde şikayetlerini doğal dilde yazar."),
        ("2️⃣", "Yapay Zeka Analizi", "LLM modeli metni semptom listesine dönüştürür, ML modeli branş ve aciliyet skoru üretir."),
        ("3️⃣", "Hekim Özeti",        "Hekim, muayene başlamadan önce yapılandırılmış hasta özetini görür."),
        ("4️⃣", "Karar Hekimde",      "Sistem hiçbir zaman tanı koymaz; tüm klinik kararlar hekime aittir."),
    ]
    for icon, baslik, aciklama in steps:
        st.markdown(
            f"""
            <div class="triage-card" style="margin-bottom:12px; padding:16px 20px;">
                <div style="font-size:1.3rem; margin-bottom:4px;">{icon} <b>{baslik}</b></div>
                <div style="font-size:0.88rem; color:#475569;">{aciklama}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

with col_b:
    st.markdown('<div class="section-title">🏥 Branş Dağılımı (Demo)</div>', unsafe_allow_html=True)
    for brans, sayi in sorted(istat["brans_dagilim"].items(), key=lambda x: -x[1])[:6]:
        maks = max(istat["brans_dagilim"].values())
        oran = int(sayi / maks * 100)
        icon = BRANSLAR[brans]["icon"]
        renk = BRANSLAR[brans]["renk"]
        st.markdown(
            f"""
            <div style="margin-bottom:14px;">
                <div style="display:flex; justify-content:space-between; font-size:0.88rem; margin-bottom:4px;">
                    <span>{icon} <b>{brans}</b></span>
                    <span style="color:#64748B;">{sayi} hasta</span>
                </div>
                <div style="background:#E2E8F0; border-radius:999px; height:8px; overflow:hidden;">
                    <div style="background:{renk}; width:{oran}%; height:8px; border-radius:999px;"></div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

# ── Navigasyon Kartları ──────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<div class="section-title">🚀 Panellere Git</div>', unsafe_allow_html=True)

nc1, nc2, nc3 = st.columns(3)

with nc1:
    st.markdown(
        """
        <div class="triage-card" style="text-align:center; padding:30px 20px;">
            <div style="font-size:3rem; margin-bottom:12px;">🏥</div>
            <div style="font-size:1.1rem; font-weight:600; color:#0F2544; margin-bottom:8px;">Hasta Triyaj</div>
            <div style="font-size:0.85rem; color:#64748B; line-height:1.5;">
                Şikayetlerinizi doğal dilde anlatın,<br>sistem sizi yönlendirsin.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.page_link("pages/1_🏥_Hasta_Triyaj.py", label="Hasta Paneline Geç →", icon="🏥")

with nc2:
    st.markdown(
        """
        <div class="triage-card" style="text-align:center; padding:30px 20px;">
            <div style="font-size:3rem; margin-bottom:12px;">👨‍⚕️</div>
            <div style="font-size:1.1rem; font-weight:600; color:#0F2544; margin-bottom:8px;">Hekim Paneli</div>
            <div style="font-size:0.85rem; color:#64748B; line-height:1.5;">
                Hasta özetlerini, risk faktörlerini<br>ve aciliyet skorlarını görün.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.page_link("pages/2_👨‍⚕️_Hekim_Paneli.py", label="Hekim Paneline Geç →", icon="👨‍⚕️")

with nc3:
    st.markdown(
        """
        <div class="triage-card" style="text-align:center; padding:30px 20px;">
            <div style="font-size:3rem; margin-bottom:12px;">📊</div>
            <div style="font-size:1.1rem; font-weight:600; color:#0F2544; margin-bottom:8px;">İstatistikler</div>
            <div style="font-size:0.85rem; color:#64748B; line-height:1.5;">
                Genel hasta akışı, branş dağılımı<br>ve aciliyet trendleri.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.page_link("pages/3_📊_Istatistikler.py", label="İstatistiklere Geç →", icon="📊")

# ── Etik Uyarı ───────────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
st.markdown(
    """
    <div class="ethical-warning">
        ⚠️ <b>Önemli Uyarı:</b> Bu sistem yalnızca ön bilgilendirme ve karar destek amaçlıdır.
        Hiçbir çıktı tıbbi tanı niteliği taşımaz. Nihai klinik karar ve teşhis yetkisi tamamen
        uzman hekime aittir. Bu uygulama YZTA Bootcamp 2026 kapsamında geliştirilmiş bir prototiptir.
    </div>
    """,
    unsafe_allow_html=True,
)