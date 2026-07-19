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

/* ── Metric kartları ──────────────────────────────────────── */
div[data-testid="metric-container"] {
    background: var(--secondary-background-color, #ffffff) !important;
    border: 1px solid rgba(128, 128, 128, 0.2) !important;
    border-radius: 14px;
    padding: 18px 22px;
    box-shadow: 0 2px 8px rgba(15,37,68,0.07);
    transition: box-shadow 0.2s;
    color: var(--text-color, #0F2544) !important;
}
div[data-testid="metric-container"]:hover {
    box-shadow: 0 6px 20px rgba(15,37,68,0.13);
}

/* ── Özel kart bileşeni ───────────────────────────────────── */
.triage-card {
    background: var(--secondary-background-color, #ffffff) !important;
    border-radius: 16px;
    padding: 24px 28px;
    border: 1px solid rgba(128, 128, 128, 0.2) !important;
    box-shadow: 0 2px 10px rgba(15,37,68,0.06);
    margin-bottom: 20px;
    color: var(--text-color, #0F2544) !important;
}
.triage-card-emergency {
    border-left: 5px solid #EF4444 !important;
    background: linear-gradient(135deg, rgba(239, 68, 68, 0.08) 0%, var(--secondary-background-color, #ffffff) 60%) !important;
}
.triage-card-medium {
    border-left: 5px solid #F59E0B !important;
    background: linear-gradient(135deg, rgba(245, 158, 11, 0.08) 0%, var(--secondary-background-color, #ffffff) 60%) !important;
}
.triage-card-low {
    border-left: 5px solid #10B981 !important;
    background: linear-gradient(135deg, rgba(16, 185, 129, 0.08) 0%, var(--secondary-background-color, #ffffff) 60%) !important;
}

/* ── Aciliyet badge ───────────────────────────────────────── */
.badge-red {
    display: inline-block;
    background: rgba(239, 68, 68, 0.15) !important; 
    color: #EF4444 !important;
    border: 1px solid rgba(239, 68, 68, 0.2) !important;
    border-radius: 999px; padding: 3px 12px;
    font-size: 0.78rem; font-weight: 600;
}
.badge-yellow {
    display: inline-block;
    background: rgba(245, 158, 11, 0.15) !important; 
    color: #F59E0B !important;
    border: 1px solid rgba(245, 158, 11, 0.2) !important;
    border-radius: 999px; padding: 3px 12px;
    font-size: 0.78rem; font-weight: 600;
}
.badge-green {
    display: inline-block;
    background: rgba(16, 185, 129, 0.15) !important; 
    color: #10B981 !important;
    border: 1px solid rgba(16, 185, 129, 0.2) !important;
    border-radius: 999px; padding: 3px 12px;
    font-size: 0.78rem; font-weight: 600;
}

/* ── Chat mesaj baloncukları ─────────────────────────────── */
.chat-bubble-user {
    background: rgba(30, 58, 95, 0.08) !important;
    border: 1px solid rgba(30, 58, 95, 0.12) !important;
    border-radius: 16px 16px 4px 16px;
    padding: 12px 16px;
    margin: 8px 0;
    color: var(--text-color, #1E3A5F) !important;
    font-size: 0.95rem;
    line-height: 1.5;
}
.chat-bubble-ai {
    background: var(--secondary-background-color, #F8FAFF) !important;
    border: 1px solid rgba(30, 58, 95, 0.12) !important;
    border-radius: 16px 16px 16px 4px;
    padding: 12px 16px;
    margin: 8px 0;
    color: var(--text-color, #1E3A5F) !important;
    font-size: 0.95rem;
    line-height: 1.5;
}

/* ── Custom Navbar ────────────────────────────────────────── */
.custom-navbar {
    background: linear-gradient(135deg, #0F2544 0%, #1A3A6B 100%) !important;
    padding: 16px 24px;
    border-radius: 12px;
    color: #ffffff !important;
    margin-bottom: 24px;
    box-shadow: 0 4px 12px rgba(15, 37, 68, 0.1);
    display: flex;
    align-items: center;
}
.navbar-title {
    font-size: 1.4rem;
    font-weight: 700;
    letter-spacing: 0.5px;
}

/* ── Hero banner ──────────────────────────────────────────── */
.hero-banner {
    background: linear-gradient(135deg, #0F2544 0%, #1A3A6B 50%, #00B4D8 100%) !important;
    border-radius: 20px;
    padding: 48px 40px;
    color: white !important;
    margin-bottom: 32px;
}
.hero-banner h1 {
    font-size: 2.2rem;
    font-weight: 700;
    margin-bottom: 12px;
    color: white !important;
}
.hero-banner h2 {
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
    color: var(--text-color, #0F2544) !important;
    margin-bottom: 16px;
    padding-bottom: 8px;
    border-bottom: 2px solid rgba(128, 128, 128, 0.2) !important;
}

/* ── Uyarı kutusu ────────────────────────────────────────── */
.ethical-warning {
    background: rgba(245, 158, 11, 0.08) !important;
    border: 1px solid rgba(245, 158, 11, 0.2) !important;
    border-left: 4px solid #F59E0B !important;
    border-radius: 10px;
    padding: 14px 18px;
    color: var(--text-color, #78350F) !important;
    font-size: 0.88rem;
    line-height: 1.5;
}

/* ── Streamlit Header & Sidebar Hiding ────────────────────── */
header, 
.stAppHeader, 
[data-testid="stHeader"] {
    display: none !important;
    height: 0px !important;
    min-height: 0px !important;
    padding: 0 !important;
    margin: 0 !important;
    visibility: hidden !important;
    opacity: 0 !important;
}
div.block-container, 
[data-testid="stAppViewBlockContainer"], 
.main .block-container {
    padding-top: 8rem !important; /* Space for sticky navbar */
    margin-top: 0rem !important;
}
[data-testid="collapsedSidebar"], 
section[data-testid="stSidebar"], 
button[data-testid="stSidebarCollapseButton"] {
    display: none !important;
}

/* ── Sticky Top Navbar ────────────────────────────────────── */
div.st-key-navbar {
    position: fixed !important;
    top: 0 !important;
    left: 0 !important;
    right: 0 !important;
    width: 100% !important;
    background: linear-gradient(135deg, #0F2544 0%, #1A3A6B 100%) !important;
    z-index: 99999 !important;
    border-bottom: 1px solid #E2E8F0 !important;
    padding: 14px 40px !important;
    box-shadow: 0 4px 12px rgba(15,37,68,0.06) !important;
}

/* ── Custom page links (Navbar & General site) ────────────── */
div[data-testid="stPageLink"] {
    background: #ffffff !important;
    border: 1px solid #E2E8F0 !important;
    border-radius: 12px !important;
    box-shadow: 0 2px 6px rgba(0,0,0,0.05) !important;
    transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
}
div[data-testid="stPageLink"]:hover {
    background: #F8FAFF !important;
    border-color: #1A3A6B !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 4px 15px rgba(0,0,0,0.12) !important;
}
div[data-testid="stPageLink"] a {
    color: #0F2544 !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    padding: 8px 16px !important;
    text-decoration: none !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
}
div[data-testid="stPageLink"]:hover a {
    color: #1A3A6B !important;
}

/* ── Multiselect selected tag chips ───────────────────────── */
div[data-baseweb="tag"] {
    background-color: var(--secondary-background-color, #ffffff) !important;
    color: var(--text-color, #0F2544) !important;
    border: 1px solid rgba(128, 128, 128, 0.25) !important;
    border-radius: 6px !important;
}
div[data-baseweb="tag"] span {
    color: var(--text-color, #0F2544) !important;
}
div[data-baseweb="tag"] svg {
    fill: var(--text-color, #0F2544) !important;
}

/* ── Progress bar (aciliyet) ─────────────────────────────── */
.urgency-bar-wrap {
    background: rgba(128, 128, 128, 0.2) !important;
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

/* ── Genel scrollbar ─────────────────────────────────────── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #F1F5F9; }
::-webkit-scrollbar-thumb { background: #94A3B8; border-radius: 3px; }
</style>

<script>
// Prevent Streamlit's default keyboard shortcuts (like C and R) outside input controls
const blockStreamlitShortcuts = (e) => {
    const key = e.key.toLowerCase();
    // Intercept single 'c' and 'r' keydowns (not triggered via Ctrl / Cmd / Alt / Shift combinations)
    if ((key === 'c' || key === 'r') && !e.ctrlKey && !e.metaKey && !e.altKey) {
        const active = document.activeElement;
        // If focusing on editable fields, let the event pass
        if (active && (
            active.tagName === 'INPUT' || 
            active.tagName === 'TEXTAREA' || 
            active.isContentEditable
        )) {
            return;
        }
        e.stopImmediatePropagation();
        e.stopPropagation();
    }
};

// Register in capture phase on both current window and the parent frame (if inside an iframe)
window.addEventListener('keydown', blockStreamlitShortcuts, true);
if (window.parent) {
    window.parent.addEventListener('keydown', blockStreamlitShortcuts, true);
}
</script>
"""