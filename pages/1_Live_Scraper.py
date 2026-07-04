"""
=========================================================
LIVE GOOGLE PLAY SCRAPER
=========================================================
"""

import streamlit as st
import pandas as pd

from modules.scraper import (
    APP_MAPPING,
    get_reviews,
    dataset_info,
    export_csv
)

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Live Scraper",
    page_icon="📥",
    layout="wide"
)

# =====================================================
# SESSION STATE
# =====================================================

if "raw_data" not in st.session_state:
    st.session_state.raw_data = pd.DataFrame()

# =====================================================
# TITLE
# =====================================================

st.title("📥 Live Google Play Review Scraper")
st.caption(
    "Ambil review terbaru langsung dari Google Play Store tanpa perlu upload dataset."
)

# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:

    st.header("⚙️ Scraper Settings")

    app_name = st.selectbox(
        "Pilih Aplikasi",
        list(APP_MAPPING.keys())
    )

    count = st.slider(
        "Jumlah Review",
        min_value=100,
        max_value=5000,
        value=500,
        step=100
    )

    scrape_button = st.button(
        "🚀 Ambil Review",
        use_container_width=True
    )

# =====================================================
# SCRAPING
# =====================================================

if scrape_button:

    with st.spinner("Mengambil review dari Google Play Store..."):

        try:

            df = get_reviews(
                app_name=app_name,
                count=count
            )

            if df.empty:
                st.warning("Tidak ada review yang berhasil diambil.")
                st.stop()

            st.session_state.raw_data = df
            st.session_state.app_name = app_name

            st.success(
                f"✅ Berhasil mengambil {len(df)} review."
            )

        except Exception as e:

            st.error(
                f"Gagal mengambil data.\n\n{e}"
            )

# =====================================================
# SHOW DATA
# =====================================================

if not st.session_state.raw_data.empty:

    df = st.session_state.raw_data

    st.divider()

    st.subheader("📊 Dataset Information")

    info = dataset_info(df)

    latest = "-"
    oldest = "-"

    if pd.notna(info["Latest Review"]):
        latest = info["Latest Review"].strftime("%d-%m-%Y")

    if pd.notna(info["Oldest Review"]):
        oldest = info["Oldest Review"].strftime("%d-%m-%Y")

    c1, c2, c3, c4, c5 = st.columns(5)

    c1.metric(
        "Total Review",
        info["Total Review"]
    )

    c2.metric(
        "Average Rating",
        info["Average Rating"]
    )

    c3.metric(
        "Latest Review",
        latest
    )

    c4.metric(
        "Oldest Review",
        oldest
    )

    c5.metric(
        "App Version",
        info["Total Version"]
    )

    st.divider()

    st.subheader("📄 Preview Review")

    st.dataframe(
        df,
        width="stretch",
        hide_index=True,
        height=500
    )

    filename = (
        st.session_state.app_name
        .replace(" ", "_")
        .replace("'", "")
    )

    st.download_button(
        "⬇️ Download CSV",
        data=export_csv(df),
        file_name=f"{filename}.csv",
        mime="text/csv",
        use_container_width=True
    )

else:

    st.info(
        "Silakan lakukan scraping terlebih dahulu."
    )
