"""
=========================================================
DASHBOARD
=========================================================
"""

import streamlit as st
import pandas as pd

from modules.utils import (
    require_session,
    download_csv
)

from modules.visualization import (
    emotion_bar,
    emotion_pie,
    confidence_histogram,
    segment_bar,
    probability_heatmap
)
st.set_page_config(
    page_title="Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Dashboard")

st.markdown("---")

retention_df = require_session(
    "retention_df",
    "Silakan lakukan seluruh proses analisis terlebih dahulu."
)
c1,c2,c3,c4 = st.columns(4)

c1.metric(
    "Total Review",
    len(retention_df)
)

c2.metric(
    "Dominant Emotion",
    retention_df["emotion"].mode()[0]
)

c3.metric(
    "Dominant Segment",
    retention_df["Customer Segment"].mode()[0]
)

c4.metric(
    "Average Confidence",
    f"{retention_df['confidence'].mean()*100:.2f}%"
)
st.markdown("---")

left,right = st.columns(2)

with left:

    st.subheader("Emotion Distribution")

    st.plotly_chart(

        emotion_bar(

            retention_df

        ),

        use_container_width=True

    )

with right:

    st.subheader("Emotion Pie Chart")

    st.plotly_chart(

        emotion_pie(

            retention_df

        ),

        use_container_width=True

    )
  st.markdown("---")

left,right = st.columns(2)

with left:

    st.subheader("Customer Segment")

    st.plotly_chart(

        segment_bar(

            retention_df

        ),

        use_container_width=True

    )

with right:

    st.subheader("Confidence Histogram")

    st.plotly_chart(

        confidence_histogram(

            retention_df

        ),

        use_container_width=True

    )
  st.markdown("---")

st.subheader("Emotion Probability Heatmap")

st.plotly_chart(

    probability_heatmap(

        retention_df

    ),

    use_container_width=True

)
st.markdown("---")

st.subheader("Risk Level")

risk = (

    retention_df["Risk Level"]

    .value_counts()

    .reset_index()

)

risk.columns=[

    "Risk",

    "Total"

]

st.dataframe(

    risk,

    use_container_width=True

)
st.markdown("---")

st.subheader("Customer Type")

customer = (

    retention_df["Customer Type"]

    .value_counts()

    .reset_index()

)

customer.columns=[

    "Customer Type",

    "Total"

]

st.dataframe(

    customer,

    use_container_width=True

)
st.markdown("---")

st.subheader("Retention Recommendation")

recommendation = (

    retention_df[

        [

            "Customer Type",

            "Risk Level",

            "Retention Strategy"

        ]

    ]

    .drop_duplicates()

)

st.dataframe(

    recommendation,

    use_container_width=True

)
st.markdown("---")

st.subheader("Final Dataset")

display_columns = [
    col for col in [
        "content",
        "emotion",
        "confidence",
        "Customer Segment",
        "Customer Type",
        "Risk Level",
        "Retention Strategy"
    ]
    if col in retention_df.columns
]

st.dataframe(
    retention_df[display_columns],
    use_container_width=True,
    height=500
)
st.markdown("---")

st.download_button(

    label="⬇ Download Final Result",

    data=download_csv(

        retention_df

    ),

    file_name="dashboard_result.csv",

    mime="text/csv",

    use_container_width=True

)
