"""
=========================================================
INDOBERT TOKENIZER
=========================================================
"""

import streamlit as st
import pandas as pd

from modules.model_loader import load_tokenizer
from config import MAX_LENGTH

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(

    page_title="IndoBERT Tokenizer",

    page_icon="🧠",

    layout="wide"

)

st.title("🧠 IndoBERT Tokenizer")

st.markdown("---")

# ==========================================================
# CHECK SESSION
# ==========================================================

if "normal_df" not in st.session_state:

    st.warning("Silakan lakukan proses Normalization terlebih dahulu.")

    st.stop()

df = st.session_state["normal_df"].copy()

tokenizer = load_tokenizer()

# ==========================================================
# PILIH REVIEW
# ==========================================================

st.subheader("Pilih Review")

index = st.number_input(

    "Index Review",

    min_value=0,

    max_value=len(df)-1,

    value=0,

    step=1

)

text = str(df.loc[index, "normalization"])

st.markdown("---")

# ==========================================================
# REVIEW
# ==========================================================

st.subheader("Review")

st.info(text)

# ==========================================================
# TOKENIZER
# ==========================================================

encoding = tokenizer(

    text,

    truncation=True,

    padding="max_length",

    max_length=MAX_LENGTH,

    return_tensors="pt"

)

tokens = tokenizer.convert_ids_to_tokens(

    encoding["input_ids"][0]

)

input_ids = encoding["input_ids"][0].tolist()

attention_mask = encoding["attention_mask"][0].tolist()

# ==========================================================
# TOKEN
# ==========================================================

st.markdown("---")

st.subheader("Token")

token_df = pd.DataFrame({

    "Position": range(len(tokens)),

    "Token": tokens

})

st.dataframe(

    token_df,

    use_container_width=True,

    height=350

)

# ==========================================================
# INPUT IDS
# ==========================================================

st.markdown("---")

st.subheader("Input IDs")

id_df = pd.DataFrame({

    "Position": range(len(input_ids)),

    "Input ID": input_ids

})

st.dataframe(

    id_df,

    use_container_width=True,

    height=350

)

# ==========================================================
# ATTENTION MASK
# ==========================================================

st.markdown("---")

st.subheader("Attention Mask")

mask_df = pd.DataFrame({

    "Position": range(len(attention_mask)),

    "Mask": attention_mask

})

st.dataframe(

    mask_df,

    use_container_width=True,

    height=350

)

# ==========================================================
# DECODE
# ==========================================================

st.markdown("---")

st.subheader("Decoded Text")

decoded = tokenizer.decode(

    input_ids,

    skip_special_tokens=True

)

st.success(decoded)

# ==========================================================
# TOKEN INFORMATION
# ==========================================================

st.markdown("---")

st.subheader("Tokenizer Information")

col1,col2,col3,col4 = st.columns(4)

with col1:

    st.metric(

        "Vocabulary",

        tokenizer.vocab_size

    )

with col2:

    st.metric(

        "Total Token",

        len(tokens)

    )

with col3:

    st.metric(

        "Input Length",

        sum(attention_mask)

    )

with col4:

    st.metric(

        "Max Length",

        MAX_LENGTH

    )

# ==========================================================
# SPECIAL TOKEN
# ==========================================================

st.markdown("---")

st.subheader("Special Token")

special = pd.DataFrame({

    "Token":[

        "[CLS]",

        "[SEP]",

        "[PAD]",

        "[UNK]",

        "[MASK]"

    ],

    "Description":[

        "Awal Kalimat",

        "Akhir Kalimat",

        "Padding",

        "Unknown Token",

        "Masked Token"

    ]

})

st.dataframe(

    special,

    use_container_width=True

)

# ==========================================================
# SAVE SESSION
# ==========================================================

st.session_state["tokenizer_df"] = token_df
