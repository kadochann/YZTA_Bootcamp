"""
pages/1_🏥_Hasta_Triyaj.py  ─  Hasta Ön-Triyaj Paneli
"""

import streamlit as st
import sys, os, time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.utils.styles import MAIN_CSS
from src.utils.mock_data import mock_llm_analiz, aciliyet_seviyesi, BRANSLAR

st.set_page_config(
    page_title="Hasta Triyaj | MediTriaj",
    page_icon="🏥",
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
        <div style='font-size:0.82rem; opacity:0.75; line-height:1.8; padding: 0 4px;'>
        <b>📋 Bu sayfada:</b><br>
        • Şikayetlerinizi yazın<br>
        • Yapay zeka analiz etsin<br>
        • Yönlendirme önerisini alın
        </div>
        """,
        unsafe_allow_html=True,
    )

# ── Başlık ────────────────────────────────────────────────────────────────────
st.markdown(
    """
    <div style="margin-bottom:8px;">
        <span style="font-size:1.8rem; font-weight:700; color:#0F2544;">🏥 Hasta Ön-Triyaj</span><br>
        <span style="color:#64748B; font-size:0.95rem;">Şikayetlerinizi aşağıdaki forma girin, sistem sizi doğru bölüme yönlendirsin.</span>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="ethical-warning" style="margin-bottom:24px;">
        ℹ️ <b>Hatırlatma:</b> Bu sistem bir tanı koymaz. Şikayetlerinizi hekiminize daha iyi iletmenize
        yardımcı olmak amacıyla tasarlanmıştır. Acil bir durumda lütfen 112'yi arayın.
    </div>
    """,
    unsafe_allow_html=True,
)

# ── Session state başlat ──────────────────────────────────────────────────────
if "chat_gecmisi" not in st.session_state:
    st.session_state.chat_gecmisi = []
if "analiz_tamamlandi" not in st.session_state:
    st.session_state.analiz_tamamlandi = False
if "analiz_sonucu" not in st.session_state:
    st.session_state.analiz_sonucu = None

# ── 2 sütun düzeni ────────────────────────────────────────────────────────────
col_form, col_sonuc = st.columns([1, 1], gap="large")

# ─── SOL: Hasta Formu ─────────────────────────────────────────────────────────
with col_form:
    st.markdown('<div class="section-title">📝 Bilgilerinizi Girin</div>', unsafe_allow_html=True)

    with st.form("hasta_formu", clear_on_submit=False):
        c1, c2 = st.columns(2)
        with c1:
            ad_soyad = st.text_input("👤 Ad Soyad", placeholder="Örn: Ahmet Yılmaz")
        with c2:
            yas = st.number_input("🎂 Yaşınız", min_value=1, max_value=120, value=35, step=1)

        c3, c4 = st.columns(2)
        with c3:
            cinsiyet = st.selectbox("⚧ Cinsiyet", ["Belirtmek istemiyorum", "Erkek", "Kadın"])
        with c4:
            sure = st.selectbox(
                "⏱️ Şikayet Süresi",
                ["Birkaç saat", "1-3 gün", "3-7 gün", "1-4 hafta", "1 aydan fazla"],
            )

        sikayet = st.text_area(
            "💬 Şikayetinizi anlatın",
            placeholder=(
                "Örn: Üç gündür göğsümün sol tarafında yanma hissi var, "
                "merdiven çıkınca nefes darlığı oluyor ve hafif çarpıntı yaşıyorum..."
            ),
            height=140,
        )

        gecmis = st.text_area(
            "📋 Geçmiş hastalık / ilaç kullanımı (isteğe bağlı)",
            placeholder="Örn: Hipertansiyon, metformin kullanıyorum...",
            height=80,
        )

        siddet = st.slider(
            "😣 Şikayetinizin şiddeti (1 = hafif, 10 = çok şiddetli)",
            min_value=1, max_value=10, value=5,
        )

        gonder = st.form_submit_button("🔍 Analiz Et", use_container_width=True)

    if gonder:
        if not sikayet.strip():
            st.error("⚠️ Lütfen şikayetinizi açıklayan bir metin girin.")
        else:
            with st.spinner("🤖 Yapay zeka şikayetinizi analiz ediyor..."):
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
        st.markdown('<div class="section-title">💬 Analiz Sonucu</div>', unsafe_allow_html=True)
        st.markdown(
            """
            <div class="triage-card" style="text-align:center; padding:48px 24px; color:#94A3B8;">
                <div style="font-size:3.5rem; margin-bottom:16px;">🤖</div>
                <div style="font-size:1rem; font-weight:500; margin-bottom:8px; color:#64748B;">
                    Yapay Zeka Bekleniyor
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

        st.markdown('<div class="section-title">✅ Analiz Sonucu</div>', unsafe_allow_html=True)

        # ── Özet kart ──────────────────────────────────────────────────────
        kart_class = "triage-card triage-card-emergency" if skor >= 8 else \
                     "triage-card triage-card-medium"    if skor >= 5 else \
                     "triage-card triage-card-low"

        brans_renk = BRANSLAR.get(sonuc["brans"], {}).get("renk", "#1A3A6B")
        brans_icon = sonuc["brans_icon"]

        st.markdown(
            f"""
            <div class="{kart_class}">
                <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:16px;">
                    <div>
                        <div style="font-size:0.78rem; color:#64748B; margin-bottom:4px; text-transform:uppercase; letter-spacing:0.5px;">Önerilen Branş</div>
                        <div style="font-size:1.6rem; font-weight:700; color:{brans_renk};">
                            {brans_icon} {sonuc["brans"]}
                        </div>
                    </div>
                    <span class="{seviye['badge']}">{seviye['emoji']} {seviye['label']}</span>
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

        # ── Sohbet baloncukları ────────────────────────────────────────────
        st.markdown('<div class="section-title" style="margin-top:16px;">💬 Değerlendirme Mesajı</div>', unsafe_allow_html=True)

        for mesaj in st.session_state.chat_gecmisi:
            if mesaj["tur"] == "kullanici":
                st.markdown(
                    f"""
                    <div style="overflow:hidden; margin-bottom:8px;">
                        <div class="chat-avatar-user">👤</div>
                        <div class="chat-bubble-user">{mesaj["mesaj"]}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    f"""
                    <div style="overflow:hidden; margin-bottom:8px;">
                        <div class="chat-avatar-ai">🤖</div>
                        <div class="chat-bubble-ai">{mesaj["mesaj"]}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        # ── Sıfırla butonu ────────────────────────────────────────────────
        if st.button("🔄 Yeni Analiz Başlat", use_container_width=True):
            st.session_state.chat_gecmisi = []
            st.session_state.analiz_tamamlandi = False
            st.session_state.analiz_sonucu = None
            st.rerun()

        # ── Etik not ──────────────────────────────────────────────────────
        st.markdown(
            """
            <div class="ethical-warning" style="margin-top:16px;">
                ⚠️ Bu sistem bir tanı koymaz. Yukarıdaki öneriler yalnızca ön bilgilendirme
                amaçlıdır ve bir sağlık profesyonelinin değerlendirmesinin yerini alamaz.
            </div>
            """,
            unsafe_allow_html=True,
        )