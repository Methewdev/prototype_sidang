st.markdown("---")

st.download_button(

    "⬇ Download Segmentation",

    download_csv(

        segmentation_df

    ),

    "customer_segmentation.csv",

    "text/csv"

)
segmentation_df = require_session(
    "segmentation_df",
    "Silakan lakukan Customer Segmentation terlebih dahulu."
)
if st.button(
    "🚀 Generate Customer Retention",
    use_container_width=True
):

    with st.spinner("Menyusun strategi customer retention..."):

        retention_df = customer_retention(
            segmentation_df
        )

        save_session(
            "retention_df",
            retention_df
        )
if "retention_df" not in st.session_state:

    st.info(
        "Klik tombol Generate Customer Retention."
    )

    st.stop()

retention_df = st.session_state["retention_df"]
kpi = retention_kpi(retention_df)

c1,c2,c3,c4 = st.columns(4)

c1.metric(
    "Total Customer",
    kpi["Total Customer"]
)

c2.metric(
    "High Priority",
    kpi["High Priority"]
)

c3.metric(
    "Medium Priority",
    kpi["Medium Priority"]
)

c4.metric(
    "Low Priority",
    kpi["Low Priority"]
)
st.markdown("---")

st.subheader("📊 Priority Distribution")

st.plotly_chart(
    priority_bar(retention_df),
    use_container_width=True
)
st.markdown("---")

st.subheader("📋 Priority Summary")

summary = priority_summary(
    retention_df
)

st.dataframe(
    summary,
    use_container_width=True
)
st.markdown("---")

st.subheader("📈 Customer Retention Summary")

summary = retention_summary(
    retention_df
)

st.dataframe(
    summary,
    use_container_width=True
)
st.markdown("---")

st.subheader("💡 Retention Recommendation")

recommendation = retention_df[
    [
        "Customer Segment",
        "Priority",
        "Recommendation",
        "Business Insight"
    ]
].drop_duplicates()

st.dataframe(
    recommendation,
    use_container_width=True
)
st.markdown("---")

st.subheader("📄 Customer Retention Result")

st.dataframe(

    retention_df[
        [
            "content",
            "emotion",
            "Customer Segment",
            "Priority"
        ]
    ],

    use_container_width=True,

    height=450

)
st.markdown("---")

st.download_button(

    "⬇ Download Customer Retention",

    download_csv(

        retention_df

    ),

    "customer_retention.csv",

    "text/csv"

)
    st.success(
        "Customer Retention berhasil dibuat."
    )
