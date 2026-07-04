"""
mock_data.py
Ortak sahte (demo) veri ve yardımcı fonksiyonlar.
Gerçek ML/LLM entegrasyonu yapıldığında burası src/ml/ ve src/llm/ ile değiştirilir.
"""

import random
from datetime import datetime, timedelta

# ── Branş kataloğu ──────────────────────────────────────────────────────────
BRANSLAR = {
    "Dahiliye":      {"icon": "🫁", "renk": "#3B82F6"},
    "Kardiyoloji":   {"icon": "❤️",  "renk": "#EF4444"},
    "Nöroloji":      {"icon": "🧠", "renk": "#8B5CF6"},
    "Ortopedi":      {"icon": "🦴", "renk": "#F59E0B"},
    "Gastroloji":    {"icon": "🫃", "renk": "#10B981"},
    "Göz Hastalıkları": {"icon": "👁️", "renk": "#06B6D4"},
    "Kulak Burun Boğaz": {"icon": "👂", "renk": "#F97316"},
    "Deri Hastalıkları": {"icon": "🩹", "renk": "#EC4899"},
    "Psikiyatri":    {"icon": "🧘", "renk": "#6366F1"},
    "Acil":          {"icon": "🚨", "renk": "#DC2626"},
}

# ── Aciliyet seviyesi yardımcı ──────────────────────────────────────────────
def aciliyet_seviyesi(skor: int) -> dict:
    """1-10 arasındaki skoru seviyeye dönüştür."""
    if skor >= 8:
        return {"label": "Yüksek Aciliyet", "badge": "badge-red",   "bar": "urgency-bar-fill-red",    "emoji": "🔴"}
    elif skor >= 5:
        return {"label": "Orta Aciliyet",   "badge": "badge-yellow", "bar": "urgency-bar-fill-yellow", "emoji": "🟡"}
    else:
        return {"label": "Düşük Aciliyet",  "badge": "badge-green",  "bar": "urgency-bar-fill-green",  "emoji": "🟢"}

def aciliyet_kart_class(skor: int) -> str:
    if skor >= 8:  return "triage-card triage-card-emergency"
    if skor >= 5:  return "triage-card triage-card-medium"
    return "triage-card triage-card-low"

# ── Mock hasta listesi ───────────────────────────────────────────────────────
def get_mock_hastalar():
    return [
        {
            "id": "H-2026-001",
            "ad_soyad": "Ahmet Kaya",
            "yas": 54,
            "randevu": "10:30",
            "sikayet_ozeti": "3 gündür süren göğüs ağrısı ve nefes darlığı. Geçmişte hipertansiyon var.",
            "semptomlar": ["Göğüs ağrısı", "Nefes darlığı", "Çarpıntı"],
            "brans": "Kardiyoloji",
            "aciliyet_skoru": 9,
            "risk_faktorleri": ["Hipertansiyon", "Sigara kullanımı (20 yıl)", "Aile geçmişi"],
            "ai_ozeti": (
                "Hasta 54 yaşında erkek. Son 3 gündür intermittant göğüs ağrısı ve efor dispnesi "
                "mevcut. Hipertansiyon öyküsü bulunuyor. Semptom profili kardiyak etiyolojiyle "
                "uyumlu olup acil kardiyolojik değerlendirme önerilmektedir. "
                "EKG ve troponin takibi planlanabilir."
            ),
        },
        {
            "id": "H-2026-002",
            "ad_soyad": "Fatma Demir",
            "yas": 32,
            "randevu": "11:00",
            "sikayet_ozeti": "Haftadır süren baş ağrısı, ense sertliği ve ışığa hassasiyet.",
            "semptomlar": ["Baş ağrısı", "Ense sertliği", "Fotofobi", "Bulantı"],
            "brans": "Nöroloji",
            "aciliyet_skoru": 7,
            "risk_faktorleri": ["Migren öyküsü"],
            "ai_ozeti": (
                "32 yaşında kadın hasta. Şiddetli baş ağrısı, boyun sertliği ve ışığa hassasiyet "
                "ile başvuruyor. Migren geçmişi mevcut. Semptom kombinasyonu nörolojik değerlendirme "
                "gerektiriyor; meningeal irritasyon bulguları dışlanmalıdır."
            ),
        },
        {
            "id": "H-2026-003",
            "ad_soyad": "Mehmet Yılmaz",
            "yas": 41,
            "randevu": "11:30",
            "sikayet_ozeti": "2 haftadır devam eden karın ağrısı ve şişkinlik hissi.",
            "semptomlar": ["Karın ağrısı", "Şişkinlik", "İştahsızlık"],
            "brans": "Gastroloji",
            "aciliyet_skoru": 4,
            "risk_faktorleri": ["Stres", "Düzensiz beslenme"],
            "ai_ozeti": (
                "41 yaşında erkek hasta. Alt ve üst karın bölgesinde 2 haftadır süren ağrı ve "
                "gaz şikayeti mevcut. Vital bulgular stabil görünüyor. Gastroenterolojik "
                "değerlendirme planlanabilir; H.pylori ve GIS endoskopi önerilebilir."
            ),
        },
        {
            "id": "H-2026-004",
            "ad_soyad": "Ayşe Çelik",
            "yas": 28,
            "randevu": "12:00",
            "sikayet_ozeti": "Sağ dizde 1 haftadır ağrı ve şişlik, yürürken artıyor.",
            "semptomlar": ["Diz ağrısı", "Eklem şişliği", "Hareket kısıtlılığı"],
            "brans": "Ortopedi",
            "aciliyet_skoru": 3,
            "risk_faktorleri": ["Spor aktivitesi"],
            "ai_ozeti": (
                "28 yaşında kadın hasta, sağ diz ağrısı ve şişliği ile başvuruyor. "
                "Spor yapma öyküsü mevcut. Liman/menisküs patolojisi ekarte edilmeli. "
                "Fizik muayene ve gerekirse MR görüntüleme önerilmektedir."
            ),
        },
        {
            "id": "H-2026-005",
            "ad_soyad": "Hasan Koç",
            "yas": 67,
            "randevu": "13:00",
            "sikayet_ozeti": "Sabahları ellerde tutukluk, eklem ağrıları 2 aydır var.",
            "semptomlar": ["Eklem ağrısı", "Sabah tutukluğu", "Yorgunluk"],
            "brans": "Dahiliye",
            "aciliyet_skoru": 4,
            "risk_faktorleri": ["İleri yaş", "Aile geçmişi (RA)"],
            "ai_ozeti": (
                "67 yaşında erkek hasta. Bilateral el eklem tutukluğu ve ağrısı ile başvuruyor. "
                "2 aydır süren sabah tutukluğu romatoid artrit veya osteoartrit ile uyumlu. "
                "RF, anti-CCP, CRP tetkikleri istenebilir; romatoloji konsültasyonu planlanabilir."
            ),
        },
    ]

# ── Mock istatistik verileri ─────────────────────────────────────────────────
def get_mock_istatistikler():
    branslar = list(BRANSLAR.keys())
    return {
        "toplam_hasta":   247,
        "bugun_hasta":    18,
        "ort_aciliyet":   5.2,
        "en_sik_brans":   "Dahiliye",
        "brans_dagilim": {b: random.randint(10, 60) for b in branslar},
        "gunluk_hasta": {
            (datetime.today() - timedelta(days=i)).strftime("%d %b"): random.randint(12, 35)
            for i in range(13, -1, -1)
        },
        "aciliyet_dagilim": {
            "Düşük (1-4)":   89,
            "Orta (5-7)":    118,
            "Yüksek (8-10)": 40,
        },
    }

# ── Mock LLM analiz sonucu ───────────────────────────────────────────────────
def mock_llm_analiz(sikayet_metni: str, yas: int) -> dict:
    """
    Gerçek Gemini API bağlandığında bu fonksiyon src/llm/gemini_client.py ile değiştirilir.
    Şimdilik deterministik bir demo çıktısı döndürür.
    """
    sikayet_lower = sikayet_metni.lower()

    if any(k in sikayet_lower for k in ["göğüs", "kalp", "nefes", "çarpıntı"]):
        brans, skor = "Kardiyoloji", 8
    elif any(k in sikayet_lower for k in ["baş", "baş ağrı", "ense", "baş dön"]):
        brans, skor = "Nöroloji", 6
    elif any(k in sikayet_lower for k in ["karın", "mide", "bulantı", "kusma", "ishal"]):
        brans, skor = "Gastroloji", 5
    elif any(k in sikayet_lower for k in ["diz", "eklem", "kemik", "bel", "sırt"]):
        brans, skor = "Ortopedi", 3
    elif any(k in sikayet_lower for k in ["göz", "görme"]):
        brans, skor = "Göz Hastalıkları", 4
    elif any(k in sikayet_lower for k in ["kulak", "boğaz", "burun"]):
        brans, skor = "Kulak Burun Boğaz", 3
    elif any(k in sikayet_lower for k in ["cilt", "kaşıntı", "döküntü"]):
        brans, skor = "Deri Hastalıkları", 2
    else:
        brans, skor = "Dahiliye", 4

    # Yaşa göre skoru hafif artır
    if yas > 60:
        skor = min(skor + 1, 10)

    semptomlar = []
    kelimeler = sikayet_metni.replace(",", " ").replace(".", " ").split()
    for s in ["ağrı", "ateş", "öksürük", "bulantı", "halsizlik", "baş dönmesi",
              "nefes", "çarpıntı", "şişlik", "tutulma"]:
        if s in sikayet_lower:
            semptomlar.append(s.capitalize())

    return {
        "brans": brans,
        "brans_icon": BRANSLAR[brans]["icon"],
        "aciliyet_skoru": skor,
        "semptomlar": semptomlar if semptomlar else ["Genel şikayet"],
        "hasta_mesaji": (
            f"Şikayetlerinizi aldım. Belirttiğiniz semptomlar değerlendirildiğinde, "
            f"**{brans}** bölümüyle görüşmeniz önerilebilir. "
            f"Aciliyet durumunuz **{aciliyet_seviyesi(skor)['label']}** olarak değerlendirildi.\n\n"
            f"⚠️ *Bu sistem bir tanı koymaz; yalnızca ön bilgilendirme amaçlıdır. "
            f"Nihai karar hekiminize aittir.*"
        ),
        "hekim_ozeti": (
            f"{yas} yaşında hasta. Şikayetleri şunları içeriyor: {sikayet_metni[:120]}... "
            f"Semptom profili {brans} ile uyumlu görünmektedir. "
            f"Aciliyet skoru {skor}/10 olarak hesaplanmıştır."
        ),
    }