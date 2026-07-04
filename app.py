"""
=========================================================
LIVIN EMOTION ANALYSIS
=========================================================
Main Application
=========================================================
"""

import streamlit as st
from pathlib import Path

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
    with open(CSS_FILE, encoding="utf-8") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )

# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:

    if LOGO.exists():
        st.image(str(LOGO), use_container_width=True)

    st.title("Livin Emotion Analysis")

    st.markdown("---")

    st.success("Version 1.0")

    st.markdown(
        """
### Workflow

1. 📥 Upload Dataset
2. 📊 Data Understanding
3. 🧹 Preprocessing
4. 🤖 Emotion Prediction
5. 📈 Emotion Probability
6. 👥 Customer Segmentation
7. 💡 Customer Retention
8. 📊 Dashboard
"""
    )

# =====================================================
# MAIN PAGE
# =====================================================

st.title("📊 Livin Emotion Analysis")

st.markdown(
"""
Aplikasi ini digunakan untuk melakukan analisis emosi pada ulasan
pengguna aplikasi **Livin' by Mandiri** menggunakan model
**Fine-Tuned IndoBERT**.

Tahapan analisis meliputi:

- Upload Dataset
- Data Understanding
- Text Preprocessing
- Emotion Prediction
- Emotion Probability
- Customer Segmentation
- Customer Retention
- Dashboard Analytics
"""
)

st.markdown("---")

# =====================================================
# INFORMATION
# =====================================================

col1, col2, col3 = st.columns(3)

col1.info(
"""
### 🤖 Model

Fine-Tuned IndoBERT
"""
)

col2.info(
"""
### 📄 Dataset

Google Play Review
"""
)

col3.info(
"""
### 🎯 Output

Emotion Analysis &
Customer Segmentation
"""
)

st.markdown("---")

st.subheader("📌 Navigation")

st.markdown(
"""
Gunakan menu pada **sidebar** untuk memulai proses analisis.

Urutan penggunaan aplikasi:

1. Upload Dataset
2. Data Understanding
3. Preprocessing
4. Emotion Prediction
5. Customer Segmentation
6. Customer Retention
7. Dashboard
"""
)

st.markdown("---")

st.caption("© 2026 Livin Emotion Analysis | Thesis Project")
