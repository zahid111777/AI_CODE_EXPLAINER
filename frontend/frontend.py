import streamlit as st
import requests

# ── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Code Explainer",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Fira+Code:wght@400;500&display=swap');

/* ╔══════════════════════════════════════════════╗
   ║  NUCLEAR TEXT FIX — every element gets       ║
   ║  an explicit bright color so nothing is      ║
   ║  ever invisible on the dark background.      ║
   ╚══════════════════════════════════════════════╝ */

*, *::before, *::after { box-sizing: border-box; }

/* Base font */
html, body,
section[data-testid="stAppViewContainer"],
div[data-testid="stAppViewContainer"],
.main, .block-container {
    font-family: 'Inter', sans-serif !important;
    color: #e2e8f0 !important;
}

/* ── Background ───────────────────────────────── */
[data-testid="stAppViewContainer"],
.stApp {
    background: linear-gradient(160deg, #0d0b1e 0%, #1a1040 45%, #0d1b30 100%) !important;
}
[data-testid="stHeader"],
[data-testid="stToolbar"] { background: transparent !important; }
[data-testid="stDecoration"] { display: none !important; }

/* ── Force ALL text bright ────────────────────── */
p, span, div, a, li, td, th,
h1, h2, h3, h4, h5, h6,
label, small, strong, b, em, i,
[class*="css"] {
    color: #e2e8f0 !important;
}

/* ── Widget labels (the titles above inputs) ────
   These are the "Programming Language" and
   "Paste Your Code Here" labels.               */
[data-testid="stWidgetLabel"],
[data-testid="stWidgetLabel"] *,
[data-testid="stWidgetLabel"] p,
[data-testid="stWidgetLabel"] label,
label[data-testid],
.stSelectbox > label,
.stTextArea  > label,
div[class*="InputInstructions"],
div[class*="label"] {
    color: #c4b5fd !important;
    font-weight: 700 !important;
    font-size: 0.9rem !important;
    letter-spacing: 0.05em !important;
    text-transform: none !important;
    margin-bottom: 0.35rem !important;
}

/* ── Selectbox — the closed box showing selected value ── */
[data-baseweb="select"],
[data-baseweb="select"] *,
[data-baseweb="select"] > div,
[data-baseweb="select"] > div > div,
[data-baseweb="select"] span,
[data-baseweb="select"] input,
[data-baseweb="select"] [class*="ValueContainer"],
[data-baseweb="select"] [class*="SingleValue"],
[data-baseweb="select"] [class*="singleValue"],
[data-baseweb="select"] [class*="placeholder"],
[data-baseweb="select"] [class*="Placeholder"],
[data-baseweb="select"] [role="combobox"],
[data-baseweb="select"] [role="option"] {
    color: #f1f5f9 !important;
    background: transparent !important;
    -webkit-text-fill-color: #f1f5f9 !important;
}

/* The closed selectbox container */
[data-baseweb="select"] > div:first-child {
    background: rgba(20, 16, 50, 0.85) !important;
    border: 1.5px solid rgba(167, 139, 250, 0.45) !important;
    border-radius: 12px !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
    min-height: 2.6rem !important;
}
[data-baseweb="select"] > div:first-child:hover,
[data-baseweb="select"] > div:focus-within {
    border-color: #a78bfa !important;
    box-shadow: 0 0 0 3px rgba(167, 139, 250, 0.18) !important;
}

/* Dropdown chevron icon */
[data-baseweb="select"] svg { fill: #a78bfa !important; }

/* ── Dropdown menu (open state) ─────────────── */
[data-baseweb="popover"],
[data-baseweb="popover"] *,
[data-baseweb="menu"],
[data-baseweb="menu"] *,
[role="listbox"],
[role="listbox"] * {
    background: #1a1645 !important;
    color: #e2e8f0 !important;
    border-color: rgba(167, 139, 250, 0.25) !important;
    border-radius: 12px !important;
}
[data-baseweb="menu"] [role="option"],
[data-baseweb="menu"] li {
    color: #e2e8f0 !important;
    background: transparent !important;
    padding: 0.5rem 1rem !important;
    border-radius: 8px !important;
}
[data-baseweb="menu"] [role="option"]:hover,
[data-baseweb="menu"] [aria-selected="true"] {
    background: rgba(124, 58, 237, 0.3) !important;
    color: #c4b5fd !important;
}

/* ── Textarea ────────────────────────────────── */
.stTextArea textarea,
textarea {
    font-family: 'Fira Code', monospace !important;
    font-size: 0.88rem !important;
    line-height: 1.65 !important;
    background: rgba(10, 8, 30, 0.8) !important;
    color: #e2e8f0 !important;
    -webkit-text-fill-color: #e2e8f0 !important;
    border: 1.5px solid rgba(167, 139, 250, 0.35) !important;
    border-radius: 14px !important;
    padding: 1rem 1.1rem !important;
    caret-color: #a78bfa !important;
    resize: vertical !important;
}
.stTextArea textarea:focus, textarea:focus {
    border-color: #a78bfa !important;
    box-shadow: 0 0 0 3px rgba(167, 139, 250, 0.18) !important;
    outline: none !important;
}
.stTextArea textarea::placeholder, textarea::placeholder {
    color: #4a5568 !important;
    -webkit-text-fill-color: #4a5568 !important;
}

/* ── Buttons ─────────────────────────────────── */
div.stButton > button,
button[kind="primary"],
button[kind="secondary"] {
    font-family: 'Inter', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    border-radius: 12px !important;
    padding: 0.65rem 1.4rem !important;
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
    width: 100% !important;
    border: none !important;
}

/* Primary — Explain */
button[kind="primary"],
div.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #7c3aed 0%, #2563eb 100%) !important;
    box-shadow: 0 4px 20px rgba(124, 58, 237, 0.45) !important;
}
button[kind="primary"]:hover,
div.stButton > button[kind="primary"]:hover {
    box-shadow: 0 6px 28px rgba(124, 58, 237, 0.65) !important;
    transform: translateY(-2px) !important;
}

/* Secondary — Load Example */
button[kind="secondary"],
div.stButton > button[kind="secondary"] {
    background: rgba(255, 255, 255, 0.07) !important;
    border: 1.5px solid rgba(167, 139, 250, 0.35) !important;
}
button[kind="secondary"]:hover,
div.stButton > button[kind="secondary"]:hover {
    background: rgba(124, 58, 237, 0.18) !important;
    border-color: #a78bfa !important;
    transform: translateY(-1px) !important;
}

/* Download */
[data-testid="stDownloadButton"] button {
    background: rgba(52, 211, 153, 0.1) !important;
    border: 1.5px solid rgba(52, 211, 153, 0.4) !important;
    color: #34d399 !important;
    -webkit-text-fill-color: #34d399 !important;
}
[data-testid="stDownloadButton"] button:hover {
    background: rgba(52, 211, 153, 0.22) !important;
    transform: translateY(-1px) !important;
}

/* ── Hero ─────────────────────────────────────── */
.hero-wrap { text-align: center; padding: 2.5rem 1rem 1.8rem; }

.hero-title {
    font-size: 3rem;
    font-weight: 800;
    line-height: 1.15;
    background: linear-gradient(100deg, #a78bfa 0%, #60a5fa 50%, #34d399 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent !important;
    background-clip: text;
    margin: 0 0 0.7rem !important;
}
.hero-sub {
    color: #94a3b8 !important;
    -webkit-text-fill-color: #94a3b8 !important;
    font-size: 1.05rem !important;
    margin: 0 !important;
    line-height: 1.75 !important;
}

/* ── Section label ───────────────────────────── */
.section-label {
    color: #a78bfa !important;
    -webkit-text-fill-color: #a78bfa !important;
    font-size: 0.72rem !important;
    font-weight: 800 !important;
    letter-spacing: 0.18em !important;
    text-transform: uppercase !important;
    margin-bottom: 0.7rem !important;
}

/* ── Language badge ──────────────────────────── */
.lang-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    background: linear-gradient(135deg, #7c3aed, #2563eb);
    color: #fff !important;
    -webkit-text-fill-color: #fff !important;
    font-size: 0.82rem;
    font-weight: 700;
    padding: 0.32rem 1.1rem;
    border-radius: 999px;
    margin-bottom: 1.2rem;
    box-shadow: 0 4px 16px rgba(124, 58, 237, 0.5);
}

/* ── Glass tip card ──────────────────────────── */
.glass-card {
    background: rgba(255, 255, 255, 0.042);
    border: 1px solid rgba(167, 139, 250, 0.22);
    border-radius: 18px;
    padding: 1.4rem 1.6rem;
    margin-bottom: 1.2rem;
    backdrop-filter: blur(14px);
}
.glass-card ul { margin: 0.5rem 0 0; padding-left: 1.3rem; line-height: 2.1; }
.glass-card li {
    color: #94a3b8 !important;
    -webkit-text-fill-color: #94a3b8 !important;
    font-size: 0.9rem !important;
}
.glass-card li strong {
    color: #c4b5fd !important;
    -webkit-text-fill-color: #c4b5fd !important;
}

/* ── Placeholder box ─────────────────────────── */
.placeholder-box {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 4rem 2rem;
    background: rgba(255, 255, 255, 0.022);
    border: 2px dashed rgba(167, 139, 250, 0.2);
    border-radius: 18px;
    min-height: 300px;
}
.placeholder-icon {
    font-size: 3.5rem;
    margin-bottom: 1.2rem;
    filter: drop-shadow(0 0 20px rgba(167, 139, 250, 0.55));
}
.placeholder-text {
    color: #64748b !important;
    -webkit-text-fill-color: #64748b !important;
    font-size: 0.98rem !important;
    line-height: 1.85 !important;
}
.placeholder-text strong {
    color: #a78bfa !important;
    -webkit-text-fill-color: #a78bfa !important;
}

/* ── Alerts / spinners ───────────────────────── */
[data-testid="stAlert"] { border-radius: 12px !important; }
[data-testid="stAlert"] * { color: inherit !important; }

div[data-testid="stSpinner"] > div > span,
div[data-testid="stSpinner"] p {
    color: #a78bfa !important;
    -webkit-text-fill-color: #a78bfa !important;
}

/* ── Markdown output text ────────────────────── */
[data-testid="stMarkdownContainer"] h1,
[data-testid="stMarkdownContainer"] h2,
[data-testid="stMarkdownContainer"] h3 {
    color: #a78bfa !important;
    -webkit-text-fill-color: #a78bfa !important;
}
[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] li {
    color: #cbd5e1 !important;
    -webkit-text-fill-color: #cbd5e1 !important;
    line-height: 1.85 !important;
}
[data-testid="stMarkdownContainer"] strong,
[data-testid="stMarkdownContainer"] b {
    color: #f1f5f9 !important;
    -webkit-text-fill-color: #f1f5f9 !important;
}
[data-testid="stMarkdownContainer"] code {
    background: rgba(124, 58, 237, 0.18) !important;
    color: #c4b5fd !important;
    -webkit-text-fill-color: #c4b5fd !important;
    padding: 0.1rem 0.45rem !important;
    border-radius: 5px !important;
    font-family: 'Fira Code', monospace !important;
    font-size: 0.85em !important;
}
[data-testid="stMarkdownContainer"] pre {
    background: rgba(5, 3, 15, 0.7) !important;
    border: 1px solid rgba(167, 139, 250, 0.15) !important;
    border-radius: 12px !important;
    padding: 1rem 1.2rem !important;
    overflow-x: auto !important;
}
[data-testid="stMarkdownContainer"] pre code {
    background: transparent !important;
    color: #a5f3fc !important;
    -webkit-text-fill-color: #a5f3fc !important;
}

/* ── Misc ─────────────────────────────────────── */
hr {
    border: none !important;
    border-top: 1px solid rgba(167, 139, 250, 0.13) !important;
    margin: 1.5rem 0 !important;
}
.footer {
    text-align: center;
    padding: 2rem 0 1rem;
    font-size: 0.82rem;
    color: #475569 !important;
    -webkit-text-fill-color: #475569 !important;
}
.footer strong {
    color: #7c3aed !important;
    -webkit-text-fill-color: #7c3aed !important;
}

/* ── Scrollbar ───────────────────────────────── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: rgba(255,255,255,0.03); }
::-webkit-scrollbar-thumb { background: rgba(124,58,237,0.4); border-radius: 99px; }
::-webkit-scrollbar-thumb:hover { background: rgba(124,58,237,0.65); }

[data-testid="column"] { padding: 0 0.8rem !important; }
</style>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════
# CONSTANTS
# ════════════════════════════════════════════════════════════════════════════
BACKEND_URL = "http://localhost:8000/explain"

LANGUAGES = [
    "auto-detect",
    "Python", "JavaScript", "TypeScript", "Java", "C", "C++", "C#",
    "Go", "Rust", "PHP", "Ruby", "Swift", "Kotlin", "SQL",
    "HTML/CSS", "Bash/Shell", "R", "MATLAB", "Scala", "Dart",
]

EXAMPLE_CODE = (
    'def fibonacci(n):\n'
    '    """Return the nth Fibonacci number."""\n'
    '    if n <= 1:\n'
    '        return n\n'
    '    a, b = 0, 1\n'
    '    for _ in range(2, n + 1):\n'
    '        a, b = b, a + b\n'
    '    return b\n\n'
    'print(fibonacci(10))\n'
)

# ── Session state defaults ────────────────────────────────────────────────────
if "explanation" not in st.session_state:
    st.session_state["explanation"] = None
if "detected_language" not in st.session_state:
    st.session_state["detected_language"] = ""
if "code_value" not in st.session_state:
    st.session_state["code_value"] = ""

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-wrap">
    <div class="hero-title">🤖 AI Code Explainer</div>
    <p class="hero-sub">
        Paste any code snippet and get a crystal-clear explanation —<br>
        perfect for <strong>developers, students, and complete beginners</strong> alike.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# ── Two-column layout ─────────────────────────────────────────────────────────
left, right = st.columns([1, 1], gap="large")

# ════════════════════════════════════════════════════════════════════════════
# LEFT — Input Panel
# ════════════════════════════════════════════════════════════════════════════
with left:
    st.markdown('<p class="section-label">📥  Your Code</p>', unsafe_allow_html=True)

    language = st.selectbox(
        "Programming Language",
        options=LANGUAGES,
        index=0,
        help="Select a language or use auto-detect.",
    )

    code_input = st.text_area(
        "Paste Your Code Here",
        value=st.session_state["code_value"],
        height=360,
        placeholder="# Paste or type any code here…\n# Supports ALL programming languages!",
    )

    btn_col, ex_col = st.columns([3, 2])
    with btn_col:
        explain_clicked = st.button(
            "✨  Explain This Code",
            use_container_width=True,
            type="primary",
        )
    with ex_col:
        if st.button("📄  Load Example", use_container_width=True):
            st.session_state["code_value"] = EXAMPLE_CODE
            st.rerun()

    st.markdown("""
    <div class="glass-card" style="margin-top:1.2rem;">
        <p class="section-label" style="margin-bottom:0.4rem;">💡  Pro Tips</p>
        <ul>
            <li>Works with <strong>any language</strong> — Python, JS, Java, SQL, Bash…</li>
            <li>Paste a full file <strong>or</strong> just a small snippet.</li>
            <li>Use <strong>auto-detect</strong> and let AI figure out the language.</li>
            <li>Explanations are friendly for <strong>everyone</strong>, not just coders.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════
# RIGHT — Output Panel
# ════════════════════════════════════════════════════════════════════════════
with right:
    st.markdown('<p class="section-label">📤  Explanation</p>', unsafe_allow_html=True)

    effective_code = code_input.strip()

    if explain_clicked:
        if not effective_code:
            st.warning("⚠️  Please paste some code before clicking **Explain**.")
        else:
            with st.spinner("🧠  Thinking with GPT-4o-mini…"):
                try:
                    resp = requests.post(
                        BACKEND_URL,
                        json={"code": effective_code, "language": language},
                        timeout=90,
                    )
                    resp.raise_for_status()
                    data = resp.json()
                    st.session_state["explanation"] = data["explanation"]
                    st.session_state["detected_language"] = data["detected_language"]

                except requests.exceptions.ConnectionError:
                    st.error(
                        "🔌  **Cannot connect to the backend.**  \n"
                        "Start the FastAPI server:  \n"
                        "`uvicorn backend.src.main:app --reload`"
                    )
                except requests.exceptions.Timeout:
                    st.error("⏱️  Request timed out. Please try again.")
                except requests.exceptions.HTTPError as e:
                    detail = ""
                    try:
                        detail = resp.json().get("detail", "")
                    except Exception:
                        pass
                    st.error(f"❌  Backend error: {e}.  \n{detail}")

    if st.session_state["explanation"]:
        detected = st.session_state["detected_language"] or language
        st.markdown(
            f'<span class="lang-badge">🏷️ &nbsp;{detected}</span>',
            unsafe_allow_html=True,
        )
        # Single clean render — no double output
        st.markdown(st.session_state["explanation"])

        st.markdown("<br>", unsafe_allow_html=True)
        st.download_button(
            label="⬇️  Download as Markdown",
            data=st.session_state["explanation"],
            file_name="code_explanation.md",
            mime="text/markdown",
            use_container_width=True,
        )
    else:
        st.markdown("""
        <div class="placeholder-box">
            <div class="placeholder-icon">🔮</div>
            <p class="placeholder-text">
                Your explanation will appear here.<br><br>
                Paste your code on the left, choose a language,<br>
                then hit <strong>✨ Explain This Code</strong>.
            </p>
        </div>
        """, unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("""
<div class="footer">
    Built with ❤️ &nbsp;using &nbsp;<strong>Streamlit</strong> · <strong>LangChain</strong> · <strong>OpenAI GPT-4o-mini</strong>
</div>
""", unsafe_allow_html=True)
