"""
pages/2_Hasta_Ozetleri.py  ─  Hasta Özetleri Paneli
"""

import streamlit as st
import sys, os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.utils.styles import MAIN_CSS
from src.utils.mock_data import get_mock_hastalar, aciliyet_seviyesi, aciliyet_kart_class, BRANSLAR

st.set_page_config(
    page_title="Hasta Özetleri | MediTriaj",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
)
st.markdown(MAIN_CSS, unsafe_allow_html=True)

# ── Top Navbar ──────────────────────────────────────────────────────────────
with st.container(key="navbar"):
    col_title, col_nav = st.columns([3, 2], vertical_alignment="center")

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
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.page_link("Ana_Sayfa.py", label="🏠 Ana Sayfa", use_container_width=True)
        with c2:
            st.page_link("pages/2_Hasta_Ozetleri.py", label="📋 Hasta Özetleri", use_container_width=True)
        with c3:
            st.page_link("pages/3_Patients.py", label="👥 Hastalar", use_container_width=True)
        with c4:
            st.page_link("pages/4_Statistics.py", label="📊 İstatistikler", use_container_width=True)

st.markdown("<hr style='margin-top: 5px; margin-bottom: 20px; border-color: #E2E8F0;'>", unsafe_allow_html=True)

# ── Başlık ────────────────────────────────────────────────────────────────────
st.markdown(
    """
    <div style="margin-bottom:24px;">
        <span style="font-size:1.8rem; font-weight:700; color:#0F2544;">Hasta Özetleri</span><br>
        <span style="color:#64748B; font-size:0.95rem;">Bugünkü randevu listesi ve yapay zeka destekli ön-triyaj özet raporları</span>
    </div>
    """,
    unsafe_allow_html=True,
)

# ── Filtreler ─────────────────────────────────────────────────────────────────
with st.expander("Hasta Listesini Filtrele", expanded=False):
    filtre_aciliyet = st.multiselect(
        "Aciliyet Seviyesi",
        ["🔴 Yüksek (8-10)", "🟡 Orta (5-7)", "🟢 Düşük (1-4)"],
        default=["🔴 Yüksek (8-10)", "🟡 Orta (5-7)", "🟢 Düşük (1-4)"],
    )

# ── Özet metrikler ────────────────────────────────────────────────────────────
hastalar = get_mock_hastalar()

acil   = sum(1 for h in hastalar if h["aciliyet_skoru"] >= 8)
orta   = sum(1 for h in hastalar if 5 <= h["aciliyet_skoru"] < 8)
dusuk  = sum(1 for h in hastalar if h["aciliyet_skoru"] < 5)

m1, m2, m3, m4 = st.columns(4)
m1.metric("Toplam Randevu", len(hastalar))
m2.metric("Yüksek Aciliyet", acil, delta="Öncelikli")
m3.metric("Orta Aciliyet",   orta)
m4.metric("Düşük Aciliyet",  dusuk)

st.markdown("<br>", unsafe_allow_html=True)

# ── Filtreleme ────────────────────────────────────────────────────────────────
def aciliyet_etiketi(skor):
    if skor >= 8: return "🔴 Yüksek (8-10)"
    if skor >= 5: return "🟡 Orta (5-7)"
    return "🟢 Düşük (1-4)"

filtreli = [
    h for h in hastalar
    if aciliyet_etiketi(h["aciliyet_skoru"]) in filtre_aciliyet
]

# Aciliyete göre sırala
filtreli.sort(key=lambda h: -h["aciliyet_skoru"])

if not filtreli:
    st.info("Seçili filtrelere uyan hasta bulunamadı.")
    st.stop()

# ── Sekme: Liste / Detay ──────────────────────────────────────────────────────
tab_liste, tab_detay = st.tabs(["Randevu Listesi", "Detaylı İnceleme"])

# ───────────────────────────── SEKME 1: LİSTE ────────────────────────────────
with tab_liste:
    for hasta in filtreli:
        seviye = aciliyet_seviyesi(hasta["aciliyet_skoru"])
        skor   = hasta["aciliyet_skoru"]
        bar_oran = int(skor / 10 * 100)
        brans_renk = BRANSLAR.get(hasta["brans"], {}).get("renk", "#1A3A6B")
        kart_class = aciliyet_kart_class(skor)

        with st.container():
            st.markdown(
                f"""
                <div class="{kart_class}">
                    <div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:8px;">
                        <div>
                            <div style="font-size:1.05rem; font-weight:700; color:#0F2544; margin-bottom:2px;">
                                {hasta["ad_soyad"]} &nbsp;
                                <span style="font-size:0.82rem; font-weight:400; color:#64748B;">
                                    {hasta["yas"]} yaş · {hasta["randevu"]}
                                </span>
                            </div>
                            <div style="font-size:0.85rem; color:#475569; margin-top:4px; margin-bottom:10px;">
                                {hasta["sikayet_ozeti"]}
                            </div>
                            <div style="display:flex; flex-wrap:wrap; gap:6px; margin-bottom:10px;">
                                {"".join(f'<span style="background:#EFF6FF; color:#1E40AF; border-radius:999px; padding:2px 10px; font-size:0.78rem;">{s}</span>' for s in hasta["semptomlar"])}
                            </div>
                        </div>
                        <div style="text-align:right; min-width:130px;">
                            <div style="font-size:1.3rem; font-weight:700; color:{brans_renk}; margin-bottom:4px;">
                                {hasta["brans"]}
                            </div>
                            <span class="{seviye['badge']}">{seviye['label']}</span>
                        </div>
                    </div>
                    <div style="font-size:0.8rem; color:#64748B; margin-bottom:4px;">
                        Aciliyet: <b>{skor}/10</b>
                    </div>
                    <div class="urgency-bar-wrap">
                        <div class="{seviye['bar']}" style="width:{bar_oran}%;"></div>
                    </div>
                    <div style="background:#F8FAFF; border:1px solid #DBEAFE; border-radius:10px; padding:12px 14px; margin-top:10px;">
                        <div style="font-size:0.78rem; color:#1E3A5F; font-weight:600; margin-bottom:4px;">Yapay Zeka Özeti</div>
                        <div style="font-size:0.85rem; color:#334155; line-height:1.55;">{hasta["ai_ozeti"]}</div>
                    </div>
                    <div style="margin-top:10px; font-size:0.8rem; color:#64748B;">
                        <b>Risk Faktörleri:</b> {", ".join(hasta["risk_faktorleri"]) if hasta["risk_faktorleri"] else "Bulunmuyor"}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

# ───────────────────────────── SEKME 2: DETAY ────────────────────────────────
with tab_detay:
    hasta_isimleri = [f"{h['ad_soyad']} ({h['randevu']})" for h in filtreli]
    secim = st.selectbox("Hasta Seçin", hasta_isimleri)
    secili_idx = hasta_isimleri.index(secim)
    hasta = filtreli[secili_idx]

    seviye = aciliyet_seviyesi(hasta["aciliyet_skoru"])
    skor   = hasta["aciliyet_skoru"]
    brans_renk = BRANSLAR.get(hasta["brans"], {}).get("renk", "#1A3A6B")

    st.markdown("<br>", unsafe_allow_html=True)
    d1, d2 = st.columns([1, 1], gap="large")

    with d1:
        st.markdown('<div class="section-title">Hasta Bilgileri</div>', unsafe_allow_html=True)
        st.markdown(
            f"""
            <div class="triage-card">
                <table style="width:100%; font-size:0.88rem; border-collapse:collapse;">
                    <tr><td style="color:#64748B; padding:6px 0; width:45%;"><b>Ad Soyad</b></td>
                        <td>{hasta["ad_soyad"]}</td></tr>
                    <tr><td style="color:#64748B; padding:6px 0;"><b>Yaş</b></td>
                        <td>{hasta["yas"]}</td></tr>
                    <tr><td style="color:#64748B; padding:6px 0;"><b>Randevu Saati</b></td>
                        <td>{hasta["randevu"]}</td></tr>
                    <tr><td style="color:#64748B; padding:6px 0;"><b>Hasta ID</b></td>
                        <td><code>{hasta["id"]}</code></td></tr>
                    <tr><td style="color:#64748B; padding:6px 0;"><b>Önerilen Branş</b></td>
                        <td style="color:{brans_renk}; font-weight:600;">{hasta["brans"]}</td></tr>
                    <tr><td style="color:#64748B; padding:6px 0;"><b>Aciliyet</b></td>
                        <td><span class="{seviye['badge']}">{seviye['label']} ({skor}/10)</span></td></tr>
                </table>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown('<div class="section-title">Risk Faktörleri</div>', unsafe_allow_html=True)
        riskler_html = "".join(
            f'<div style="padding:8px 12px; background:#FEF3C7; border-radius:8px; margin-bottom:8px; font-size:0.85rem; color:#92400E;">{r}</div>'
            for r in hasta["risk_faktorleri"]
        )
        st.markdown(f'<div class="triage-card">{riskler_html}</div>', unsafe_allow_html=True)

    with d2:
        st.markdown('<div class="section-title">Semptom Analizi</div>', unsafe_allow_html=True)
        semptomlar_html = "".join(
            f'<div style="padding:8px 12px; background:#EFF6FF; border-radius:8px; margin-bottom:8px; font-size:0.85rem; color:#1E40AF;">{s}</div>'
            for s in hasta["semptomlar"]
        )
        st.markdown(f'<div class="triage-card">{semptomlar_html}</div>', unsafe_allow_html=True)

        st.markdown('<div class="section-title">Yapay Zeka Özet Raporu</div>', unsafe_allow_html=True)
        st.markdown(
            f"""
            <div class="triage-card" style="background:#F8FAFF; border:1px solid #DBEAFE;">
                <div style="font-size:0.88rem; color:#1E3A5F; line-height:1.65;">
                    {hasta["ai_ozeti"]}
                </div>
                <hr style="border:none; border-top:1px solid #E2E8F0; margin:14px 0;">
                <div style="font-size:0.78rem; color:#94A3B8;">
                    Bu özet yapay zeka tarafından üretilmiştir. Nihai klinik karar hekime aittir.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Aciliyet bar
        bar_oran = int(skor / 10 * 100)
        st.markdown(
            f"""
            <div class="triage-card" style="padding:16px 20px;">
                <div style="font-size:0.85rem; color:#64748B; margin-bottom:6px;">
                    <b>Aciliyet Göstergesi:</b> {skor}/10
                </div>
                <div class="urgency-bar-wrap" style="height:14px;">
                    <div class="{seviye['bar']}" style="width:{bar_oran}%; height:14px;"></div>
                </div>
                <div style="display:flex; justify-content:space-between; font-size:0.75rem; color:#94A3B8; margin-top:4px;">
                    <span>Düşük</span><span>Orta</span><span>Yüksek</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )