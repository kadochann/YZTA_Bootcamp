MAIN_CSS = """
<style>
/* ── Google Font ──────────────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* ── Global ───────────────────────────────────────────────── */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0F2544 0%, #1A3A6B 100%);
}
section[data-testid="stSidebar"] * {
    color: #E8EEF7 !important;
}
section[data-testid="stSidebar"] .stRadio label,
section[data-testid="stSidebar"] p {
    color: #B8C8E0 !important;
}

/* ── Metric kartları ──────────────────────────────────────── */
div[data-testid="metric-container"] {
    background: #ffffff;
    border: 1px solid #E2E8F0;
    border-radius: 14px;
    padding: 18px 22px;
    box-shadow: 0 2px 8px rgba(15,37,68,0.07);
    transition: box-shadow 0.2s;
}
div[data-testid="metric-container"]:hover {
    box-shadow: 0 6px 20px rgba(15,37,68,0.13);
}

/* ── Özel kart bileşeni ───────────────────────────────────── */
.triage-card {
    background: #ffffff;
    border-radius: 16px;
    padding: 24px 28px;
    border: 1px solid #E2E8F0;
    box-shadow: 0 2px 10px rgba(15,37,68,0.06);
    margin-bottom: 20px;
}
.triage-card-emergency {
    border-left: 5px solid #EF4444;
    background: linear-gradient(135deg, #FFF5F5 0%, #ffffff 60%);
}
.triage-card-medium {
    border-left: 5px solid #F59E0B;
    background: linear-gradient(135deg, #FFFBEB 0%, #ffffff 60%);
}
.triage-card-low {
    border-left: 5px solid #10B981;
    background: linear-gradient(135deg, #F0FDF4 0%, #ffffff 60%);
}

/* ── Aciliyet badge ───────────────────────────────────────── */
.badge-red {
    display: inline-block;
    background: #FEE2E2; color: #991B1B;
    border-radius: 999px; padding: 3px 12px;
    font-size: 0.78rem; font-weight: 600;
}
.badge-yellow {
    display: inline-block;
    background: #FEF3C7; color: #92400E;
    border-radius: 999px; padding: 3px 12px;
    font-size: 0.78rem; font-weight: 600;
}
.badge-green {
    display: inline-block;
    background: #D1FAE5; color: #065F46;
    border-radius: 999px; padding: 3px 12px;
    font-size: 0.78rem; font-weight: 600;
}

/* ── Chat mesaj baloncukları ─────────────────────────────── */
.chat-bubble-user {
    background: #EFF6FF;
    border-radius: 16px 16px 4px 16px;
    padding: 12px 16px;
    margin: 8px 0 8px 60px;
    color: #1E3A5F;
    font-size: 0.95rem;
    line-height: 1.5;
}
.chat-bubble-ai {
    background: #F8FAFF;
    border: 1px solid #DBEAFE;
    border-radius: 16px 16px 16px 4px;
    padding: 12px 16px;
    margin: 8px 60px 8px 0;
    color: #1E3A5F;
    font-size: 0.95rem;
    line-height: 1.5;
}
.chat-avatar-user {
    float: right; margin-left: 10px;
    background: #1E3A5F; color: white;
    width: 36px; height: 36px;
    border-radius: 50%; text-align: center;
    line-height: 36px; font-size: 1rem;
}
.chat-avatar-ai {
    float: left; margin-right: 10px;
    background: #00B4D8; color: white;
    width: 36px; height: 36px;
    border-radius: 50%; text-align: center;
    line-height: 36px; font-size: 1rem;
}

/* ── Hero banner ──────────────────────────────────────────── */
.hero-banner {
    background: linear-gradient(135deg, #0F2544 0%, #1A3A6B 50%, #00B4D8 100%);
    border-radius: 20px;
    padding: 48px 40px;
    color: white;
    margin-bottom: 32px;
}
.hero-banner h1 {
    font-size: 2.2rem;
    font-weight: 700;
    margin-bottom: 12px;
    color: white !important;
}
.hero-banner p {
    font-size: 1.05rem;
    opacity: 0.88;
    line-height: 1.6;
}

/* ── Section başlığı ─────────────────────────────────────── */
.section-title {
    font-size: 1.2rem;
    font-weight: 600;
    color: #0F2544;
    margin-bottom: 16px;
    padding-bottom: 8px;
    border-bottom: 2px solid #DBEAFE;
}

/* ── Uyarı kutusu ────────────────────────────────────────── */
.ethical-warning {
    background: #FFFBEB;
    border: 1px solid #FCD34D;
    border-left: 4px solid #F59E0B;
    border-radius: 10px;
    padding: 14px 18px;
    color: #78350F;
    font-size: 0.88rem;
    line-height: 1.5;
}

/* ── Progress bar (aciliyet) ─────────────────────────────── */
.urgency-bar-wrap {
    background: #E2E8F0;
    border-radius: 999px;
    height: 10px;
    margin: 6px 0 14px 0;
    overflow: hidden;
}
.urgency-bar-fill-red   { background: linear-gradient(90deg,#F59E0B,#EF4444); height:10px; border-radius:999px; }
.urgency-bar-fill-yellow{ background: linear-gradient(90deg,#10B981,#F59E0B); height:10px; border-radius:999px; }
.urgency-bar-fill-green { background: linear-gradient(90deg,#06B6D4,#10B981); height:10px; border-radius:999px; }

/* ── Streamlit buton override ────────────────────────────── */
.stButton > button {
    background: linear-gradient(135deg, #1A3A6B 0%, #00B4D8 100%);
    color: white !important;
    border: none;
    border-radius: 10px;
    padding: 10px 28px;
    font-weight: 600;
    font-size: 0.95rem;
    transition: opacity 0.2s, transform 0.1s;
    width: 100%;
}
.stButton > button:hover {
    opacity: 0.88;
    transform: translateY(-1px);
}

/* ── Tabs ────────────────────────────────────────────────── */
button[data-baseweb="tab"] {
    font-weight: 500;
    color: #64748B;
}
button[data-baseweb="tab"][aria-selected="true"] {
    color: #1A3A6B !important;
    border-bottom-color: #1A3A6B !important;
}

/* ── DataFrame ───────────────────────────────────────────── */
[data-testid="stDataFrame"] {
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 2px 8px rgba(15,37,68,0.06);
}

/* ── Genel scrollbar ─────────────────────────────────────── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #F1F5F9; }
::-webkit-scrollbar-thumb { background: #94A3B8; border-radius: 3px; }
</style>
"""