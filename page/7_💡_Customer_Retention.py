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

st.set_page_config(
    page_title="Customer Retention",
    page_icon="💡",
    layout="wide"
)

st.title("💡 Customer Retention")

st.markdown("---")

segmentation_df = require_session(
    "segmentation_df",
    "Silakan lakukan Customer Segmentation terlebih dahulu."
)

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

if "retention_df" not in st.session_state:

    st.info(
        "Klik tombol Generate Customer Retention."
    )

    st.stop()

retention_df = st.session_state["retention_df"]

stat = retention_statistics(
    retention_df
)

c1, c2, c3 = st.columns(3)

c1.metric(
    "Total Customer",
    stat["Total Customer"]
)

c2.metric(
    "Customer Type",
    stat["Customer Type"]
)

c3.metric(
    "Highest Risk",
    stat["Highest Risk"]
)

st.markdown("---")

st.subheader("Retention Summary")

summary = retention_summary(
    retention_df
)

st.dataframe(
    summary,
    use_container_width=True
)

st.markdown("---")

st.subheader("Retention Recommendation")

display_columns = [
    col for col in [
        "content",
        "emotion",
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
    label="⬇ Download Customer Retention",
    data=download_csv(retention_df),
    file_name="customer_retention.csv",
    mime="text/csv",
    use_container_width=True
)
