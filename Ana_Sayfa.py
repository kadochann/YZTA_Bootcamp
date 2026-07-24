"""
app.py  ─  Ana giriş noktası & Anasayfa
Çalıştırmak için:  streamlit run app.py
"""

import streamlit as st
import sys, os

# ── Proje kök dizinini Python path'e ekle ────────────────────────────────────
sys.path.insert(0, os.path.dirname(__file__))

from src.utils.styles import MAIN_CSS
import time
import requests

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

        cinsiyet = st.selectbox("Cinsiyet", ["Erkek", "Kadın"])

        sikayet = st.text_area(
            "Şikayetinizi anlatın",
            placeholder=(
                "Örn: Üç gündür göğsümün sol tarafında yanma hissi var, "
                "merdiven çıkınca nefes darlığı oluyor ve hafif çarpıntı yaşıyorum..."
            ),
            height=140,
        )

        gonder = st.form_submit_button("Analiz Et", use_container_width=True)

    if gonder:
        if not sikayet.strip():
            st.error("Lütfen şikayetinizi açıklayan bir metin girin.")
        else:
            with st.spinner("Yapay zeka şikayetinizi analiz ediyor (API)..."):
                try:
                    payload = {
                        "full_name": ad_soyad or 'Hasta',
                        "age": yas,
                        "sex": "M" if cinsiyet == "Erkek" else "E",
                        "complaint": sikayet
                    }
                    response = requests.post("http://127.0.0.1:8000/triage", json=payload)
                    response.raise_for_status()
                    sonuc = response.json()
                    
                    st.session_state.chat_gecmisi.append({
                        "tur": "kullanici",
                        "mesaj": f"**{ad_soyad or 'Hasta'}** ({yas} yaş)\n\n{sikayet}",
                    })
                    
                    top_p = sonuc.get("prediction", {}).get("top_prediction", {}).get("pathology", "Bilinmiyor")
                    st.session_state.chat_gecmisi.append({
                        "tur": "ai",
                        "mesaj": f"Şikayetleriniz alındı ve değerlendirildi. Yüksek olasılıklı durum: **{top_p}**. Bu bir tanı değildir, lütfen en kısa sürede doktorunuza başvurun."
                    })
                    
                    st.session_state.analiz_sonucu = sonuc
                    st.session_state.analiz_tamamlandi = True
                    st.rerun()
                except Exception as e:
                    st.error(f"API Hatası: {e}")

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
        
        # API Response structure mapping
        hasta_adi = sonuc.get("patient_name", "Hasta")
        yas = sonuc.get("age", 0)
        cins = "Erkek" if sonuc.get("sex") == "M" else "Kadın" if sonuc.get("sex") == "E" else "Bilinmiyor"
        skor = sonuc.get("urgency", 5)
        semptomlar = sonuc.get("symptoms", [])
        
        prediction = sonuc.get("prediction", {})
        top_pred = prediction.get("top_prediction", {}).get("pathology", "Bilinmiyor")
        top_prob = prediction.get("top_prediction", {}).get("probability", 0) * 100
        
        differentials = prediction.get("differential", [])
        
        # Colors for urgency
        if skor >= 8:
            urgency_color = "#DC2626" # Red
            urgency_label = "Yüksek Aciliyet"
            kart_class = "triage-card triage-card-emergency"
        elif skor >= 5:
            urgency_color = "#F59E0B" # Yellow
            urgency_label = "Orta Aciliyet"
            kart_class = "triage-card triage-card-medium"
        else:
            urgency_color = "#10B981" # Green
            urgency_label = "Düşük Aciliyet"
            kart_class = "triage-card triage-card-low"

        st.markdown('<div class="section-title">Analiz Sonucu</div>', unsafe_allow_html=True)

        # Differential list HTML
        diff_html = ""
        for i, diff in enumerate(differentials[:3]):
            pathology = diff.get("pathology", "")
            prob = diff.get("probability", 0) * 100
            diff_html += f'<li style="margin-bottom: 4px;"><b>{pathology}</b> (%{prob:.1f})</li>'

        st.markdown(
            f"""
            <div class="{kart_class}">
                <div style="border-bottom: 1px solid #E2E8F0; padding-bottom: 12px; margin-bottom: 16px;">
                    <div style="font-size: 1.1rem; font-weight: 600; color: #1E293B;">{hasta_adi}</div>
                    <div style="font-size: 0.9rem; color: #64748B;">Yaş: {yas} | Cinsiyet: {cins}</div>
                </div>

                <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:16px;">
                    <div>
                        <div style="font-size:0.78rem; color:#64748B; margin-bottom:4px; text-transform:uppercase; letter-spacing:0.5px;">En Olası Durum (Tahmin)</div>
                        <div style="font-size:1.6rem; font-weight:800; color:#1E293B;">
                            {top_pred} <span style="font-size: 1rem; color: #64748B; font-weight: normal;">(%{top_prob:.1f})</span>
                        </div>
                    </div>
                    <div style="text-align: right;">
                        <div style="font-size:0.78rem; color:#64748B; margin-bottom:4px; text-transform:uppercase; letter-spacing:0.5px;">Aciliyet Skoru</div>
                        <div style="font-size: 1.6rem; font-weight: 800; color: {urgency_color};">
                            {skor}/10
                        </div>
                        <div style="font-size: 0.85rem; font-weight: 600; color: {urgency_color};">{urgency_label}</div>
                    </div>
                </div>

                <div style="font-size:0.9rem; color:#475569; margin-bottom: 16px;">
                    <div style="font-weight: 600; margin-bottom: 4px;">Ayırıcı Tanılar (İlk 3):</div>
                    <ul style="margin-top: 0; padding-left: 20px; color: #475569;">
                        {diff_html}
                    </ul>
                </div>

                <div style="font-size:0.82rem; color:#64748B; border-top: 1px solid #E2E8F0; padding-top: 12px;">
                    <b>Tespit edilen semptomlar:</b> {", ".join(semptomlar) if semptomlar else "—"}
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