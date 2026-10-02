import base64
import html
from io import BytesIO
import os

import requests
import streamlit as st
from PIL import Image, ImageDraw
from dotenv import load_dotenv

load_dotenv()

API_URL = "http://127.0.0.1:8000/legal/api/v1/ask"
headers = {"X-API-Key": os.getenv("API_KEY")}

LOGO_PATH = "assets/symbol_of_jordan.png"

EXAMPLES = [
    "كم مدة إجازة الأمومة؟",
    "ما هي حقوقي عند الفصل التعسفي؟",
    "كم يوم إجازة سنوية من حقي؟",]

st.set_page_config(
    page_title="مساعد قانون العمل الأردني",
    page_icon="⚖️",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ==========================================================
# Styles
# ==========================================================

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800&display=swap');

:root {
    --navy: #12355B;
    --gold: #9C7A2F;
    --bg: #F6F7F9;
    --border: #E1E5EB;
    --muted: #667085;
}

/* إخفاء عناصر ستريمليت الافتراضية */
#MainMenu, footer, header,
[data-testid="stToolbar"], [data-testid="stDecoration"] { display: none !important; }

.stApp { background: var(--bg); direction: rtl; }
.block-container { max-width: 860px; padding-top: 2rem; padding-bottom: 3rem; }

.stApp, .stMarkdown, p, li, h1, h2, h3, label, textarea, button {
    font-family: 'Cairo', sans-serif !important;
}
[data-testid="stMarkdownContainer"] { direction: rtl; text-align: right; }
[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] li { line-height: 2; font-size: 17px; color: #1D2939; }
[data-testid="stMarkdownContainer"] ol,
[data-testid="stMarkdownContainer"] ul { padding-right: 1.6rem; padding-left: 0; }
[data-testid="stMarkdownContainer"] li { margin-bottom: .6rem; }

/* الترويسة */
.hero { text-align: center; padding: 1rem 0 1.5rem; }
.hero img { width: 96px; height: auto; margin-bottom: .6rem; }
.hero .kingdom { font-size: 15px; color: var(--muted); font-weight: 600; }
.hero .ministry { font-size: 19px; color: var(--navy); font-weight: 700; }
.hero .title { font-size: 38px; color: var(--navy); font-weight: 800; margin: .8rem 0 .4rem; line-height: 1.4; }
.hero .subtitle { font-size: 16px; color: var(--muted); line-height: 1.9; max-width: 560px; margin: 0 auto; }
.hero .rule { width: 64px; height: 3px; background: var(--gold); border-radius: 2px; margin: 1.2rem auto 0; }

/* حقل السؤال */
div[data-testid="stTextArea"] label { direction: rtl; text-align: right; display: block; width: 100%; }
div[data-testid="stTextArea"] label p { font-weight: 700; color: var(--navy); font-size: 16px; }
div[data-baseweb="textarea"] { border-radius: 12px; border: 1px solid var(--border); background: #fff; }
div[data-baseweb="textarea"]:focus-within { border-color: var(--navy); box-shadow: 0 0 0 3px rgba(18,53,91,.12); }
textarea { direction: rtl !important; text-align: right !important; font-size: 17px !important; background: #fff !important; }
textarea::placeholder { direction: rtl; text-align: right; color: #98A2B3; }

/* الأزرار */
.stButton > button {
    border-radius: 10px; border: 1px solid var(--border); background: #fff;
    color: var(--navy); font-weight: 600; transition: all .15s;
}
.stButton > button:hover { border-color: var(--navy); color: var(--navy); }
.stButton > button[kind="primary"] {
    background: var(--navy); color: #fff; border: none; height: 3rem; font-size: 17px; font-weight: 700;
}
.stButton > button[kind="primary"]:hover { background: #0D2A4A; color: #fff; }
.stButton > button:focus-visible { outline: 2px solid var(--gold); outline-offset: 2px; }

/* الإجابة والمراجع */
.section-title {
    color: var(--navy); font-size: 22px; font-weight: 800; margin: 2rem 0 .8rem;
    padding-right: .8rem; border-right: 4px solid var(--gold);
}
div[data-testid="stVerticalBlockBorderWrapper"] { background: #fff; border-radius: 14px; border-color: var(--border); }
.source-box {
    background: #fff; border: 1px solid var(--border); border-right: 4px solid var(--navy);
    border-radius: 10px; padding: .9rem 1.1rem; margin-bottom: .7rem; line-height: 1.9; font-size: 15px;
}
.source-box .label { color: var(--muted); font-weight: 600; margin-left: .4rem; }
.source-box .value { color: #1D2939; }

.disclaimer { color: var(--muted); font-size: 13.5px; line-height: 1.9; text-align: center; margin-top: 2.5rem; }
.disclaimer hr { border: none; border-top: 1px solid var(--border); margin-bottom: 1rem; }
</style>
""",
    unsafe_allow_html=True,
)

# ==========================================================
# Header
# ==========================================================


@st.cache_data
def load_logo_b64(path: str) -> str | None:
    """Loads the logo and removes the light (checkerboard/white) background
    connected to the image edges, so it sits cleanly on the page."""
    try:
        img = Image.open(path).convert("RGBA")
    except Exception:
        return None

    w, h = img.size
    for xy in [(0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1)]:
        ImageDraw.floodfill(img, xy, (255, 255, 255, 0), thresh=90)

    buf = BytesIO()
    img.save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode()


logo_b64 = load_logo_b64(LOGO_PATH)
logo_html = f'<img src="data:image/png;base64,{logo_b64}" alt="شعار المملكة">' if logo_b64 else ""

st.markdown(
    f"""<div class="hero">
{logo_html}
<div class="kingdom">المملكة الأردنية الهاشمية</div>
<div class="ministry">وزارة العمل</div>
<div class="title">مساعد قانون العمل الأردني</div>
<div class="subtitle">اسأل عن حقوقك وواجباتك في العمل، والإجابة تستند إلى التشريعات الأردنية والمصادر الرسمية.</div>
<div class="rule"></div>
</div>""",
    unsafe_allow_html=True,
)

# ==========================================================
# Question
# ==========================================================


def set_question(text: str):
    st.session_state["question"] = text


question = st.text_area(
    "اكتب سؤالك هنا",
    key="question",
    height=150,
    placeholder="مثال: كم مدة إجازة الأمومة في قانون العمل الأردني؟",
)

cols = st.columns(len(EXAMPLES))
for col, example in zip(cols, EXAMPLES):
    col.button(example, on_click=set_question, args=(
        example,), use_container_width=True)

st.markdown("""
<style>
div.stButton > button[kind="primary"] p {
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

ask = st.button("بحث", type="primary", use_container_width=True)

# ==========================================================
# Ask API
# ==========================================================

if ask:
    if not question.strip():
        st.warning("يرجى كتابة سؤالك أولًا.")
        st.stop()

    with st.spinner("جارٍ البحث في المصادر القانونية..."):
        try:
            response = requests.post(
                API_URL, json={"question": question}, headers=headers, timeout=120)
            response.raise_for_status()
            rag = response.json()["rag_response"]
            answer = rag.get("answer", "لم يتم العثور على إجابة.")
            sources = rag.get("sources", [])

        except requests.exceptions.ConnectionError:
            st.error(
                "تعذّر الاتصال بالخادم. تأكد من تشغيل الـ API ثم أعد المحاولة.")
            st.stop()
        except Exception as e:
            st.error(f"حدث خطأ غير متوقع:\n\n{e}")
            st.stop()

    st.markdown('<div class="section-title">الإجابة</div>',
                unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown(answer)  # يعرض الماركداون (قوائم وخط عريض) بشكل صحيح

    if sources:
        st.markdown(
            '<div class="section-title">المراجع القانونية</div>', unsafe_allow_html=True)
        for s in sources:
            st.markdown(
                f"""<div class="source-box">
<div><span class="label">المصدر:</span><span class="value">{html.escape(str(s.get("source", "")))}</span></div>
<div><span class="label">المرجع:</span><span class="value">{html.escape(str(s.get("reference", "")))}</span></div>
</div>""",
                unsafe_allow_html=True,
            )

# ==========================================================
# Footer
# ==========================================================

st.markdown(
    """<div class="disclaimer">
<hr>
تعتمد الإجابات على التشريعات والمصادر القانونية الرسمية، ولا تغني عن الاستشارة القانونية المتخصصة عند الحاجة.<br>
© 2026 وزارة العمل
</div>""",
    unsafe_allow_html=True,
)
