"""
=========================================================
UPLOAD DATASET
=========================================================
"""

import streamlit as st
import pandas as pd

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Upload Dataset",
    page_icon="📂",
    layout="wide"
)

st.title("📂 Upload Dataset")

st.markdown("---")

st.write("""
Silakan upload dataset hasil scraping Google Play
dalam format CSV (.csv) atau Excel (.xlsx).
""")

# ==========================================================
# INITIAL SESSION
# ==========================================================

if "raw_df" not in st.session_state:
    st.session_state["raw_df"] = None

# ==========================================================
# READ DATASET
# ==========================================================

def read_dataset(uploaded_file):

    if uploaded_file.name.lower().endswith(".xlsx"):
        return pd.read_excel(uploaded_file)

    read_options = [

        {"sep": ",", "encoding": "utf-8"},

        {"sep": ";", "encoding": "utf-8"},

        {"sep": ",", "encoding": "latin1"},

        {"sep": ";", "encoding": "latin1"},

        {"sep": None, "engine": "python"}

    ]

    for option in read_options:

        uploaded_file.seek(0)

        try:

            return pd.read_csv(uploaded_file, **option)

        except Exception:

            continue

    raise ValueError(
        "File CSV tidak dapat dibaca."
    )

# ==========================================================
# FILE UPLOADER
# ==========================================================

uploaded_file = st.file_uploader(
    "Upload Dataset",
    type=["csv", "xlsx"]
)

# ==========================================================
# LOAD DATASET
# ==========================================================

if uploaded_file is not None:

    try:

        df = read_dataset(uploaded_file)

        # ===============================
        # SAVE SESSION
        # ===============================

        st.session_state["raw_df"] = df

        st.success("✅ Dataset berhasil diupload.")

    except Exception as e:

        st.error(f"Gagal membaca dataset : {e}")

        st.stop()

# ==========================================================
# DISPLAY DATA
# ==========================================================

df = st.session_state.get("raw_df")

if df is not None and isinstance(df, pd.DataFrame):

    st.markdown("---")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Jumlah Review",
        len(df)
    )

    col2.metric(
        "Jumlah Kolom",
        len(df.columns)
    )

    col3.metric(
        "Missing Value",
        int(df.isnull().sum().sum())
    )

    col4.metric(
        "Duplicate",
        int(df.duplicated().sum())
    )

    st.markdown("---")

    st.subheader("Preview Dataset")

    st.dataframe(
        df,
        use_container_width=True,
        height=450
    )

    st.markdown("---")

    st.subheader("Informasi Dataset")

    info = pd.DataFrame({

        "Column": df.columns,

        "Data Type": df.dtypes.astype(str),

        "Missing": df.isnull().sum().values

    })

    st.dataframe(
        info,
        use_container_width=True
    )

    st.markdown("---")

    csv = df.to_csv(
        index=False
    ).encode("utf-8-sig")

    st.download_button(

        "⬇ Download Dataset",

        csv,

        file_name="uploaded_dataset.csv",

        mime="text/csv"

    )

else:

    st.info("📂 Silakan upload dataset terlebih dahulu.")
