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
        "Berikan reward, loyalty program, cashback, dan pertahankan kualitas layanan."

    },

    "😐 Nasabah Passive ": {

        "Priority": "Medium",

        "Retention Strategy":
        "Tingkatkan engagement melalui edukasi fitur dan personalisasi promosi."

    },

    "😟 Nasabah Tidak Puas": {

        "Priority": "High",

        "Retention Strategy":
        "Tindak lanjuti keluhan pelanggan dan tingkatkan kualitas layanan."

    },

    "😠 Nasabah Frustasi": {

        "Priority": "Very High",

        "Retention Strategy":
        "Prioritaskan penyelesaian masalah, customer service proaktif, dan kompensasi bila diperlukan."

    }

}
# =====================================================
# CUSTOMER RETENTION
# =====================================================

def customer_retention(df):

    data = df.copy()

    priority = []

    recommendation = []

    for segment in data["Customer Segment"]:

        rule = RETENTION_RULE.get(

            segment,

            {

                "Priority": "Unknown",

                "Retention Strategy": "-"

            }

        )

        priority.append(

            rule["Priority"]

        )

        recommendation.append(

            rule["Retention Strategy"]

        )

    data["Priority"] = priority

    data["Retention Strategy"] = recommendation

    return data
    # =====================================================
# SUMMARY
# =====================================================

def retention_summary(df):

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

        /

        summary["Total Customer"].sum()

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

            df["Priority"].mode()[0],

        "Customer Segment":

            df["Customer Segment"].mode()[0]

    }
    # =====================================================
# PRIORITY DISTRIBUTION
# =====================================================

def priority_distribution(df):

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
# TOP STRATEGY
# =====================================================

def strategy_table(df):

    return (

        df[

            [

                "Customer Segment",

                "Priority",

                "Retention Strategy"

            ]

        ]

        .drop_duplicates()

    )
