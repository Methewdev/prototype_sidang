"""
=========================================================
CUSTOMER SEGMENTATION
=========================================================
"""

import streamlit as st

from modules.utils import (
    require_session,
    save_session,
    download_csv
)

from modules.clustering import (
    customer_segmentation,
    segment_summary,
    cluster_profile,
    dominant_emotion,
    segment_statistics
)

from modules.visualization import (
    segment_bar
)

st.set_page_config(
    page_title="Customer Segmentation",
    page_icon="👥",
    layout="wide"
)

st.title("👥 Customer Segmentation")

st.markdown("---")
