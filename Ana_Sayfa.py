"""
app.py  ─  Ana giriş noktası & Anasayfa
Çalıştırmak için:  streamlit run app.py
"""

import streamlit as st
import sys, os

# ── Proje kök dizinini Python path'e ekle ────────────────────────────────────
sys.path.insert(0, os.path.dirname(__file__))

from src.utils.styles import MAIN_CSS
from src.utils.mock_data import get_mock_istatistikler, BRANSLAR, mock_llm_analiz, aciliyet_seviyesi
import time

# ── Sayfa konfigürasyonu ─────────────────────────────────────────────────────
st.set_page_config(
    page_title="MediTriaj | Akıllı Ön-Triyaj Sistemi",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(MAIN_CSS, unsafe_allow_html=True)

# ── Session state başlat ──────────────────────────────────────────────────────
if "chat_gecmisi" not in st.session_state:
    st.session_state.chat_gecmisi = []
if "analiz_tamamlandi" not in st.session_state:
    st.session_state.analiz_tamamlandi = False
if "analiz_sonucu" not in st.session_state:
    st.session_state.analiz_sonucu = None

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
        c1, c2 = st.columns([1, 1])
        with c1:
            st.page_link("Ana_Sayfa.py", label="🏠 Ana Sayfa", use_container_width=True)
        with c2:
            st.page_link("pages/2_Hasta_Ozetleri.py", label="📋 Hasta Özetleri", use_container_width=True)

st.markdown("<hr style='margin-top: 5px; margin-bottom: 20px; border-color: #E2E8F0;'>", unsafe_allow_html=True)

# ── Nasıl Çalışır Kartı (Eski Hero Banner Yerine) ──────────────────────────────
st.markdown(
    """
    <div class="hero-banner" style="padding: 32px 40px; margin-bottom: 24px;">
        <h2 style="color: white; margin-top: 0; margin-bottom: 20px; font-size: 1.5rem; font-weight: 700; border-bottom: 1px solid rgba(255, 255, 255, 0.2); padding-bottom: 10px;">Nasıl Çalışır?</h2>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 20px;">
            <div style="background: rgba(255, 255, 255, 0.08); padding: 18px; border-radius: 12px; border: 1px solid rgba(255, 255, 255, 0.12);">
                <div style="font-weight: 700; font-size: 1.05rem; margin-bottom: 6px; color: white;">1. Şikayetinizi Yazın</div>
                <div style="font-size: 0.85rem; opacity: 0.85; line-height: 1.45;">Hastaneye gelmeden önce şikayetinizi ve nasıl hissettiğinizi kendi cümlelerinizle kısaca yazın.</div>
            </div>
            <div style="background: rgba(255, 255, 255, 0.08); padding: 18px; border-radius: 12px; border: 1px solid rgba(255, 255, 255, 0.12);">
                <div style="font-weight: 700; font-size: 1.05rem; margin-bottom: 6px; color: white;">2. Akıllı Ön Analiz</div>
                <div style="font-size: 0.85rem; opacity: 0.85; line-height: 1.45;">Sistem şikayetlerinizi inceleyerek hangi tıbbi bölüme gitmeniz gerektiğini ve durumun önceliğini belirler.</div>
            </div>
            <div style="background: rgba(255, 255, 255, 0.08); padding: 18px; border-radius: 12px; border: 1px solid rgba(255, 255, 255, 0.12);">
                <div style="font-weight: 700; font-size: 1.05rem; margin-bottom: 6px; color: white;">3. Doktorunuza İletim</div>
                <div style="font-size: 0.85rem; opacity: 0.85; line-height: 1.45;">Yapay zeka şikayetlerinizi doktorunuzun anlayacağı şekilde özetler, böylece doktorunuz muayene öncesinde hazırlık yapabilir.</div>
            </div>
            <div style="background: rgba(255, 255, 255, 0.08); padding: 18px; border-radius: 12px; border: 1px solid rgba(255, 255, 255, 0.12);">
                <div style="font-weight: 700; font-size: 1.05rem; margin-bottom: 6px; color: white;">4. Hekim Kararı</div>
                <div style="font-size: 0.85rem; opacity: 0.85; line-height: 1.45;">Bu sistem kesinlikle bir tanı koymaz veya ilaç yazmaz. Son muayene ve tedavi kararları tamamen doktorunuza aittir.</div>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ── Hasta Triyaj İçerikleri ──────────────────────────────────────────────────
st.markdown(
    """
    <div style="margin-bottom:8px;">
        <span style="font-size:1.8rem; font-weight:700; color:#0F2544;">Hasta Ön-Triyaj</span><br>
        <span style="color:#64748B; font-size:0.95rem;">Şikayetlerinizi aşağıdaki forma girin, sistem sizi doğru bölüme yönlendirsin.</span>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="ethical-warning" style="margin-bottom:24px;">
        <b>Hatırlatma:</b> Bu sistem bir tanı koymaz. Şikayetlerinizi hekiminize daha iyi iletmenize
        yardımcı olmak amacıyla tasarlanmıştır.
    </div>
    """,
    unsafe_allow_html=True,
)

# 2 sütun düzeni
col_form, col_sonuc = st.columns([1, 1], gap="large")

# ─── SOL: Hasta Formu ─────────────────────────────────────────────────────────
with col_form:
    st.markdown('<div class="section-title">Bilgilerinizi Girin</div>', unsafe_allow_html=True)

    with st.form("hasta_formu", clear_on_submit=False):
        c1, c2 = st.columns(2)
        with c1:
            ad_soyad = st.text_input("Ad Soyad", placeholder="Örn: Ahmet Yılmaz")
        with c2:
            yas = st.number_input("Yaşınız", min_value=1, max_value=120, value=35, step=1)

        c3, c4 = st.columns(2)
        with c3:
            cinsiyet = st.selectbox("Cinsiyet", ["Belirtmek istemiyorum", "Erkek", "Kadın"])
        with c4:
            sure = st.selectbox(
                "Şikayet Süresi",
                ["Birkaç saat", "1-3 gün", "3-7 gün", "1-4 hafta", "1 aydan fazla"],
            )

        sikayet = st.text_area(
            "Şikayetinizi anlatın",
            placeholder=(
                "Örn: Üç gündür göğsümün sol tarafında yanma hissi var, "
                "merdiven çıkınca nefes darlığı oluyor ve hafif çarpıntı yaşıyorum..."
            ),
            height=140,
        )

        gecmis = st.text_area(
            "Geçmiş hastalık / ilaç kullanımı (isteğe bağlı)",
            placeholder="Örn: Hipertansiyon, metformin kullanıyorum...",
            height=80,
        )

        siddet = st.slider(
            "Şikayetinizin şiddeti (1 = hafif, 10 = çok şiddetli)",
            min_value=1, max_value=10, value=5,
        )

        gonder = st.form_submit_button("Analiz Et", use_container_width=True)

    if gonder:
        if not sikayet.strip():
            st.error("Lütfen şikayetinizi açıklayan bir metin girin.")
        else:
            with st.spinner("Yapay zeka şikayetinizi analiz ediyor..."):
                time.sleep(1.5)  # Gerçek API çağrısını simüle et
                sonuc = mock_llm_analiz(sikayet, yas)

            # Sohbet geçmişine ekle
            st.session_state.chat_gecmisi.append({
                "tur": "kullanici",
                "mesaj": f"**{ad_soyad or 'Hasta'}** ({yas} yaş) — *Şiddet: {siddet}/10*\n\n{sikayet}",
            })
            st.session_state.chat_gecmisi.append({
                "tur": "ai",
                "mesaj": sonuc["hasta_mesaji"],
            })
            st.session_state.analiz_sonucu = sonuc
            st.session_state.analiz_tamamlandi = True
            st.rerun()

# ─── SAĞ: Analiz Sonucu & Sohbet ─────────────────────────────────────────────
with col_sonuc:
    if not st.session_state.analiz_tamamlandi:
        st.markdown('<div class="section-title">Analiz Sonucu</div>', unsafe_allow_html=True)
        st.markdown(
            """
            <div class="triage-card" style="text-align:center; padding:48px 24px; color:#94A3B8;">
                <div style="font-size:1rem; font-weight:500; margin-bottom:8px; color:#64748B;">
                    Yapay Zeka Analizi Bekleniyor
                </div>
                <div style="font-size:0.85rem; line-height:1.6;">
                    Formu doldurup <b>Analiz Et</b> butonuna bastıktan<br>
                    sonra sonuçlar burada görünecek.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        sonuc = st.session_state.analiz_sonucu
        seviye = aciliyet_seviyesi(sonuc["aciliyet_skoru"])
        skor = sonuc["aciliyet_skoru"]
        bar_oran = int(skor / 10 * 100)

        st.markdown('<div class="section-title">Analiz Sonucu</div>', unsafe_allow_html=True)

        # Özet kart
        kart_class = "triage-card triage-card-emergency" if skor >= 8 else \
                     "triage-card triage-card-medium"    if skor >= 5 else \
                     "triage-card triage-card-low"

        brans_renk = BRANSLAR.get(sonuc["brans"], {}).get("renk", "#1A3A6B")

        st.markdown(
            f"""
            <div class="{kart_class}">
                <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:16px;">
                    <div>
                        <div style="font-size:0.78rem; color:#64748B; margin-bottom:4px; text-transform:uppercase; letter-spacing:0.5px;">Önerilen Branş</div>
                        <div style="font-size:1.6rem; font-weight:700; color:{brans_renk};">
                            {sonuc["brans"]}
                        </div>
                    </div>
                    <span class="{seviye['badge']}">{seviye['label']}</span>
                </div>
                <div style="font-size:0.85rem; color:#475569; margin-bottom:4px;">
                    Aciliyet Skoru: <b>{skor}/10</b>
                </div>
                <div class="urgency-bar-wrap">
                    <div class="{seviye['bar']}" style="width:{bar_oran}%;"></div>
                </div>
                <div style="font-size:0.82rem; color:#64748B;">
                    <b>Tespit edilen semptomlar:</b> {", ".join(sonuc["semptomlar"]) if sonuc["semptomlar"] else "—"}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Sohbet baloncukları
        st.markdown('<div class="section-title" style="margin-top:16px;">Değerlendirme Mesajı</div>', unsafe_allow_html=True)

        for mesaj in st.session_state.chat_gecmisi:
            if mesaj["tur"] == "kullanici":
                st.markdown(
                    f"""
                    <div style="overflow:hidden; margin-bottom:8px;">
                        <div class="chat-bubble-user" style="margin-left: 0px !important;">{mesaj["mesaj"]}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    f"""
                    <div style="overflow:hidden; margin-bottom:8px;">
                        <div class="chat-bubble-ai" style="margin-right: 0px !important;">{mesaj["mesaj"]}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        # Sıfırla butonu
        if st.button("Yeni Analiz Başlat", use_container_width=True):
            st.session_state.chat_gecmisi = []
            st.session_state.analiz_tamamlandi = False
            st.session_state.analiz_sonucu = None
            st.rerun()

        # Etik not
        st.markdown(
            """
            <div class="ethical-warning" style="margin-top:16px;">
                Bu sistem bir tanı koymaz. Yukarıdaki öneriler yalnızca ön bilgilendirme
                amaçlıdır ve bir sağlık profesyonelinin değerlendirmesinin yerini alamaz.
            </div>
            """,
            unsafe_allow_html=True,
        )

# ── Hekim Paneli Geçiş ────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<div class="section-title">Hasta Özetleri Paneli (Doktorlar İçin)</div>', unsafe_allow_html=True)

with st.container(border=True):
    st.markdown(
        """
        <div style="padding: 10px 0;">
            <div style="font-size: 1.1rem; font-weight: 700; color: #0F2544; margin-bottom: 6px;">Hasta Özetleri ve Karar Destek</div>
            <div style="font-size: 0.88rem; color: #64748B; line-height: 1.5; margin-bottom: 16px;">
                Doktorlar için hasta randevu listesini, ön-triyaj aciliyet skorlarını ve yapay zeka tarafından hazırlanan semptom özetlerini görüntüler.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.page_link("pages/2_Hasta_Ozetleri.py", label="Hasta Özetleri Paneline Geç", use_container_width=True)

# ── Etik Uyarı ───────────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
st.markdown(
    """
    <div class="ethical-warning">
        <b>Önemli Uyarı:</b> Bu sistem yalnızca ön bilgilendirme ve karar destek amaçlıdır.
        Hiçbir çıktı tıbbi tanı niteliği taşımaz. Nihai klinik karar ve teşhis yetkisi tamamen
        uzman hekime aittir. Bu uygulama YZTA Bootcamp 2026 kapsamında geliştirilmiş bir prototiptir.
    </div>
    """,
    unsafe_allow_html=True,
)