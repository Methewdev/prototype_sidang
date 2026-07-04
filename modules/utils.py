"""
=========================================================
UTILITY MODULE
Livin Emotion Analysis
=========================================================
"""

from pathlib import Path
import pandas as pd
import streamlit as st

# =====================================================
# SESSION
# =====================================================

def save_session(key, value):
    st.session_state[key] = value


def get_session(key, default=None):
    return st.session_state.get(key, default)


def has_session(key):
    return key in st.session_state


def clear_session():
    st.session_state.clear()


# =====================================================
# DATASET
# =====================================================

def read_dataset(uploaded_file):

    if uploaded_file is None:
        return None

    extension = Path(uploaded_file.name).suffix.lower()

    if extension == ".csv":

        options = [

            {"sep": ",", "encoding": "utf-8"},

            {"sep": ";", "encoding": "utf-8"},

            {"sep": ",", "encoding": "latin1"},

            {"sep": ";", "encoding": "latin1"},

            {"sep": None, "engine": "python"}

        ]

        for option in options:

            uploaded_file.seek(0)

            try:

                return pd.read_csv(
                    uploaded_file,
                    **option
                )

            except Exception:

                continue

        raise ValueError(
            "CSV tidak dapat dibaca."
        )

    elif extension in [".xlsx", ".xls"]:

        return pd.read_excel(uploaded_file)

    else:

        raise ValueError(
            "Format file tidak didukung."
        )


# =====================================================
# COLUMN DETECTION
# =====================================================

TEXT_COLUMNS = [

    "content",

    "review",

    "ulasan",

    "text"

]

RATING_COLUMNS = [

    "score",

    "rating"

]

DATE_COLUMNS = [

    "at",

    "date",

    "tanggal"

]


def detect_text_column(df):

    for col in TEXT_COLUMNS:

        if col in df.columns:

            return col

    return None


def detect_rating_column(df):

    for col in RATING_COLUMNS:

        if col in df.columns:

            return col

    return None


def detect_date_column(df):

    for col in DATE_COLUMNS:

        if col in df.columns:

            return col

    return None


# =====================================================
# DATASET INFO
# =====================================================

def dataset_info(df):

    return {

        "rows": len(df),

        "columns": len(df.columns),

        "missing": int(df.isnull().sum().sum()),

        "duplicate": int(df.duplicated().sum())

    }


# =====================================================
# DATA TYPE
# =====================================================

def dataframe_info(df):

    return pd.DataFrame({

        "Column": df.columns,

        "Data Type": df.dtypes.astype(str),

        "Missing": df.isnull().sum().values,

        "Unique": df.nunique().values

    })


# =====================================================
# DOWNLOAD
# =====================================================

def download_csv(df):

    return df.to_csv(

        index=False

    ).encode("utf-8-sig")


# =====================================================
# VALIDATION
# =====================================================

def validate_dataframe(df):

    if df is None:

        return False

    if not isinstance(df, pd.DataFrame):

        return False

    if df.empty:

        return False

    return True


# =====================================================
# CHECK SESSION
# =====================================================

def require_session(key, message):

    if key not in st.session_state:

        st.warning(message)

        st.stop()

    df = st.session_state[key]

    if not validate_dataframe(df):

        st.warning(message)

        st.stop()

    return df
