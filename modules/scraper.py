"""
=========================================================
GOOGLE PLAY REVIEW SCRAPER
=========================================================
Scraper Module
=========================================================
"""

from google_play_scraper import reviews, Sort
import pandas as pd


# =====================================================
# APP MAPPING
# =====================================================

APP_MAPPING = {
    "Livin By Mandiri": "id.bmri.livin",
   
}

# =====================================================
# SCRAPE REVIEWS
# =====================================================

def get_reviews(
    app_name: str,
    count: int = 500,
    country: str = "id",
    language: str = "id",
    sort: str = "newest"
):
    """
    Mengambil review dari Google Play Store.

    Parameters
    ----------
    app_name : str
        Nama aplikasi sesuai APP_MAPPING

    count : int
        Jumlah review

    country : str
        Negara

    language : str
        Bahasa

    sort : str
        newest
        relevant

    Returns
    -------
    DataFrame
    """

    if app_name not in APP_MAPPING:
        raise ValueError(f"{app_name} tidak tersedia.")

    app_id = APP_MAPPING[app_name]

    sort_option = (
        Sort.NEWEST if sort.lower() == "newest"
        else Sort.MOST_RELEVANT
    )

    result, _ = reviews(
        app_id,
        lang=language,
        country=country,
        sort=sort_option,
        count=count
    )

    df = pd.DataFrame(result)

    return clean_reviews(df)


# =====================================================
# CLEAN DATAFRAME
# =====================================================

def clean_reviews(df: pd.DataFrame):

    columns = {
        
        "userName": "username",
        "score": "rating",
        "content": "review",
        "at": "date",
    }

    available = {
        k: v
        for k, v in columns.items()
        if k in df.columns
    }

    df = df.rename(columns=available)

    keep_columns = list(available.values())

    df = df[keep_columns].copy()

    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"])

    if "reply_date" in df.columns:
        df["reply_date"] = pd.to_datetime(df["reply_date"])

    df = df.drop_duplicates(subset="review")

    df = df.reset_index(drop=True)

    return df


# =====================================================
# FILTER DATE
# =====================================================

def filter_date(
    df: pd.DataFrame,
    start_date=None,
    end_date=None
):

    if "date" not in df.columns:
        return df

    if start_date is not None:
        df = df[df["date"] >= pd.to_datetime(start_date)]

    if end_date is not None:
        df = df[df["date"] <= pd.to_datetime(end_date)]

    return df.reset_index(drop=True)


# =====================================================
# FILTER RATING
# =====================================================

def filter_rating(
    df: pd.DataFrame,
    rating=None
):

    if rating is None:
        return df

    return df[df["rating"] == rating].reset_index(drop=True)


# =====================================================
# FILTER VERSION
# =====================================================

def filter_version(
    df: pd.DataFrame,
    version=None
):

    if version is None:
        return df

    return df[df["app_version"] == version].reset_index(drop=True)


# =====================================================
# SEARCH KEYWORD
# =====================================================

def search_review(
    df: pd.DataFrame,
    keyword: str
):

    if keyword == "":
        return df

    return df[
        df["review"].str.contains(
            keyword,
            case=False,
            na=False
        )
    ].reset_index(drop=True)


# =====================================================
# DATASET INFO
# =====================================================

def dataset_info(df):

    info = {
        "Total Review": len(df),
        "Average Rating": round(df["rating"].mean(), 2),
        "Latest Review": df["date"].max(),
        "Oldest Review": df["date"].min(),
        "Total Version": df["app_version"].nunique()
        if "app_version" in df.columns else "-"
    }

    return info


# =====================================================
# EXPORT CSV
# =====================================================

def export_csv(df: pd.DataFrame):

    return df.to_csv(index=False).encode("utf-8")
