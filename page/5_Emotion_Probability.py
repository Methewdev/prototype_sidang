"""
=========================================================
EMOTION PROBABILITY
=========================================================
"""

import streamlit as st

from modules.utils import (
    require_session,
    download_csv
)

from modules.emotion_probability import (
    dataframe_probability,
    probability_summary,
    probability_heatmap,
    average_probability,
    average_probability_chart
)

st.set_page_config(
    page_title="Emotion Probability",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Emotion Probability")

st.markdown("---")

# =====================================================
# LOAD PREDICTION
# =====================================================

prediction_df = require_session(
    "prediction_df",
    "Silakan lakukan Emotion Prediction terlebih dahulu."
)

# =====================================================
# BUILD PROBABILITY
# =====================================================

probability_df = dataframe_probability(
    prediction_df
)

summary = probability_summary(
    probability_df
)

# =====================================================
# SUMMARY
# =====================================================

c1, c2 = st.columns(2)

c1.metric(
    "Average Confidence",
    f"{summary['Average Confidence']} %"
)

c2.metric(
    "Dominant Emotion",
    summary["Dominant Emotion"]
)

st.markdown("---")

# =====================================================
# AVERAGE TABLE
# =====================================================

st.subheader("Average Probability")

avg = average_probability(
    probability_df
)

st.dataframe(
    avg,
    use_container_width=True
)

st.markdown("---")

# =====================================================
# BAR
# =====================================================

st.subheader("Average Probability Chart")

st.plotly_chart(
    average_probability_chart(
        probability_df
    ),
    use_container_width=True
)

st.markdown("---")

# =====================================================
# HEATMAP
# =====================================================

st.subheader("Probability Heatmap")

st.plotly_chart(
    probability_heatmap(
        probability_df
    ),
    use_container_width=True
)

st.markdown("---")

# =====================================================
# TABLE
# =====================================================

st.subheader("Emotion Probability")

display = probability_df[

    [

        "emotion",

        "confidence",

        "Frustrasi",

        "Netral",

        "Sedih",

        "Senang"

    ]

]

st.dataframe(

    display,

    use_container_width=True,

    height=500

)

st.markdown("---")

# =====================================================
# DOWNLOAD
# =====================================================

st.download_button(

    label="⬇ Download Probability",

    data=download_csv(

        probability_df

    ),

    file_name="emotion_probability.csv",

    mime="text/csv",

    use_container_width=True

)
