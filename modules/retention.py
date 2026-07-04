# =====================================================
# SEGMENT STATISTICS
# =====================================================

def segment_statistics(df):

    return {

        "Total Customer":len(df),

        "Total Segment":

        df["Customer Segment"].nunique(),

        "Dominant Segment":

        df["Customer Segment"].mode()[0]

    }
        # =====================================================
# RETENTION DATAFRAME
# =====================================================

def customer_retention(df):

    data = df.copy()

    data["Priority"] = data["Customer Segment"].map(

        lambda x: RETENTION_STRATEGY[x]["Priority"]

    )

    data["Recommendation"] = data["Customer Segment"].map(

        lambda x: RETENTION_STRATEGY[x]["Recommendation"]

    )

    data["Business Insight"] = data["Customer Segment"].map(

        lambda x: RETENTION_STRATEGY[x]["Business Insight"]

    )

    return data
# =====================================================
# PRIORITY SUMMARY
# =====================================================

def priority_summary(df):

    summary = (

        df["Priority"]

        .value_counts()

        .reset_index()

    )

    summary.columns=[

        "Priority",

        "Total"

    ]

    summary["Percentage"]=(

        summary["Total"]

        /

        summary["Total"].sum()

        *100

    ).round(2)

    return summary
# =====================================================
# SEGMENT SUMMARY
# =====================================================

def retention_summary(df):

    summary=(

        df

        .groupby(

            "Customer Segment"

        )

        .agg(

            Customer=("Customer Segment","count"),

            Avg_Confidence=("confidence","mean")

        )

        .round(3)

    )

    return summary
# =====================================================
# KPI
# =====================================================

def retention_kpi(df):

    return{

        "Total Customer":len(df),

        "High Priority":

        len(

            df[

                df["Priority"]=="High"

            ]

        ),

        "Medium Priority":

        len(

            df[

                df["Priority"]=="Medium"

            ]

        ),

        "Low Priority":

        len(

            df[

                df["Priority"]=="Low"

            ]

        )

    }
# =====================================================
# BUSINESS RECOMMENDATION
# =====================================================

def recommendation(segment):

    return RETENTION_STRATEGY.get(segment,{})
