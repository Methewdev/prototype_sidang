"""
=========================================================
CUSTOMER SEGMENTATION
=========================================================
Emotion Probability
        ↓
KMeans
        ↓
Customer Segment
=========================================================
"""

import streamlit as st
import pandas as pd
import plotly.express as px

from modules.clustering import (
    segment_dataframe,
    segment_summary,
    segment_profile
)

st.set_page_config(
    page_title="Customer Segmentation",
    page_icon="👥",
    layout="wide"
)

st.title("👥 Customer Segmentation")

st.markdown("---")

# =====================================================
# CHECK SESSION
# =====================================================

if "probability_df" not in st.session_state:

    st.warning(
        "Silakan lakukan Emotion Probability terlebih dahulu."
    )

    st.stop()

# =====================================================
# LOAD DATA
# =====================================================

df = st.session_state["probability_df"].copy()

# =====================================================
# SEGMENTATION
# =====================================================

if "segment_df" not in st.session_state:

    with st.spinner("Melakukan Customer Segmentation ..."):

        segment_df = segment_dataframe(df)

        st.session_state["segment_df"] = segment_df

else:

    segment_df = st.session_state["segment_df"]

# =====================================================
# KPI
# =====================================================

st.subheader("Segmentation Overview")

col1,col2,col3,col4 = st.columns(4)

with col1:

    st.metric(
        "Total Review",
        len(segment_df)
    )

with col2:

    st.metric(
        "Total Cluster",
        segment_df["Cluster"].nunique()
    )

with col3:

    st.metric(
        "Dominant Segment",
        segment_df["Customer Segment"].mode()[0]
    )

with col4:

    st.metric(
        "Average Confidence",
        f"{segment_df['confidence'].mean()*100:.2f}%"
    )

st.markdown("---")

# =====================================================
# PREVIEW
# =====================================================

st.subheader("Segmentation Result")

st.dataframe(

    segment_df,

    use_container_width=True,

    height=450

)

# =====================================================
# DISTRIBUTION
# =====================================================

st.markdown("---")

st.subheader("Customer Segment Distribution")

segment_count = (

    segment_df["Customer Segment"]

    .value_counts()

    .reset_index()

)

segment_count.columns = [

    "Segment",

    "Total"

]

col1,col2 = st.columns(2)

with col1:

    fig = px.bar(

        segment_count,

        x="Segment",

        y="Total",

        color="Segment",

        text_auto=True

    )

    fig.update_layout(

        height=400

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )

with col2:

    fig = px.pie(

        segment_count,

        names="Segment",

        values="Total",

        hole=0.4

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )

# =====================================================
# PROFILE
# =====================================================

st.markdown("---")

st.subheader("Cluster Profile")

profile = segment_profile(segment_df)

st.dataframe(

    profile,

    use_container_width=True

)

# =====================================================
# EMOTION PROFILE
# =====================================================

st.markdown("---")

st.subheader("Average Emotion Probability per Segment")

profile_reset = profile.reset_index()

emotion_columns = [

    "Frustrasi",

    "Netral",

    "Sedih",

    "Senang"

]

selected_segment = st.selectbox(

    "Pilih Customer Segment",

    profile_reset["Customer Segment"]

)

selected_profile = profile_reset[

    profile_reset["Customer Segment"] == selected_segment

]

emotion_df = pd.DataFrame({

    "Emotion": emotion_columns,

    "Probability": [

        selected_profile.iloc[0]["Frustrasi"],

        selected_profile.iloc[0]["Netral"],

        selected_profile.iloc[0]["Sedih"],

        selected_profile.iloc[0]["Senang"]

    ]

})

fig = px.bar(

    emotion_df,

    x="Emotion",

    y="Probability",

    color="Emotion",

    text_auto=".2f"

)

fig.update_layout(

    height=400

)

st.plotly_chart(

    fig,

    use_container_width=True

)

# =====================================================
# SEGMENT SUMMARY
# =====================================================

st.markdown("---")

st.subheader("Segmentation Summary")

summary = segment_summary(segment_df)

st.dataframe(

    summary,

    use_container_width=True

)

# =====================================================
# DOWNLOAD
# =====================================================

st.markdown("---")

csv = segment_df.to_csv(

    index=False

).encode("utf-8-sig")

st.download_button(

    "⬇ Download Segmentation Result",

    csv,

    "customer_segmentation.csv",

    "text/csv"

)

# =====================================================
# SAVE SESSION
# =====================================================

st.session_state["segment_df"] = segment_df

st.success(

    "Customer Segmentation selesai."

)

# =====================================================
# NEXT
# =====================================================

st.info(

    "➡ Selanjutnya buka halaman Customer Retention."

)
