
import streamlit as st
import pandas as pd
import joblib

# -------------------- تنظیمات صفحه --------------------
st.set_page_config(
    page_title="سامانه تحلیل سلامت قلب",
    page_icon="❤️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -------------------- طراحی ظاهری و راست‌چین --------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@400;500;600;700;800&display=swap');

:root {
    --bg: #071321;
    --panel: #101f30;
    --panel2: #14283a;
    --cyan: #39e0d0;
    --text: #edf7ff;
    --muted: #9db1c5;
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
    text-align: right;
}

.stApp {
    background:
        radial-gradient(ellipse at 10% 0%, #123247 0%, transparent 38%),
        linear-gradient(135deg, #071321, #0a1828 60%, #071321);
    color: var(--text);
}

.block-container {
    max-width: 1180px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

header[data-testid="stHeader"] {
    background: transparent;
}

h1, h2, h3, p, label {
    color: var(--text);
    text-align: right;
}

[data-testid="stMarkdownContainer"] p,
[data-testid="stCaptionContainer"],
[data-testid="stWidgetLabel"] {
    text-align: right;
}

.hero {
    background: linear-gradient(120deg, #132c40, #102237 65%, #123b47);
    border: 1px solid #285066;
    border-radius: 24px;
    padding: 30px;
    margin-bottom: 24px;
    text-align: right;
    direction: rtl;
}

.hero-tag {
    color: var(--cyan);
    font-size: 14px;
    font-weight: 700;
}

.hero-title {
    font-size: 32px;
    font-weight: 800;
    margin: 10px 0;
    color: #f3fbff;
}

.hero-desc {
    color: #b7cbdc;
    font-size: 15px;
    line-height: 2;
}

.hero-icon {
    font-size: 62px;
    text-align: center;
    padding: 8px;
    color: var(--cyan);
}

.section-card {
    background: linear-gradient(145deg, #122438, #0d1c2c);
    border: 1px solid #233e52;
    border-radius: 18px;
    padding: 20px 22px 10px 22px;
    margin-bottom: 16px;
    direction: rtl;
    text-align: right;
}

.section-heading {
    color: var(--cyan);
    font-size: 18px;
    font-weight: 700;
    margin-bottom: 4px;
}

.section-sub {
    color: var(--muted);
    font-size: 12px;
    margin-bottom: 18px;
}

div[data-baseweb="input"] > div,
div[data-baseweb="select"] > div,
div[data-baseweb="textarea"] > div {
    background: #0a1928 !important;
    border: 1px solid #29455a !important;
    border-radius: 10px !important;
    color: white !important;
}

input, textarea {
    color: white !important;
    font-family: 'Vazirmatn', sans-serif !important;
    direction: rtl !important;
    text-align: right !important;
}

div[data-baseweb="select"] span {
    color: #eaf5ff !important;
    font-family: 'Vazirmatn', sans-serif !important;
}

div[data-baseweb="popover"],
div[data-baseweb="menu"],
ul[role="listbox"] {
    direction: rtl !important;
    text-align: right !important;
    font-family: 'Vazirmatn', sans-serif !important;
}

li[role="option"] {
    direction: rtl !important;
    text-align: right !important;
    font-family: 'Vazirmatn', sans-serif !important;
}

[data-testid="stNumberInput"] button {
    background: #19374a !important;
    color: var(--cyan) !important;
    border: none !important;
}

div.stButton > button,
div[data-testid="stFormSubmitButton"] > button {
    background: linear-gradient(90deg, #23bdb4, #39e0d0) !important;
    color: #06202a !important;
    border: none !important;
    border-radius: 12px !important;
    font-family: 'Vazirmatn', sans-serif !important;
    font-size: 16px !important;
    font-weight: 800 !important;
    padding: 13px 22px !important;
    min-height: 50px;
    width: 100%;
    transition: 0.2s ease;
}

div.stButton > button:hover,
div[data-testid="stFormSubmitButton"] > button:hover {
    filter: brightness(1.08);
    transform: translateY(-1px);
}

.metric-card {
    background: #102438;
    border: 1px solid #25475a;
    border-radius: 15px;
    padding: 18px;
    text-align: center;
    min-height: 105px;
}

.metric-label {
    color: #9db5c8;
    font-size: 13px;
    margin-bottom: 8px;
}

.metric-value {
    color: var(--cyan);
    font-size: 23px;
    font-weight: 800;
}

.result-card {
    background: linear-gradient(135deg, #112d3e, #102437);
    border: 1px solid #2a6471;
    border-radius: 20px;
    padding: 24px;
    margin-top: 18px;
    direction: rtl;
    text-align: right;
}

.result-title {
    color: #eafaff;
    font-size: 22px;
    font-weight: 800;
}

.result-text {
    color: #bdd1df;
    line-height: 2;
    font-size: 14px;
}

div[data-testid="stAlert"] {
    border-radius: 12px;
    direction: rtl;
    text-align: right;
}

div[data-testid="stProgress"] {
    direction: rtl;
}

hr {
    border-color: #233e52;
}

footer, #MainMenu {
    visibility: hidden;
}

.stDataFrame {
    direction: rtl;
}

@media (max-width: 700px) {
    .hero-title {
        font-size: 24px;
    }

    .hero {
        padding: 20px;
    }
}
</style>
""", unsafe_allow_html=True)


# -------------------- بارگذاری مدل --------------------
@st.cache_resource
def load_model():
    return joblib.load("heart_model.joblib")


try:
    model = load_model()
except Exception:
    st.error(
        "مدل بارگذاری نشد. مطمئن شو فایل "
        "heart_model.joblib کنار فایل app.py قرار دارد."
    )
    st.stop()


# -------------------- سربرگ --------------------
st.markdown("""
<div class="hero">
    <div class="hero-tag">سامانه هوشمند پایش سلامت</div>
    <div class="hero-title">سامانه تحلیل سلامت قلب</div>
    <div class="hero-desc">
        اطلاعات مربوط به سلامت را وارد کن تا مدل یادگیری ماشین،
        داده‌ها را بر اساس الگوهای موجود در مجموعه داده تحلیل کند.
    </div>
    <div class="hero-icon">♡</div>
</div>
""", unsafe_allow_html=True)


# -------------------- خلاصه‌های نمایشی --------------------
c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-label">نوع سامانه</div>
        <div class="metric-value">هوش مصنوعی</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-label">حوزه تحلیل</div>
        <div class="metric-value">سلامت قلب</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-label">وضعیت خروجی</div>
        <div class="metric-value">آزمایشی</div>
    </div>
    """, unsafe_allow_html=True)

st.write("")

st.info(
    "توجه: این پروژه آموزشی است و نتیجه آن تشخیص پزشکی نیست. "
    "برای ارزیابی وضعیت سلامت، با پزشک مشورت کن."
)

st.markdown("## ثبت اطلاعات")
st.caption("فیلدها را بر اساس اطلاعات معتبر تکمیل کن.")


# -------------------- فرم ورود اطلاعات --------------------
with st.form("cardio_form"):

    left, right = st.columns(2, gap="large")

    with left:
        st.markdown("""
        <div class="section-card">
            <div class="section-heading">۰۱ ـ مشخصات و علائم حیاتی</div>
            <div class="section-sub">اطلاعات پایه و اندازه‌گیری‌های اولیه</div>
        </div>
        """, unsafe_allow_html=True)

        age = st.number_input(
            "سن (سال)", 1, 120, 45
        )

        sex = st.selectbox(
            "جنسیت",
            [(1, "مرد"), (0, "زن")],
            format_func=lambda x: x[1]
        )

        trestbps = st.number_input(
            "فشار خون در حالت استراحت (میلی‌متر جیوه)",
            50, 250, 120
        )

        thalach = st.number_input(
            "حداکثر ضربان قلب ثبت‌شده",
            50, 250, 150
        )

        exang = st.selectbox(
            "بروز درد قلبی هنگام فعالیت ورزشی",
            [(0, "خیر"), (1, "بله")],
            format_func=lambda x: x[1]
        )

        st.markdown("""
        <div class="section-card">
            <div class="section-heading">۰۲ ـ درد قفسه سینه</div>
            <div class="section-sub">انتخاب نوع درد بر اساس کدهای مجموعه داده</div>
        </div>
        """, unsafe_allow_html=True)

        cp = st.selectbox(
            "نوع درد قفسه سینه",
            [
                (1, "نوع اول"),
                (2, "نوع دوم"),
                (3, "نوع سوم"),
                (4, "نوع چهارم")
            ],
            format_func=lambda x: x[1]
        )

    with right:
        st.markdown("""
        <div class="section-card">
            <div class="section-heading">۰۳ ـ نتایج آزمایش</div>
            <div class="section-sub">مقادیر آزمایشگاهی ثبت‌شده</div>
        </div>
        """, unsafe_allow_html=True)

        chol = st.number_input(
            "کلسترول (میلی‌گرم بر دسی‌لیتر)",
            50, 700, 200
        )

        fbs = st.selectbox(
            "آیا قند خون ناشتا بیشتر از ۱۲۰ است؟",
            [(0, "خیر"), (1, "بله")],
            format_func=lambda x: x[1]
        )

        restecg = st.selectbox(
            "نتیجه نوار قلب در حالت استراحت",
            [
                (0, "نوع صفر"),
                (1, "نوع اول"),
                (2, "نوع دوم")
            ],
            format_func=lambda x: x[1]
        )

        oldpeak = st.number_input(
            "میزان افت بخش اس‌تی در نوار قلب",
            min_value=0.0,
            max_value=10.0,
            value=1.0,
            step=0.1
        )

        slope = st.selectbox(
            "شیب بخش اس‌تی در نوار قلب",
            [
                (1, "نوع اول"),
                (2, "نوع دوم"),
                (3, "نوع سوم")
            ],
            format_func=lambda x: x[1]
        )

        ca = st.selectbox(
            "تعداد رگ‌های اصلی مشاهده‌شده",
            [0, 1, 2, 3]
        )

        thal = st.selectbox(
            "کد نتیجه آزمایش تالاسمی",
            [
                (3, "کد ۳"),
                (6, "کد ۶"),
                (7, "کد ۷")
            ],
            format_func=lambda x: x[1]
        )

    st.write("")

    submitted = st.form_submit_button(
        "تحلیل اطلاعات و اجرای مدل"
    )


# -------------------- اجرای پیش‌بینی --------------------
if submitted:

    row = pd.DataFrame([{
        "age": age,
        "sex": sex[0],
        "cp": cp[0],
        "trestbps": trestbps,
        "chol": chol,
        "fbs": fbs[0],
        "restecg": restecg[0],
        "thalach": thalach,
        "exang": exang[0],
        "oldpeak": oldpeak,
        "slope": slope[0],
        "ca": ca,
        "thal": thal[0]
    }])

    try:
        prediction = int(model.predict(row)[0])

        st.markdown("---")
        st.markdown("## گزارش تحلیل مدل")

        if hasattr(model, "predict_proba"):
            probabilities = model.predict_proba(row)[0]

            # یافتن احتمال کلاس ۱ در صورت مشخص بودن ترتیب کلاس‌ها
            classes = list(model.classes_)
            if 1 in classes:
                score = float(probabilities[classes.index(1)])
            else:
                score = None

            if score is not None:
                st.markdown(f"""
                <div class="result-card">
                    <div class="result-title">نتیجه پردازش آماده است</div>
                    <div class="result-text">
                        امتیاز مدل برای کلاس دارای برچسب بیماری:
                        <b>{score:.1%}</b>
                    </div>
                </div>
                """, unsafe_allow_html=True)

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
            "این نتیجه صرفاً خروجی یک مدل آماری بر اساس داده‌های "
            "ورودی است. امتیاز مدل، احتمال قطعی ابتلا یا تشخیص "
            "بالینی محسوب نمی‌شود."
        )

        with st.expander("مشاهده اطلاعات ارسال‌شده به مدل"):
            st.dataframe(row, use_container_width=True)

    except Exception as e:
        st.error(
            f"اجرای پیش‌بینی با خطا مواجه شد: {e}"
        )


# -------------------- پابرگ --------------------
st.markdown("---")

st.markdown("""
<div style="
    direction:rtl;
    text-align:center;
    color:#8fa9bd;
    font-size:12px;
    line-height:2;
    font-family:'Vazirmatn',sans-serif;
">
    سامانه تحلیل سلامت قلب · پروژه آموزشی یادگیری ماشین
    <br>
    تصمیم‌گیری درمانی باید توسط متخصص سلامت انجام شود.
</div>
""", unsafe_allow_html=True)
