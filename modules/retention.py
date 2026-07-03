"""
=========================================================
CUSTOMER RETENTION MODULE
=========================================================
Customer Segment
        ↓
Priority
        ↓
Recommendation
        ↓
Business Insight
=========================================================
"""

import pandas as pd

from config import RETENTION

# ==========================================================
# GET PRIORITY
# ==========================================================

def get_priority(segment):

    if segment not in RETENTION:
        return "Unknown"

    return RETENTION[segment]["Priority"]


# ==========================================================
# GET RECOMMENDATION
# ==========================================================

def get_recommendation(segment):

    if segment not in RETENTION:
        return "-"

    return RETENTION[segment]["Recommendation"]


# ==========================================================
# GET BUSINESS INSIGHT
# ==========================================================

def get_business_insight(segment):

    insight = {

        "Satisfied Customer":
            "Pelanggan memiliki tingkat kepuasan tinggi dan berpotensi menjadi pelanggan loyal.",

        "Passive Customer":
            "Pelanggan belum menunjukkan loyalitas yang kuat sehingga perlu ditingkatkan engagement-nya.",

        "At-Risk Customer":
            "Pelanggan menunjukkan indikasi ketidakpuasan dan berpotensi berhenti menggunakan aplikasi."

    }

    return insight.get(segment, "-")


# ==========================================================
# SINGLE RETENTION
# ==========================================================

def retention_result(segment):

    return {

        "Customer Segment": segment,

        "Priority": get_priority(segment),

        "Recommendation": get_recommendation(segment),

        "Business Insight": get_business_insight(segment)

    }


# ==========================================================
# DATAFRAME RETENTION
# ==========================================================

def retention_dataframe(df):

    data = df.copy()

    data["Priority"] = data["Customer Segment"].apply(
        get_priority
    )

    data["Recommendation"] = data["Customer Segment"].apply(
        get_recommendation
    )

    data["Business Insight"] = data["Customer Segment"].apply(
        get_business_insight
    )

    return data


# ==========================================================
# PRIORITY SUMMARY
# ==========================================================

def priority_summary(df):

    return (

        df["Priority"]

        .value_counts()

        .reset_index()

        .rename(

            columns={

                "index":"Priority",

                "Priority":"Total"

            }

        )

    )


# ==========================================================
# SEGMENT SUMMARY
# ==========================================================

def retention_summary(df):

    summary = (

        df

        .groupby(

            "Customer Segment"

        )

        .agg(

            Total=("Customer Segment","count"),

            Avg_Confidence=("confidence","mean")

        )

        .round(3)

    )

    return summary


# ==========================================================
# HIGH PRIORITY
# ==========================================================

def high_priority(df):

    return df[

        df["Priority"]=="High"

    ]


# ==========================================================
# MEDIUM PRIORITY
# ==========================================================

def medium_priority(df):

    return df[

        df["Priority"]=="Medium"

    ]


# ==========================================================
# LOW PRIORITY
# ==========================================================

def low_priority(df):

    return df[

        df["Priority"]=="Low"

    ]


# ==========================================================
# CUSTOMER COUNT
# ==========================================================

def customer_count(df):

    return {

        "Total Customer":len(df),

        "High Priority":len(

            high_priority(df)

        ),

        "Medium Priority":len(

            medium_priority(df)

        ),

        "Low Priority":len(

            low_priority(df)

        )

    }


# ==========================================================
# EXPORT
# ==========================================================

def export_retention(df):

    return retention_dataframe(df)
