"""
=========================================================
CUSTOMER RETENTION MODULE
=========================================================
Livin Emotion Analysis
=========================================================
"""

import pandas as pd

# =====================================================
# RETENTION STRATEGY
# =====================================================

RETENTION_RULE = {

    "😊 Nasabah Puas": {

        "Priority": "Low",

        "Retention Strategy":
        "Berikan reward, loyalty program, cashback, dan pertahankan kualitas layanan.",

        "Recommended Action":
        "Loyalty Program"

    },

    "😐 Nasabah Passive": {

        "Priority": "Medium",

        "Retention Strategy":
        "Tingkatkan engagement melalui edukasi fitur dan personalisasi promosi.",

        "Recommended Action":
        "Engagement Campaign"

    },

    "😟 Nasabah Tidak Puas": {

        "Priority": "High",

        "Retention Strategy":
        "Tindak lanjuti keluhan pelanggan dan tingkatkan kualitas layanan.",

        "Recommended Action":
        "Customer Service Follow-up"

    },

    "😠 Nasabah Frustasi": {

        "Priority": "Very High",

        "Retention Strategy":
        "Prioritaskan penyelesaian masalah, customer service proaktif, dan kompensasi bila diperlukan.",

        "Recommended Action":
        "Immediate Recovery"

    }

}
    }

}

# =====================================================
# CUSTOMER RETENTION
# =====================================================

def customer_retention(df):

    data = df.copy()

    if "Customer Segment" not in data.columns:
        raise ValueError(
            "Kolom 'Customer Segment' tidak ditemukan."
        )

    priority = []
    recommendation = []

    for segment in data["Customer Segment"]:

        segment = str(segment).strip()

        rule = RETENTION_RULE.get(segment)

        if rule is None:

            priority.append("Unknown")
            recommendation.append("-")

        else:

            priority.append(rule["Priority"])
            recommendation.append(rule["Retention Strategy"])

    data["Priority"] = priority
    data["Retention Strategy"] = recommendation

    return data


# =====================================================
# SUMMARY
# =====================================================

def retention_summary(df):

    if "Customer Segment" not in df.columns:
        return pd.DataFrame()

    summary = (
        df["Customer Segment"]
        .value_counts()
        .reset_index()
    )

    summary.columns = [
        "Customer Segment",
        "Total Customer"
    ]

    summary["Percentage"] = (
        summary["Total Customer"]
        / summary["Total Customer"].sum()
        * 100
    ).round(2)

    return summary


# =====================================================
# STATISTICS
# =====================================================

def retention_statistics(df):

    return {

        "Total Customer":
            len(df),

        "Highest Priority":
            df["Priority"].mode()[0]
            if "Priority" in df.columns
            else "-",

        "Customer Segment":
            df["Customer Segment"].mode()[0]
            if "Customer Segment" in df.columns
            else "-"

    }


# =====================================================
# PRIORITY DISTRIBUTION
# =====================================================

def priority_distribution(df):

    if "Priority" not in df.columns:
        return pd.DataFrame()

    priority = (
        df["Priority"]
        .value_counts()
        .reset_index()
    )

    priority.columns = [
        "Priority",
        "Total"
    ]

    return priority


# =====================================================
# STRATEGY TABLE
# =====================================================

def strategy_table(df):

    columns = [
        col
        for col in [
            "Customer Segment",
            "Priority",
            "Retention Strategy"
        ]
        if col in df.columns
    ]

    return (
        df[columns]
        .drop_duplicates()
    )
