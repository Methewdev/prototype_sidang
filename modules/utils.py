"""
=========================================================
UTILITIES MODULE
=========================================================
Livin Emotion Analysis
=========================================================
"""

import io
import streamlit as st
import pandas as pd

from config import (
    LOGO,
    CSS_FILE
)
# =====================================================
# SAVE SESSION
# =====================================================

def save_session(

    key,

    value

):

    st.session_state[key] = value
  # =====================================================
# REQUIRE SESSION
# =====================================================

def require_session(

    key,

    message

):

    if key not in st.session_state:

        st.warning(message)

        st.stop()

    return st.session_state[key]
  # =====================================================
# CLEAR SESSION
# =====================================================

def clear_session():

    st.session_state.clear()
  # =====================================================
# DOWNLOAD CSV
# =====================================================

def download_csv(df):

    return df.to_csv(

        index=False

    ).encode("utf-8")
  # =====================================================
# DETECT TEXT COLUMN
# =====================================================

def detect_text_column(df):

    candidates = [

        "content",

        "review",

        "ulasan",

        "text",

        "comment",

        "komentar"

    ]

    columns = [

        c.lower()

        for c in df.columns

    ]

    for candidate in candidates:

        if candidate in columns:

            index = columns.index(candidate)

            return df.columns[index]

    return None
  # =====================================================
# VALIDATE DATAFRAME
# =====================================================

def validate_dataframe(df):

    if df.empty:

        return False

    if detect_text_column(df) is None:

        return False

    return True
  # =====================================================
# DATAFRAME INFO
# =====================================================

def dataframe_info(df):

    return {

        "Rows":len(df),

        "Columns":len(df.columns),

        "Missing":df.isna().sum().sum(),

        "Duplicate":df.duplicated().sum()

    }
  # =====================================================
# FORMAT PERCENTAGE
# =====================================================

def format_percentage(value):

    return f"{value:.2f}%"
  # =====================================================
# RESET PIPELINE
# =====================================================

def reset_pipeline():

    keys = [

        "preprocess_df",

        "prediction_df",

        "segmentation_df",

        "retention_df"

    ]

    for key in keys:

        if key in st.session_state:

            del st.session_state[key]
