import joblib
import pandas as pd
import streamlit as st


st.set_page_config(
    page_title="سامانه تحلیل سلامت قلب و عروق",
    page_icon="❤️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@400;500;600;700;800&display=swap');

:root {
    --bg: #0d1b24;
    --surface: #122130;
    --surface-raised: #172c3d;
    --border: #1e3a4f;
    --accent: oklch(72% 0.18 185);
    --accent-dim: oklch(55% 0.14 185);
    --text: oklch(96% 0.01 220);
    --text-muted: oklch(72% 0.03 220);
    --success: oklch(70% 0.17 145);
    --warning: oklch(78% 0.18 65);
    --radius-sm: 10px;
    --radius-md: 16px;
    --radius-lg: 22px;
    --space-1: 4px;
    --space-2: 8px;
    --space-3: 16px;
    --space-4: 24px;
    --space-5: 32px;
}

html, body, .stApp,
[class*="css"],
[data-testid="stAppViewContainer"],
[data-testid="stMarkdownContainer"],
[data-testid="stWidgetLabel"],
[data-testid="stCaptionContainer"],
[data-testid="stAlert"],
[data-testid="stExpander"] {
    font-family: 'Vazirmatn', sans-serif !important;
    direction: rtl !important;
    text-align: right !important;
}

.stApp {
    background: radial-gradient(ellipse at 15% 0%, #0e2233 0%, transparent 50%),
                linear-gradient(160deg, #0d1b24 0%, #0a1520 100%);
    color: var(--text);
}

.block-container {
    max-width: 1160px;
    padding-top: var(--space-4);
    padding-bottom: var(--space-5);
}

header[data-testid="stHeader"] { background: transparent; }

h1, h2, h3, p, label {
    color: var(--text);
    text-align: right;
}

/* ── Hero ── */
.hero {
    background: linear-gradient(130deg, #152f42 0%, #0f2234 60%, #133544 100%);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    padding: var(--space-4) var(--space-5);
    margin-bottom: var(--space-4);
}

.hero-tag {
    color: var(--accent);
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 0.04em;
    text-transform: uppercase;
}

.hero-title {
    font-size: clamp(22px, 4vw, 30px);
    font-weight: 800;
    margin: var(--space-2) 0 var(--space-2);
    color: oklch(97% 0.01 210);
    line-height: 1.3;
}

.hero-desc {
    color: var(--text-muted);
    font-size: 14px;
    line-height: 1.9;
    max-width: 640px;
}

/* ── Metric cards ── */
.metric-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: var(--space-3) var(--space-3);
    text-align: center;
    min-height: 96px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: var(--space-1);
}

.metric-label {
    color: var(--text-muted);
    font-size: 12px;
    font-weight: 500;
}

.metric-value {
    color: var(--accent);
    font-size: 20px;
    font-weight: 800;
}

/* ── Section headers ── */
.section-head {
    border-right: 3px solid var(--accent);
    padding-right: var(--space-2);
    margin-bottom: var(--space-3);
}

.section-heading {
    color: var(--accent);
    font-size: 15px;
    font-weight: 700;
    margin: 0 0 2px;
}

.section-sub {
    color: var(--text-muted);
    font-size: 12px;
    margin: 0;
}

/* ── Inputs ── */
div[data-baseweb="input"] > div,
div[data-baseweb="select"] > div,
div[data-baseweb="textarea"] > div {
    background: #0a1724 !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-sm) !important;
    color: var(--text) !important;
    transition: border-color 0.15s ease;
}

div[data-baseweb="input"] > div:focus-within,
div[data-baseweb="select"] > div:focus-within {
    border-color: var(--accent-dim) !important;
    outline: 2px solid color-mix(in oklch, var(--accent) 25%, transparent) !important;
    outline-offset: 0 !important;
}

input, textarea {
    color: var(--text) !important;
    font-family: 'Vazirmatn', sans-serif !important;
    direction: rtl !important;
    text-align: right !important;
}

div[data-baseweb="select"] span { color: var(--text) !important; }

div[data-baseweb="popover"],
div[data-baseweb="menu"],
ul[role="listbox"],
li[role="option"] {
    direction: rtl !important;
    text-align: right !important;
    font-family: 'Vazirmatn', sans-serif !important;
}

[data-testid="stNumberInput"] button {
    background: var(--surface-raised) !important;
    color: var(--accent) !important;
    border: none !important;
    min-width: 44px;
    min-height: 44px;
}

/* ── Submit button ── */
div.stButton > button,
div[data-testid="stFormSubmitButton"] > button {
    background: linear-gradient(90deg, var(--accent-dim), var(--accent)) !important;
    color: #061520 !important;
    border: none !important;
    border-radius: var(--radius-sm) !important;
    font-family: 'Vazirmatn', sans-serif !important;
    font-size: 15px !important;
    font-weight: 800 !important;
    padding: 13px 22px !important;
    min-height: 48px;
    width: 100%;
    transition: filter 0.15s ease, transform 0.1s ease;
}

div.stButton > button:hover,
div[data-testid="stFormSubmitButton"] > button:hover {
    filter: brightness(1.1);
    transform: translateY(-1px);
}

div.stButton > button:focus-visible,
div[data-testid="stFormSubmitButton"] > button:focus-visible {
    outline: 2px solid var(--accent);
    outline-offset: 3px;
}

/* ── Result card ── */
.result-card {
    background: linear-gradient(135deg, #122d3e, #0f2334);
    border: 1px solid #265566;
    border-radius: var(--radius-md);
    padding: var(--space-4);
    margin-top: var(--space-3);
}

.result-title {
    color: oklch(96% 0.01 210);
    font-size: 18px;
    font-weight: 800;
    margin-bottom: var(--space-2);
}

.result-score {
    color: var(--text-muted);
    font-size: 14px;
    line-height: 1.8;
}

.result-score b { color: var(--accent); }

/* ── Alerts ── */
div[data-testid="stAlert"] {
    border-radius: var(--radius-sm);
    direction: rtl;
    text-align: right;
}

hr { border-color: var(--border); margin: var(--space-4) 0; }
footer, #MainMenu { visibility: hidden; }
.stDataFrame { direction: rtl; }

@media (max-width: 700px) {
    .hero { padding: var(--space-3); }
    .hero-title { font-size: 20px; }
}
</style>
""",
    unsafe_allow_html=True,
)


# ── بارگذاری مدل ──────────────────────────────────────────
@st.cache_resource
def load_model():
    return joblib.load("cardio_model.joblib")


try:
    model = load_model()
except Exception:
    st.error(
        "مدل بارگذاری نشد. مطمئن شو فایل cardio_model.joblib "
        "کنار فایل app.py قرار دارد."
    )
    st.stop()


# ── Hero ──────────────────────────────────────────────────
st.markdown(
    """
<div class="hero">
    <div class="hero-tag">سامانه هوشمند پایش سلامت</div>
    <div class="hero-title">سامانه تحلیل سلامت قلب و عروق</div>
    <div class="hero-desc">
        اطلاعات سلامت را وارد کن تا مدل، ورودی‌ها را بر اساس الگوهای
        موجود در مجموعه دادهٔ بیماری‌های قلبی‌عروقی تحلیل کند.
    </div>
</div>
""",
    unsafe_allow_html=True,
)


# ── کارت‌های خلاصه ───────────────────────────────────────
c1, c2, c3 = st.columns(3)
for col, label, val in [
    (c1, "نوع سامانه", "هوش مصنوعی"),
    (c2, "حوزه تحلیل", "سلامت قلب و عروق"),
    (c3, "وضعیت خروجی", "آزمایشی"),
]:
    with col:
        st.markdown(
            f'<div class="metric-card">'
            f'<div class="metric-label">{label}</div>'
            f'<div class="metric-value">{val}</div>'
            f"</div>",
            unsafe_allow_html=True,
        )

st.write("")
st.info(
    "توجه: این پروژه آموزشی است و نتیجهٔ آن تشخیص پزشکی نیست. "
    "برای ارزیابی وضعیت سلامت با پزشک مشورت کن."
)

st.markdown("## ثبت اطلاعات")
st.caption("فیلدها را بر اساس اطلاعات معتبر تکمیل کن.")


# ── فرم ──────────────────────────────────────────────────
with st.form("cardio_form"):
    left, right = st.columns(2, gap="large")

    with left:
        st.markdown(
            '<div class="section-head">'
            '<p class="section-heading">۰۱ ـ مشخصات فیزیکی</p>'
            '<p class="section-sub">سن، جنسیت و اندازه‌گیری‌های بدنی</p>'
            "</div>",
            unsafe_allow_html=True,
        )

        age = st.number_input("سن (سال)", min_value=1, max_value=100, value=45)
        gender = st.selectbox(
            "جنسیت",
            [(0, "زن"), (1, "مرد")],
            format_func=lambda x: x[1],
        )
        height = st.number_input(
            "قد (سانتی‌متر)", min_value=100, max_value=220, value=170
        )
        weight = st.number_input(
            "وزن (کیلوگرم)", min_value=30, max_value=200, value=70
        )

        st.markdown(
            '<div class="section-head" style="margin-top:20px">'
            '<p class="section-heading">۰۲ ـ فشار خون</p>'
            '<p class="section-sub">مقادیر سیستولیک و دیاستولیک</p>'
            "</div>",
            unsafe_allow_html=True,
        )

        ap_hi = st.number_input(
            "فشار خون سیستولیک (بالا)", min_value=60, max_value=250, value=120
        )
        ap_lo = st.number_input(
            "فشار خون دیاستولیک (پایین)", min_value=40, max_value=200, value=80
        )

    with right:
        st.markdown(
            '<div class="section-head">'
            '<p class="section-heading">۰۳ ـ نتایج آزمایش و سبک زندگی</p>'
            '<p class="section-sub">کلسترول، گلوکز و عادت‌های روزمره</p>'
            "</div>",
            unsafe_allow_html=True,
        )

        cholesterol = st.selectbox(
            "سطح کلسترول",
            [(1, "نرمال"), (2, "بالاتر از نرمال"), (3, "خیلی بالاتر از نرمال")],
            format_func=lambda x: x[1],
        )
        gluc = st.selectbox(
            "سطح گلوکز",
            [(1, "نرمال"), (2, "بالاتر از نرمال"), (3, "خیلی بالاتر از نرمال")],
            format_func=lambda x: x[1],
        )
        smoke = st.selectbox(
            "سیگار می‌کشی؟",
            [(0, "خیر"), (1, "بله")],
            format_func=lambda x: x[1],
        )
        alco = st.selectbox(
            "مصرف الکل داری؟",
            [(0, "خیر"), (1, "بله")],
            format_func=lambda x: x[1],
        )
        active = st.selectbox(
            "فعالیت بدنی منظم داری؟",
            [(1, "بله"), (0, "خیر")],
            format_func=lambda x: x[1],
        )

    st.write("")
    submitted = st.form_submit_button("تحلیل اطلاعات و اجرای مدل")


# ── پیش‌بینی ─────────────────────────────────────────────
if submitted:
    row = pd.DataFrame([{
        "age": age,
        "gender": gender[0],
        "height": height,
        "weight": weight,
        "ap_hi": ap_hi,
        "ap_lo": ap_lo,
        "cholesterol": cholesterol[0],
        "gluc": gluc[0],
        "smoke": smoke[0],
        "alco": alco[0],
        "active": active[0],
    }])

    try:
        prediction = int(model.predict(row)[0])
        classes = list(model.classes_)
        score = None

        if hasattr(model, "predict_proba") and 1 in classes:
            proba = model.predict_proba(row)[0]
            score = float(proba[classes.index(1)])

        st.markdown("---")
        st.markdown("## گزارش تحلیل مدل")

        if score is not None:
            st.markdown(
                f'<div class="result-card">'
                f'<div class="result-title">نتیجه پردازش آماده است</div>'
                f'<div class="result-score">امتیاز مدل برای کلاس دارای برچسب بیماری: '
                f"<b>{score:.1%}</b></div>"
                f"</div>",
                unsafe_allow_html=True,
            )
            st.progress(score)

        if prediction == 1:
            st.warning(
                "خروجی مدل: این ورودی در گروه دارای برچسب بیماری "
                "در مجموعه داده قرار گرفته است."
            )
        else:
            st.success(
                "خروجی مدل: این ورودی در گروه بدون برچسب بیماری "
                "در مجموعه داده قرار گرفته است."
            )

        st.caption(
            "این نتیجه صرفاً خروجی یک مدل آماری بر اساس داده‌های ورودی است. "
            "امتیاز مدل احتمال قطعی ابتلا یا تشخیص بالینی محسوب نمی‌شود."
        )

        with st.expander("مشاهده اطلاعات ارسال‌شده به مدل"):
            st.dataframe(row, use_container_width=True)

    except Exception as exc:
        st.error(f"اجرای پیش‌بینی با خطا مواجه شد: {exc}")


# ── پابرگ ─────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    '<div style="direction:rtl;text-align:center;color:#6a8fa8;'
    'font-size:12px;line-height:2;font-family:\'Vazirmatn\',sans-serif;">'
    "سامانه تحلیل سلامت قلب و عروق · پروژه آموزشی یادگیری ماشین<br>"
    "تصمیم‌گیری درمانی باید توسط متخصص سلامت انجام شود."
    "</div>",
    unsafe_allow_html=True,
)
