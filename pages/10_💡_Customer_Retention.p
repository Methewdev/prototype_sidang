"""
=========================================================
CUSTOMER RETENTION
=========================================================
Customer Segmentation
        ↓
Retention Strategy
=========================================================
"""

import streamlit as st
import pandas as pd
import plotly.express as px

from modules.retention import (
    retention_dataframe,
    customer_count
)

st.set_page_config(
    page_title="Customer Retention",
    page_icon="💡",
    layout="wide"
)

st.title("💡 Customer Retention Recommendation")

st.markdown("---")

# =====================================================
# CHECK SESSION
# =====================================================

if "segment_df" not in st.session_state:

    st.warning(
        "Silakan lakukan Customer Segmentation terlebih dahulu."
    )

    st.stop()

# =====================================================
# LOAD DATA
# =====================================================

segment_df = st.session_state["segment_df"].copy()

# =====================================================
# RETENTION
# =====================================================

if "retention_df" not in st.session_state:

    with st.spinner("Generating Retention Strategy..."):

        retention_df = retention_dataframe(segment_df)

        st.session_state["retention_df"] = retention_df

else:

    retention_df = st.session_state["retention_df"]

# =====================================================
# KPI
# =====================================================

summary = customer_count(retention_df)

col1,col2,col3,col4 = st.columns(4)

with col1:

    st.metric(

        "Total Customer",

        summary["Total Customer"]

    )

with col2:

    st.metric(

        "High Priority",

        summary["High Priority"]

    )

with col3:

    st.metric(

        "Medium Priority",

        summary["Medium Priority"]

    )

with col4:

    st.metric(

        "Low Priority",

        summary["Low Priority"]

    )

st.markdown("---")

# =====================================================
# PRIORITY DISTRIBUTION
# =====================================================

priority = (

    retention_df["Priority"]

    .value_counts()

    .reset_index()

)

priority.columns = [

    "Priority",

    "Total"

]

col1,col2 = st.columns(2)

with col1:

    fig = px.bar(

        priority,

        x="Priority",

        y="Total",

        color="Priority",

        text_auto=True

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )

with col2:

    fig = px.pie(

        priority,

        names="Priority",

        values="Total",

        hole=0.4

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )

# =====================================================
# SEGMENT
# =====================================================

st.markdown("---")

st.subheader("Customer Segment")

segment = (

    retention_df["Customer Segment"]

    .value_counts()

    .reset_index()

)

segment.columns = [

    "Segment",

    "Total"

]

fig = px.bar(

    segment,

    x="Segment",

    y="Total",

    color="Segment",

    text_auto=True

)

st.plotly_chart(

    fig,

    use_container_width=True

)

# =====================================================
# RETENTION TABLE
# =====================================================

st.markdown("---")

st.subheader("Retention Recommendation")

display_df = retention_df[[

    "emotion",

    "Customer Segment",

    "Priority",

    "Recommendation"

]]

st.dataframe(

    display_df,

    use_container_width=True,

    height=450

)

# =====================================================
# BUSINESS INSIGHT
# =====================================================

st.markdown("---")

st.subheader("Business Insight")

segment_selected = st.selectbox(

    "Pilih Customer Segment",

    retention_df["Customer Segment"].unique()

)

example = retention_df[

    retention_df["Customer Segment"] == segment_selected

].iloc[0]

st.success(

    f"""
**Customer Segment**

{example['Customer Segment']}

---

**Priority**

{example['Priority']}

---

**Recommendation**

{example['Recommendation']}

---

**Business Insight**

{example['Business Insight']}
"""
)

# =====================================================
# DOWNLOAD
# =====================================================

st.markdown("---")

csv = retention_df.to_csv(

    index=False

).encode("utf-8-sig")

st.download_button(

    "⬇ Download Retention Result",

    csv,

    "customer_retention.csv",

    "text/csv"

)

# =====================================================
# SAVE SESSION
# =====================================================

st.session_state["retention_df"] = retention_df

st.success("Customer Retention selesai.")

st.info("➡ Selanjutnya buka halaman Dashboard Analytics.")
