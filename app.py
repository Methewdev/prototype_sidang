"""
=========================================================
LIVIN EMOTION ANALYSIS DASHBOARD
Main Application
=========================================================
"""

import streamlit as st
from PIL import Image
import os

from config import *

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(

    page_title=PAGE_TITLE,

    page_icon=PAGE_ICON,

    layout=LAYOUT,

    initial_sidebar_state=INITIAL_SIDEBAR_STATE

)

# ==========================================================
# LOAD CSS
# ==========================================================

if os.path.exists(CSS):

    with open(CSS) as f:

        st.markdown(

            f"<style>{f.read()}</style>",

            unsafe_allow_html=True

        )

# ==========================================================
# LOAD LOGO
# ==========================================================

if os.path.exists(LOGO):

    logo = Image.open(LOGO)

    st.sidebar.image(

        logo,

        use_container_width=True

    )

# ==========================================================
# SIDEBAR
# ==========================================================

st.sidebar.title("📊 Livin Emotion Analysis")

st.sidebar.markdown("---")

st.sidebar.success("System Ready")

st.sidebar.markdown("---")

st.sidebar.markdown(

"""
### Pipeline

1️⃣ Upload Dataset

2️⃣ Data Understanding

3️⃣ Cleaning

4️⃣ Case Folding

5️⃣ Normalization

6️⃣ Tokenizer

7️⃣ Emotion Prediction

8️⃣ Emotion Probability

9️⃣ Customer Segmentation

🔟 Customer Retention

"""
)

st.sidebar.markdown("---")

st.sidebar.info(

"""
Model

✅ Fine-Tuned IndoBERT

Segmentation

✅ KMeans

Deployment

✅ Streamlit
"""
)

# ==========================================================
# MAIN PAGE
# ==========================================================

st.title("📊 Livin Emotion Analysis Dashboard")

st.markdown("---")

st.markdown(

"""
Selamat datang pada aplikasi

**Emotion Analysis menggunakan Fine-Tuned IndoBERT**

Aplikasi ini melakukan:

- Emotion Classification
- Emotion Probability
- Customer Segmentation
- Customer Retention Recommendation

Silakan gunakan menu di sebelah kiri untuk memulai analisis.
"""
)

st.markdown("---")

# ==========================================================
# FEATURE
# ==========================================================

col1,col2,col3,col4 = st.columns(4)

with col1:

    st.metric(

        "Model",

        "IndoBERT"

    )

with col2:

    st.metric(

        "Emotion",

        "4 Label"

    )

with col3:

    st.metric(

        "Segmentation",

        "KMeans"

    )

with col4:

    st.metric(

        "Deployment",

        "Streamlit"

    )

st.markdown("---")

st.subheader("📌 Workflow")

st.image(

"https://raw.githubusercontent.com/simple-icons/simple-icons/develop/icons/python.svg",

width=80

)

st.markdown("""

Review

⬇

Cleaning

⬇

Case Folding

⬇

Normalization

⬇

Tokenizer

⬇

Emotion Prediction

⬇

Emotion Probability

⬇

Customer Segmentation

⬇

Customer Retention

""")

st.markdown("---")

st.info(

"""
Silakan pilih halaman pada sidebar.

Dashboard akan otomatis menampilkan hasil sesuai proses penelitian.
"""
)

# ==========================================================
# FOOTER
# ==========================================================

st.markdown("---")

st.caption(

FOOTER

)
