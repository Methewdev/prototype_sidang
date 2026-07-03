"""
=========================================================
NORMALIZATION PAGE
=========================================================
"""

import streamlit as st
import pandas as pd

from modules.preprocessing import normalization

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(

    page_title="Normalization",

    page_icon="🔄",

    layout="wide"

)

st.title("🔄 Text Normalization")

st.markdown("---")

# ==========================================================
# CHECK SESSION
# ==========================================================

if "case_df" not in st.session_state:

    st.warning("Silakan lakukan proses Case Folding terlebih dahulu.")

    st.stop()

df = st.session_state["case_df"].copy()

# ==========================================================
# ORIGINAL DATA
# ==========================================================

st.subheader("📋 Data Sebelum Normalization")

st.dataframe(

    df[["case_folding"]].head(10),

    use_container_width=True

)

# ==========================================================
# PROCESS
# ==========================================================

with st.spinner("Melakukan Normalization..."):

    df["normalization"] = df["case_folding"].apply(normalization)

# ==========================================================
# RESULT
# ==========================================================

st.markdown("---")

st.subheader("✅ Hasil Normalization")

st.dataframe(

    df[

        [

            "case_folding",

            "normalization"

        ]

    ].head(20),

    use_container_width=True

)

# ==========================================================
# BEFORE AFTER
# ==========================================================

st.markdown("---")

st.subheader("📊 Before vs After")

compare = pd.DataFrame({

    "Case Folding":

        df["case_folding"].head(15),

    "Normalization":

        df["normalization"].head(15)

})

st.dataframe(

    compare,

    use_container_width=True

)

# ==========================================================
# CHANGED DATA
# ==========================================================

changed = (

    df["case_folding"]

    !=

    df["normalization"]

).sum()

col1,col2,col3,col4 = st.columns(4)

with col1:

    st.metric(

        "Total Review",

        len(df)

    )

with col2:

    st.metric(

        "Changed Review",

        changed

    )

with col3:

    st.metric(

        "Percentage",

        round(

            changed/len(df)*100,

            2

        )

    )

with col4:

    st.metric(

        "No Change",

        len(df)-changed

    )

# ==========================================================
# SAMPLE
# ==========================================================

st.markdown("---")

st.subheader("🔍 Contoh Normalization")

index = st.slider(

    "Pilih Review",

    0,

    len(df)-1,

    0

)

st.write("### Sebelum")

st.info(

    df.loc[index,"case_folding"]

)

st.write("### Sesudah")

st.success(

    df.loc[index,"normalization"]

)

# ==========================================================
# DOWNLOAD
# ==========================================================

st.markdown("---")

st.download_button(

    "⬇ Download Hasil Normalization",

    data=df.to_csv(index=False),

    file_name="normalization_result.csv",

    mime="text/csv"

)

# ==========================================================
# SAVE SESSION
# ==========================================================

st.session_state["normal_df"] = df

st.success("Normalization selesai.")
