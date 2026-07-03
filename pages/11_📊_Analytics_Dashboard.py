"""
=========================================================
ANALYTICS DASHBOARD
=========================================================
Final Dashboard
=========================================================
"""

import streamlit as st
import plotly.express as px

from modules.dashboard import (
    dashboard_kpi,
    emotion_summary,
    segment_summary,
    priority_summary,
    review_statistics,
    top_word,
    download_dataset
)

from modules.visualization import (
    emotion_pie,
    emotion_bar,
    segment_bar,
    priority_bar,
    confidence_histogram,
    probability_heatmap,
    create_wordcloud
)

st.set_page_config(
    page_title="Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Analytics Dashboard")

st.markdown("---")

# =====================================================
# CHECK SESSION
# =====================================================

if "retention_df" not in st.session_state:

    st.warning(
        "Silakan selesaikan seluruh proses analisis terlebih dahulu."
    )

    st.stop()

df = st.session_state["retention_df"]

# =====================================================
# KPI
# =====================================================

kpi = dashboard_kpi(df)

col1, col2, col3, col4 = st.columns(4)

col1.metric("📄 Total Review", kpi["Total Review"])
col2.metric("😊 Dominant Emotion", kpi["Dominant Emotion"])
col3.metric("👥 Dominant Segment", kpi["Dominant Segment"])
col4.metric("🎯 Avg Confidence", f"{kpi['Average Confidence']:.2f}%")

st.markdown("---")

# =====================================================
# EMOTION
# =====================================================

st.subheader("😊 Emotion Distribution")

c1, c2 = st.columns(2)

with c1:
    st.plotly_chart(
        emotion_pie(df),
        use_container_width=True
    )

with c2:
    st.plotly_chart(
        emotion_bar(df),
        use_container_width=True
    )

# =====================================================
# SEGMENT
# =====================================================

st.markdown("---")

st.subheader("👥 Customer Segment")

c1, c2 = st.columns(2)

with c1:

    st.plotly_chart(

        segment_bar(df),

        use_container_width=True

    )

with c2:

    st.plotly_chart(

        priority_bar(df),

        use_container_width=True

    )

# =====================================================
# CONFIDENCE
# =====================================================

st.markdown("---")

st.subheader("🎯 Confidence Distribution")

st.plotly_chart(

    confidence_histogram(df),

    use_container_width=True

)

# =====================================================
# HEATMAP
# =====================================================

st.markdown("---")

st.subheader("🔥 Emotion Probability Heatmap")

st.plotly_chart(

    probability_heatmap(df),

    use_container_width=True

)

# =====================================================
# WORD CLOUD
# =====================================================

st.markdown("---")

st.subheader("☁ WordCloud")

st.pyplot(

    create_wordcloud(df)

)

# =====================================================
# REVIEW STATISTICS
# =====================================================

st.markdown("---")

st.subheader("📈 Review Statistics")

stats = review_statistics(df)

col1, col2, col3 = st.columns(3)

col1.metric(
    "Average Length",
    stats["Average Review Length"]
)

col2.metric(
    "Maximum Length",
    stats["Maximum Review Length"]
)

col3.metric(
    "Minimum Length",
    stats["Minimum Review Length"]
)

# =====================================================
# TOP WORD
# =====================================================

st.markdown("---")

st.subheader("🔤 Top 10 Frequent Words")

word = top_word(df)

fig = px.bar(

    word,

    x="Word",

    y="Frequency",

    text_auto=True,

    color="Frequency"

)

st.plotly_chart(

    fig,

    use_container_width=True

)

# =====================================================
# SUMMARY TABLE
# =====================================================

st.markdown("---")

st.subheader("📋 Summary")

c1, c2, c3 = st.columns(3)

with c1:

    st.dataframe(

        emotion_summary(df),

        use_container_width=True

    )

with c2:

    st.dataframe(

        segment_summary(df),

        use_container_width=True

    )

with c3:

    st.dataframe(

        priority_summary(df),

        use_container_width=True

    )

# =====================================================
# PREVIEW
# =====================================================

st.markdown("---")

st.subheader("📄 Final Dataset")

st.dataframe(

    df.head(50),

    use_container_width=True,

    height=500

)

# =====================================================
# DOWNLOAD
# =====================================================

st.markdown("---")

st.download_button(

    "⬇ Download Final Result",

    download_dataset(df),

    "final_result.csv",

    "text/csv"

)

st.success("Dashboard selesai dibuat.")
