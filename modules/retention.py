"""
=========================================================
CUSTOMER RETENTION MODULE
=========================================================
"""

import pandas as pd
# =====================================================
# SEGMENT PROFILE
# =====================================================

SEGMENT_PROFILE = {

    "Senang":{

        "Segment":"😊 Loyal Customer",

        "Risk":"Low",

        "Retention":"Pertahankan kualitas layanan, berikan reward, cashback, loyalty program."

    },

    "Netral":{

        "Segment":"😐 Passive Customer",

        "Risk":"Medium",

        "Retention":"Tingkatkan engagement melalui edukasi fitur dan personalisasi promosi."

    },

    "Sedih":{

        "Segment":"😟 Unsatisfied Customer",

        "Risk":"High",

        "Retention":"Lakukan follow-up terhadap keluhan dan tingkatkan kualitas layanan."

    },

    "Frustrasi":{

        "Segment":"😠 At-Risk Customer",

        "Risk":"Very High",

        "Retention":"Prioritaskan penyelesaian masalah, percepat response customer service, dan berikan kompensasi apabila diperlukan."

    }

}
# =====================================================
# RETENTION RECOMMENDATION
# =====================================================

def customer_retention(df):

    data = df.copy()

    segment = []

    risk = []

    recommendation = []

    for emotion in data["emotion"]:

        info = SEGMENT_PROFILE.get(emotion)

        segment.append(

            info["Segment"]

        )

        risk.append(

            info["Risk"]

        )

        recommendation.append(

            info["Retention"]

        )

    data["Customer Type"] = segment

    data["Risk Level"] = risk

    data["Retention Strategy"] = recommendation

    return data
  # =====================================================
# SUMMARY
# =====================================================

def retention_summary(df):

    summary = (

        df["Customer Type"]

        .value_counts()

        .reset_index()

    )

    summary.columns = [

        "Customer Type",

        "Total"

    ]

    summary["Percentage"] = (

        summary["Total"]

        /

        summary["Total"].sum()

        *100

    ).round(2)

    return summary
  # =====================================================
# RISK DISTRIBUTION
# =====================================================

def risk_distribution(df):

    risk = (

        df["Risk Level"]

        .value_counts()

        .reset_index()

    )

    risk.columns = [

        "Risk",

        "Total"

    ]

    return risk
  # =====================================================
# STATISTICS
# =====================================================

def retention_statistics(df):

    return {

        "Total Customer":

        len(df),

        "Customer Type":

        df["Customer Type"]

        .nunique(),

        "Highest Risk":

        df["Risk Level"]

        .mode()[0]

    }
