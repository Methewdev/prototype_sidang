"""
=========================================================
FINAL DASHBOARD
=========================================================
"""

import streamlit as st

from modules.utils import (
    require_session,
    download_csv
)

from modules.visualization import (
    emotion_bar,
    emotion_pie,
    segment_bar,
    priority_bar,
    probability_heatmap,
    confidence_histogram,
    create_wordcloud,
    top_words,
    dashboard_kpi
)

st.set_page_config(
    page_title="Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Livin Emotion Analysis Dashboard")

st.markdown("---")
