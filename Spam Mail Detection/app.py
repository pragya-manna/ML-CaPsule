"""
app.py  —  Spam Mail Detection | Streamlit Web App
====================================================
Place this file inside:   spam detection/
Run with:                 streamlit run app.py
"""

import streamlit as st
import pickle
import os
import string
import time

import nltk
from nltk.corpus import stopwords

# ── Download NLTK data silently on first run ────────────────────────────────
nltk.download('stopwords', quiet=True)

# ── MUST be defined here so pickle can find it when loading the model ────────
# Pickle saves a *reference* to this function by name. When loading the .pkl,
# Python looks for `message_text_process` in the current module (__main__).
# If it's missing, you get:  AttributeError: module '__main__' has no attribute
# 'message_text_process'. Defining it here fixes that.
STOPWORDS = stopwords.words('english')

def message_text_process(mess):
    """Remove punctuation and stop words — must exactly match save_model.py."""
    no_punctuation = [char for char in mess if char not in string.punctuation]
    no_punctuation = ''.join(no_punctuation)
    return [word for word in no_punctuation.split() if word.lower() not in STOPWORDS]

# ── Page configuration ───────────────────────────────────────────────────────
st.set_page_config(
    page_title="Spam Detector",
    page_icon="🛡️",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS — clean dark-card aesthetic ───────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;600&display=swap');

/* ---------- global ---------- */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}
.main {
    background: linear-gradient(135deg, #0f0f1a 0%, #1a1a2e 50%, #16213e 100%);
    min-height: 100vh;
}
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 720px;
}

/* ---------- header ---------- */
.hero-title {
    font-family: 'Space Mono', monospace;
    font-size: 2.4rem;
    font-weight: 700;
    color: #ffffff;
    line-height: 1.2;
    margin-bottom: 0.2rem;
}
.hero-subtitle {
    font-size: 1rem;
    color: #8b949e;
    margin-bottom: 2rem;
}
.shield-icon {
    font-size: 3rem;
    display: block;
    margin-bottom: 0.5rem;
}

/* ---------- card ---------- */
.card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: 2rem;
    margin-bottom: 1.5rem;
    backdrop-filter: blur(12px);
}

/* ---------- result banners ---------- */
.result-spam {
    background: linear-gradient(135deg, #ff4757, #ff3742);
    color: white;
    border-radius: 12px;
    padding: 1.5rem 2rem;
    font-family: 'Space Mono', monospace;
    font-size: 1.4rem;
    font-weight: 700;
    text-align: center;
    box-shadow: 0 8px 32px rgba(255, 71, 87, 0.35);
    animation: popIn 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
}
.result-ham {
    background: linear-gradient(135deg, #2ed573, #1fbc61);
    color: white;
    border-radius: 12px;
    padding: 1.5rem 2rem;
    font-family: 'Space Mono', monospace;
    font-size: 1.4rem;
    font-weight: 700;
    text-align: center;
    box-shadow: 0 8px 32px rgba(46, 213, 115, 0.35);
    animation: popIn 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
}
.result-detail {
    text-align: center;
    color: #8b949e;
    font-size: 0.9rem;
    margin-top: 0.75rem;
}
@keyframes popIn {
    0%   { transform: scale(0.85); opacity: 0; }
    100% { transform: scale(1);    opacity: 1; }
}

/* ---------- stats badge ---------- */
.stats-row {
    display: flex;
    gap: 1rem;
    margin-bottom: 1.5rem;
}
.stat-badge {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 10px;
    padding: 0.6rem 1rem;
    font-size: 0.82rem;
    color: #8b949e;
    flex: 1;
    text-align: center;
}
.stat-badge b {
    display: block;
    color: #e6edf3;
    font-size: 1.1rem;
    font-family: 'Space Mono', monospace;
}

/* ---------- sample chips ---------- */
.chip-label {
    font-size: 0.8rem;
    color: #8b949e;
    margin-bottom: 0.5rem;
}
</style>
""", unsafe_allow_html=True)


# ── Load model ───────────────────────────────────────────────────────────────
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'model', 'spam_model.pkl')

@st.cache_resource(show_spinner=False)
def load_model():
    if not os.path.exists(MODEL_PATH):
        return None
    with open(MODEL_PATH, 'rb') as f:
        return pickle.load(f)

model = load_model()


# ── Header ───────────────────────────────────────────────────────────────────
st.markdown('<span class="shield-icon">🛡️</span>', unsafe_allow_html=True)
st.markdown('<p class="hero-title">Spam Detector</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="hero-subtitle">Paste any SMS message below — '
    'the model will tell you if it\'s spam or legitimate in milliseconds.</p>',
    unsafe_allow_html=True,
)

# Model stats badges
st.markdown("""
<div class="stats-row">
  <div class="stat-badge"><b>MultinomialNB</b>Algorithm</div>
  <div class="stat-badge"><b>TF-IDF</b>Vectorizer</div>
  <div class="stat-badge"><b>~97%</b>Accuracy</div>
  <div class="stat-badge"><b>5,572</b>Training samples</div>
</div>
""", unsafe_allow_html=True)


# ── Model missing warning ─────────────────────────────────────────────────────
if model is None:
    st.error(
        "⚠️ **Model file not found.**\n\n"
        "Please run `python model/save_model.py` first to train and save the model, "
        "then restart the app.",
        icon="🚨",
    )
    st.stop()


# ── Input card ───────────────────────────────────────────────────────────────
st.markdown('<div class="card">', unsafe_allow_html=True)

# Sample messages as quick-fill chips
SAMPLES = {
    "🎁 Spam sample": "Congratulations! You've won a £1,000 Tesco gift card. Click here to claim your prize now!",
    "💬 Ham sample":  "Hey, are we still meeting at 6pm today? Let me know if plans changed.",
    "🚨 Spam sample 2": "WINNER!! As a valued network customer you have been selected to receivea £900 prize reward! Call 09061701461",
    "📱 Ham sample 2": "Can you pick up some groceries on the way home? We need milk and eggs.",
}

st.markdown('<p class="chip-label">Quick fill with a sample message ↓</p>', unsafe_allow_html=True)
cols = st.columns(len(SAMPLES))
selected_sample = ""
for i, (label, text) in enumerate(SAMPLES.items()):
    if cols[i].button(label, use_container_width=True):
        selected_sample = text

default_text = selected_sample if selected_sample else st.session_state.get("last_input", "")

user_input = st.text_area(
    label="SMS Message",
    value=default_text,
    height=140,
    placeholder="Type or paste an SMS message here…",
    label_visibility="collapsed",
)

if user_input:
    st.session_state["last_input"] = user_input

word_count = len(user_input.split()) if user_input.strip() else 0
char_count = len(user_input)
st.caption(f"{word_count} words · {char_count} characters")

predict_btn = st.button("🔍  Analyse Message", type="primary", use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)


# ── Prediction ───────────────────────────────────────────────────────────────
if predict_btn:
    if not user_input.strip():
        st.warning("Please enter a message before clicking Analyse.", icon="⚠️")
    else:
        with st.spinner("Analysing…"):
            time.sleep(0.4)   # tiny delay so the spinner is visible

        prediction = model.predict([user_input])[0]

        # Show result
        if prediction.lower() == "spam":
            st.markdown(
                '<div class="result-spam">🚫 &nbsp; SPAM DETECTED</div>',
                unsafe_allow_html=True,
            )
            st.markdown(
                '<p class="result-detail">This message matches patterns commonly found in spam.</p>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                '<div class="result-ham">✅ &nbsp; NOT SPAM (Ham)</div>',
                unsafe_allow_html=True,
            )
            st.markdown(
                '<p class="result-detail">This message looks legitimate.</p>',
                unsafe_allow_html=True,
            )

        # Show confidence if the model supports it
        if hasattr(model, "predict_proba"):
            proba = model.predict_proba([user_input])[0]
            classes = model.classes_
            proba_dict = dict(zip(classes, proba))

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("**Confidence scores**")

            ham_score  = proba_dict.get('ham',  proba_dict.get('Ham',  0))
            spam_score = proba_dict.get('spam', proba_dict.get('Spam', 0))

            col1, col2 = st.columns(2)
            col1.metric("✅ Ham",  f"{ham_score*100:.1f}%")
            col2.metric("🚫 Spam", f"{spam_score*100:.1f}%")


# ── Footer ───────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<center><small>Built for <b>ML-CaPsule</b> · GirlScript Summer of Code · "
    "Model: Multinomial Naïve Bayes + TF-IDF</small></center>",
    unsafe_allow_html=True,
)
