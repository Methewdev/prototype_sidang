"""
=========================================================
CUSTOMER RETENTION
=========================================================
"""

import streamlit as st

from modules.utils import (
    require_session,
    save_session,
    download_csv
)

from modules.retention import (
    customer_retention,
    retention_summary,
    retention_statistics
)

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Customer Retention",
    page_icon="💡",
    layout="wide"
)

st.title("💡 Customer Retention")

st.markdown("---")

# =====================================================
# LOAD SEGMENTATION
# =====================================================

segmentation_df = require_session(
    "segmentation_df",
    "Silakan lakukan Customer Segmentation terlebih dahulu."
)

# =====================================================
# GENERATE RETENTION
# =====================================================

if st.button(
    "🚀 Generate Customer Retention",
    use_container_width=True
):

    retention_df = customer_retention(
        segmentation_df
    )

    save_session(
        "retention_df",
        retention_df
    )

    st.success(
        "Customer Retention berhasil dibuat."
    )

# =====================================================
# CHECK SESSION
# =====================================================

if "retention_df" not in st.session_state:

    st.info(
        "Klik tombol **Generate Customer Retention**."
    )

    st.stop()

retention_df = st.session_state["retention_df"]

# =====================================================
# STATISTICS
# =====================================================

stat = retention_statistics(
    retention_df
)

c1, c2, c3 = st.columns(3)

c1.metric(
    "Total Customer",
    stat.get(
        "Total Customer",
        0
    )
)

c2.metric(
    "Customer Segment",
    stat.get(
        "Customer Segment",
        "-"
    )
)

c3.metric(
    "Highest Priority",
    stat.get(
        "Highest Priority",
        "-"
    )
)

st.markdown("---")

# =====================================================
# SUMMARY
# =====================================================

st.subheader(
    "Retention Summary"
)

summary = retention_summary(
    retention_df
)

st.dataframe(
    summary,
    use_container_width=True,
    hide_index=True
)

st.markdown("---")

# =====================================================
# RETENTION RECOMMENDATION
# =====================================================

# =====================================================
# RETENTION RECOMMENDATION
# =====================================================

st.subheader(
    "Retention Recommendation"
)

display_columns = [

    col

    for col in [

        "content",
        "final_text",
        "emotion",
        "Customer Segment",
        "Risk Level",
        "Priority",
        "Retention Strategy",
        "Recommended Action"

    ]

    if col in retention_df.columns

]

st.dataframe(

    retention_df[
        display_columns
    ],

    use_container_width=True,

    hide_index=True,

    height=500

)

st.markdown("---")

# =====================================================
# DOWNLOAD
# =====================================================

st.download_button(

    label="⬇ Download Customer Retention",

    data=download_csv(
        retention_df
    ),

    file_name="customer_retention.csv",

    mime="text/csv",

    use_container_width=True

)
