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
# DISPLAY COLUMN
# =====================================================

# Tentukan kolom review
if "review" in probability_df.columns:

    text_column = "review"

elif "content" in probability_df.columns:

    text_column = "content"

else:

    text_column = probability_df.columns[0]

# Kolom probabilitas yang tersedia
emotion_columns = [

    col

    for col in [

        "Senang",

        "Netral",

        "Marah",

        "Frustrasi"

    ]

    if col in probability_df.columns

]

display_columns = [

    text_column,

    "emotion",

    "confidence",

    *emotion_columns

]

st.subheader("Emotion Probability")

st.dataframe(

    probability_df[display_columns],

    use_container_width=True,

    height=500,

    hide_index=True

)

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
