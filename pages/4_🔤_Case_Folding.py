"""
=========================================================
CASE FOLDING PAGE
=========================================================
"""

import streamlit as st
import pandas as pd

from modules.preprocessing import case_folding

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(

    page_title="Case Folding",

    page_icon="🔤",

    layout="wide"

)

st.title("🔤 Case Folding")

st.markdown("---")

# ==========================================================
# CHECK SESSION
# ==========================================================

if "clean_df" not in st.session_state:

    st.warning("Silakan lakukan proses Cleaning terlebih dahulu.")

    st.stop()

df = st.session_state["clean_df"].copy()

# ==========================================================
# ORIGINAL DATA
# ==========================================================

st.subheader("📋 Data Sebelum Case Folding")

st.dataframe(

    df[["cleaning"]].head(10),

    use_container_width=True

)

# ==========================================================
# PROCESS
# ==========================================================

with st.spinner("Melakukan Case Folding..."):

    df["case_folding"] = df["cleaning"].apply(case_folding)

# ==========================================================
# RESULT
# ==========================================================

st.markdown("---")

st.subheader("✅ Hasil Case Folding")

st.dataframe(

    df[
        [
            "cleaning",
            "case_folding"
        ]
    ].head(20),

    use_container_width=True

)

# ==========================================================
# BEFORE VS AFTER
# ==========================================================

st.markdown("---")

st.subheader("📊 Perbandingan")

compare = pd.DataFrame({

    "Cleaning":

        df["cleaning"].head(10),

    "Case Folding":

        df["case_folding"].head(10)

})

st.dataframe(

    compare,

    use_container_width=True

)

# ==========================================================
# CHARACTER STATISTICS
# ==========================================================

before_char = (

    df["cleaning"]

    .astype(str)

    .apply(len)

)

after_char = (

    df["case_folding"]

    .astype(str)

    .apply(len)

)

col1,col2,col3,col4 = st.columns(4)

with col1:

    st.metric(

        "Total Review",

        len(df)

    )

with col2:

    st.metric(

        "Avg Character",

        round(before_char.mean(),2)

    )

with col3:

    st.metric(

        "Avg Character After",

        round(after_char.mean(),2)

    )

with col4:

    st.metric(

        "Changed",

        (df["cleaning"] != df["case_folding"]).sum()

    )

# ==========================================================
# SAMPLE RESULT
# ==========================================================

st.markdown("---")

st.subheader("🔍 Contoh Hasil")

index = st.number_input(

    "Pilih Review",

    0,

    len(df)-1,

    0

)

st.write("### Sebelum")

st.info(

    df.loc[index,"cleaning"]

)

st.write("### Sesudah")

st.success(

    df.loc[index,"case_folding"]

)

# ==========================================================
# DOWNLOAD
# ==========================================================

st.markdown("---")

st.download_button(

    "⬇ Download Hasil Case Folding",

    data=df.to_csv(index=False),

    file_name="case_folding.csv",

    mime="text/csv"

)

# ==========================================================
# SAVE SESSION
# ==========================================================

st.session_state["case_df"] = df

st.success("Case Folding selesai.")
