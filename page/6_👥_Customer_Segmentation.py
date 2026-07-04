"""
=========================================================
CUSTOMER SEGMENTATION
=========================================================
"""

import streamlit as st
import pandas as pd

from modules.utils import (
    require_session,
    save_session,
    download_csv
)

from modules.segmentation import (
    customer_segmentation,
    segment_summary,
    cluster_profile,
    dominant_emotion,
    segment_statistics,
    silhouette
)

from modules.visualization import (
    segment_bar
)

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Customer Segmentation",
    page_icon="👥",
    layout="wide"
)

st.title("👥 Customer Segmentation")

st.markdown("---")

# =====================================================
# LOAD PREDICTION RESULT
# =====================================================

prediction_df = require_session(
    "prediction_df",
    "Silakan lakukan Emotion Prediction terlebih dahulu."
)

# =====================================================
# RUN SEGMENTATION
# =====================================================

if st.button(
    "🚀 Jalankan Customer Segmentation",
    use_container_width=True
):

    with st.spinner("Melakukan clustering..."):

        segmentation_df = customer_segmentation(
            prediction_df
        )

        save_session(
            "segmentation_df",
            segmentation_df
        )

    st.success(
        "Customer Segmentation berhasil."
    )

# =====================================================
# CHECK SESSION
# =====================================================

if "segmentation_df" not in st.session_state:

    st.info(
        "Klik tombol **Jalankan Customer Segmentation**."
    )

    st.stop()

segmentation_df = st.session_state["segmentation_df"]

# =====================================================
# SUMMARY
# =====================================================

stat = segment_statistics(
    segmentation_df
)

score = silhouette(
    segmentation_df
)

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Total Customer",
    stat["Total Customer"]
)

c2.metric(
    "Total Segment",
    stat["Total Segment"]
)

c3.metric(
    "Dominant Segment",
    stat["Dominant Segment"]
)

c4.metric(
    "Silhouette Score",
    score
)

st.markdown("---")

# =====================================================
# SEGMENT DISTRIBUTION
# =====================================================

st.subheader("📊 Customer Segment Distribution")

st.plotly_chart(
    segment_bar(segmentation_df),
    use_container_width=True
)

st.markdown("---")

# =====================================================
# SEGMENT SUMMARY
# =====================================================

st.subheader("📋 Segment Summary")

summary = segment_summary(
    segmentation_df
)

st.dataframe(
    summary,
    use_container_width=True
)

st.markdown("---")

# =====================================================
# CLUSTER PROFILE
# =====================================================

st.subheader("📈 Cluster Profile")

profile = cluster_profile(
    segmentation_df
)

st.dataframe(
    profile,
    use_container_width=True
)

st.markdown("---")

# =====================================================
# DOMINANT EMOTION
# =====================================================

st.subheader("😊 Dominant Emotion per Segment")

emotion = dominant_emotion(
    segmentation_df
)

emotion_df = pd.DataFrame({

    "Customer Segment": emotion.index,

    "Dominant Emotion": emotion.values

})

st.dataframe(
    emotion_df,
    use_container_width=True
)

st.markdown("---")

# =====================================================
# RESULT
# =====================================================

st.subheader("📄 Segmentation Result")

display_columns = [
    col
    for col in [
        "content",
        "emotion",
        "confidence",
        "Customer Segment"
    ]
    if col in segmentation_df.columns
]

st.dataframe(
    segmentation_df[
        display_columns
    ],
    use_container_width=True,
    height=500
)

st.markdown("---")

# =====================================================
# DOWNLOAD
# =====================================================

st.download_button(
    label="⬇ Download Customer Segmentation",
    data=download_csv(segmentation_df),
    file_name="customer_segmentation.csv",
    mime="text/csv",
    use_container_width=True
)
