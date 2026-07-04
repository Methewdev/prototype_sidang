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
prediction_df = require_session(
    "prediction_df",
    "Silakan lakukan Emotion Prediction terlebih dahulu."
)
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
    if "segmentation_df" not in st.session_state:

    st.info(
        "Klik tombol Jalankan Customer Segmentation."
    )

    st.stop()

segmentation_df = st.session_state["segmentation_df"]
stat = segment_statistics(
    segmentation_df
)

c1,c2,c3 = st.columns(3)

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
st.markdown("---")

st.subheader("Segment Distribution")

st.plotly_chart(

    segment_bar(

        segmentation_df

    ),

    use_container_width=True

)
st.markdown("---")

st.subheader("Segment Summary")

summary = segment_summary(
    segmentation_df
)

st.dataframe(

    summary,

    use_container_width=True

)
st.markdown("---")

st.subheader("Cluster Profile")

profile = cluster_profile(
    segmentation_df
)

st.dataframe(

    profile,

    use_container_width=True

)
st.markdown("---")

st.subheader("Dominant Emotion")

emotion = dominant_emotion(
    segmentation_df
)

emotion_df = (
    pd.DataFrame.from_dict(
        emotion,
        orient="index",
        columns=["Dominant Emotion"]
    )
    .reset_index()
)

emotion_df.columns = [
    "Customer Segment",
    "Dominant Emotion"
]

st.dataframe(
    emotion_df,
    use_container_width=True
)
st.markdown("---")

st.subheader("Segmentation Result")

st.dataframe(

    segmentation_df[
        [
            "content",
            "emotion",
            "Customer Segment"
        ]
    ],

    use_container_width=True,

    height=450

)
st.markdown("---")

st.download_button(

    "⬇ Download Segmentation",

    download_csv(

        segmentation_df

    ),

    "customer_segmentation.csv",

    "text/csv"

)
