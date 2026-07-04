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

with st.sidebar:

    if LOGO.exists():

        st.image(str(LOGO), width=180)

    st.title(APP_TITLE)

    st.markdown("---")

    st.success("Version 1.0")

    st.markdown("## Workflow")

    st.page_link(
        "page/1_Upload_Dataset.py",
        label="📂 Upload Dataset"
    )

    st.page_link(
        "page/2_Data_Understanding.py",
        label="📊 Data Understanding"
    )

    st.page_link(
        "page/3_Preprocessing.py",
        label="🧹 Preprocessing"
    )

    st.page_link(
        "page/4_Emotion_Prediction.py",
        label="🤖 Emotion Prediction"
    )

    st.page_link(
        "page/5_Emotion_Probability.py",
        label="📈 Emotion Probability"
    )

    st.page_link(
        "page/6_Customer_Segmentation.py",
        label="👥 Customer Segmentation"
    )

    st.page_link(
        "page/7_Customer_Retention.py",
        label="💡 Customer Retention"
    )

    st.page_link(
        "page/8_Dashboard.py",
        label="📊 Dashboard"
    )

# =====================================================
# HOME
# =====================================================

st.title("📊 Livin Emotion Analysis")

st.markdown("---")

st.markdown(
"""
Aplikasi ini digunakan untuk melakukan analisis emosi ulasan
Google Play **Livin' by Mandiri** menggunakan
**Fine-Tuned IndoBERT**.

### Tahapan Analisis

1. Upload Dataset
2. Data Understanding
3. Text Preprocessing
4. Emotion Prediction
5. Emotion Probability
6. Customer Segmentation
7. Customer Retention
8. Dashboard Analytics
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

Emotion Classification

Customer Segmentation

Customer Retention
"""
    )

st.markdown("---")

st.success(
"""
Silakan pilih menu pada sidebar untuk memulai analisis.
"""
)

st.caption("© 2026 Livin Emotion Analysis")
