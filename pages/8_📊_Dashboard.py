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
retention_df = require_session(
    "retention_df",
    "Silakan jalankan seluruh pipeline terlebih dahulu."
)
kpi = dashboard_kpi(retention_df)

c1,c2,c3,c4 = st.columns(4)

c1.metric(
    "Total Review",
    kpi["Total Review"]
)

c2.metric(
    "Dominant Emotion",
    kpi["Emotion"]
)

c3.metric(
    "Dominant Segment",
    kpi["Segment"]
)

c4.metric(
    "Average Confidence",
    f"{kpi['Confidence']} %"
)
st.markdown("---")

left,right = st.columns(2)

with left:

    st.subheader("Emotion Distribution")

    st.plotly_chart(

        emotion_bar(retention_df),

        use_container_width=True

    )

with right:

    st.subheader("Emotion Pie")

    st.plotly_chart(

        emotion_pie(retention_df),

        use_container_width=True

    )
    st.markdown("---")

left,right = st.columns(2)

with left:

    st.subheader("Customer Segment")

    st.plotly_chart(

        segment_bar(retention_df),

        use_container_width=True

    )

with right:

    st.subheader("Priority Distribution")

    st.plotly_chart(

        priority_bar(retention_df),

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

st.subheader("Confidence Distribution")

st.plotly_chart(

    confidence_histogram(

        retention_df

    ),

    use_container_width=True

)
st.markdown("---")

left,right = st.columns(2)

with left:

    st.subheader("WordCloud")

    st.pyplot(

        create_wordcloud(

            retention_df

        )

    )

with right:

    st.subheader("Top 20 Words")

    st.dataframe(

        top_words(

            retention_df

        ),

        use_container_width=True

    )
    st.markdown("---")

st.subheader("Customer Retention Recommendation")

recommendation = (

    retention_df[

        [

            "Customer Segment",

            "Priority",

            "Recommendation",

            "Business Insight"

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

st.dataframe(

    retention_df,

    use_container_width=True,

    height=500

)
st.markdown("---")

st.download_button(

    "⬇ Download Final Result",

    download_csv(

        retention_df

    ),

    "livin_emotion_analysis.csv",

    "text/csv"

)
