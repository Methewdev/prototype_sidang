"""
=========================================================
LIVIN EMOTION ANALYSIS
Main Application
=========================================================
"""

import streamlit as st

from config import (
    APP_TITLE,
    APP_ICON,
    LOGO,
    CSS_FILE
)

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

# =====================================================
# SIDEBAR
# =====================================================

# =====================================================
# HOME
# =====================================================

st.title("📊 Livin Emotion Analysis Dashboard")

st.markdown("---")

st.markdown(
"""
Selamat datang di **Livin Emotion Analysis Dashboard**.

Aplikasi ini digunakan untuk melakukan analisis emosi terhadap ulasan
Google Play **Livin' by Mandiri** menggunakan model
**Fine-Tuned IndoBERT**.

Seluruh proses analisis dilakukan secara bertahap mulai dari:

- 📂 Input Datase / Scrapper Dataset
- 📊 Data Understanding
- 🧹 Text Preprocessing
- 🤖 Emotion Prediction
- 📈 Emotion Probability
- 👥 Customer Segmentation
- 💡 Customer Retention
- 📊 Dashboard Analytics

Silakan pilih halaman pada **sidebar** untuk memulai proses analisis.
"""
)

st.markdown("---")

col1, col2, col3 = st.columns(3)

with col1:
    st.info(
        """
### 🤖 Model

Fine-Tuned IndoBERT
"""
    )

with col2:
    st.info(
        """
### 📄 Dataset

Google Play Review
"""
    )

with col3:
    st.info(
        """
### 🎯 Output

- Emotion Classification
- Customer Segmentation
- Customer Retention
"""
    )

st.markdown("---")

st.success(
"""
✅ Gunakan menu **Pages** pada sidebar sebelah kiri untuk berpindah antar halaman analisis.
"""
)

st.caption("© 2026 Livin Emotion Analysis")
