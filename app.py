"""
=====================================================
Livin Emotion Analysis
Main App
=====================================================
"""

import streamlit as st
from PIL import Image
from config import *

st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# LOAD CSS
# ============================================

with open(CSS_FILE, encoding="utf-8") as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )

# ============================================
# SIDEBAR
# ============================================

st.sidebar.image(LOGO, width=180)

st.sidebar.title(APP_TITLE)

st.sidebar.markdown("---")

st.sidebar.success(
"""
✅ Fine-Tuned IndoBERT

✅ Customer Segmentation

✅ Customer Retention
"""
)

# ============================================
# HOME
# ============================================

st.title("📊 Livin Emotion Analysis")

st.markdown("---")

st.markdown(
"""
Aplikasi ini digunakan untuk menganalisis emosi
ulasan Google Play menggunakan **Fine-Tuned IndoBERT**.

Pipeline:

1. Upload Dataset
2. Data Understanding
3. Preprocessing
4. Emotion Prediction
5. Emotion Probability
6. Customer Segmentation
7. Customer Retention
8. Dashboard
"""
)

st.info(
"Silakan pilih menu pada sidebar."
)
