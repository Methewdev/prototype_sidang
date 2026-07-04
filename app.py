"""
=====================================================
Livin Emotion Analysis
Main App
=====================================================
"""

import streamlit as st
from PIL import Image
from pathlib import Path

from config import *

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# LOAD CSS
# =====================================================

if CSS_FILE.exists():

    with open(CSS_FILE, "r", encoding="utf-8") as f:

        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )

else:

    st.warning(f"CSS tidak ditemukan: {CSS_FILE}")

# =====================================================
# SIDEBAR
# =====================================================

if LOGO.exists():

    try:

        logo = Image.open(LOGO)

        st.sidebar.image(
            logo,
            width=180
        )

    except Exception as e:

        st.sidebar.warning(f"Logo tidak dapat dibuka: {e}")

else:

    st.sidebar.warning("Logo tidak ditemukan.")

st.sidebar.title(APP_TITLE)

st.sidebar.markdown("---")

st.sidebar.success(
"""
✅ Fine-Tuned IndoBERT

✅ Customer Segmentation

✅ Customer Retention
"""
)

# =====================================================
# HOME
# =====================================================

st.title("📊 Livin Emotion Analysis")

st.markdown("---")

st.markdown(
"""
Selamat datang di **Livin Emotion Analysis Dashboard**.

Aplikasi ini digunakan untuk menganalisis emosi ulasan Google Play menggunakan
model **Fine-Tuned IndoBERT** sebagai dasar penyusunan **Customer Segmentation**
dan **Customer Retention Recommendation**.

### Pipeline Analisis

1. 📂 Upload Dataset
2. 📊 Data Understanding
3. 🧹 Preprocessing
4. 🤖 Emotion Prediction
5. 📈 Emotion Probability
6. 👥 Customer Segmentation
7. 💡 Customer Retention
8. 📊 Dashboard Analytics
"""
)

st.info("Silakan pilih menu pada sidebar.")
