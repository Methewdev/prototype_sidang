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
    "Ambil review terbaru langsung dari Google Play Store "
    "tanpa perlu upload dataset."
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

    with st.spinner("Mengambil data dari Google Play Store..."):

        try:

            df = get_reviews(
                app_name=app_name,
                count=count,
                country=country,
                language=language,
                sort=sort
            )

            st.session_state.raw_data = df

            st.success(
                f"✅ {len(df)} review berhasil diambil."
            )

        except Exception as e:

            st.error(str(e))

# =====================================================
# SHOW DATA
# =====================================================

if not st.session_state.raw_data.empty:

    df = st.session_state.raw_data

    st.divider()

    st.subheader("📊 Dataset Information")

    info = dataset_info(df)

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
    info["Latest Review"].strftime("%d-%m-%Y")
        
    )

    c4.metric(
    "Oldest Review",
    info["Oldest Review"].strftime("%d-%m-%Y")
        
    )

    st.divider()

    st.subheader("📄 Preview Review")

    st.dataframe(
        df,
        width="stretch",
        hide_index=True
    )

    st.download_button(
        "⬇️ Download CSV",
        data=export_csv(df),
        file_name="google_play_reviews.csv",
        mime="text/csv",
        use_container_width=True
    )

else:

    st.info(
        "Silakan lakukan scraping terlebih dahulu."
    )
