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
          # =====================================================
# SEGMENT MAPPING
# =====================================================

SEGMENT_MAPPING = {

    "Senang":{

        "Customer Segment":"😊 Loyal Customer",

        "Risk Level":"Low"

    },

    "Netral":{

        "Customer Segment":"😐 Passive Customer",

        "Risk Level":"Medium"

    },

    "Sedih":{

        "Customer Segment":"😟 Unsatisfied Customer",

        "Risk Level":"High"

    },

    "Frustrasi":{

        "Customer Segment":"😠 At-Risk Customer",

        "Risk Level":"Very High"

    }

}
# =====================================================
# CUSTOMER SEGMENTATION
# =====================================================

def customer_segmentation(df):

    data = df.copy()

    segment = []

    risk = []

    for emotion in data["emotion"]:

        info = SEGMENT_MAPPING.get(

            emotion,

            {

                "Customer Segment":"Unknown",

                "Risk Level":"Unknown"

            }

        )

        segment.append(

            info["Customer Segment"]

        )

        risk.append(

            info["Risk Level"]

        )

    data["Customer Segment"] = segment

    data["Risk Level"] = risk

    return data
  # =====================================================
# SEGMENT SUMMARY
# =====================================================

def segment_summary(df):

    summary = (

        df["Customer Segment"]

        .value_counts()

        .reset_index()

    )

    summary.columns = [

        "Customer Segment",

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
# DOMINANT EMOTION
# =====================================================

def dominant_emotion(df):

    result = (

        df

        .groupby(

            "Customer Segment"

        )["emotion"]

        .agg(

            lambda x:x.mode()[0]

        )

    )

    return result
  # =====================================================
# SEGMENT STATISTICS
# =====================================================

def segment_statistics(df):

    return {

        "Total Customer":

            len(df),

        "Total Segment":

            df["Customer Segment"]

            .nunique(),

        "Dominant Segment":

            df["Customer Segment"]

            .mode()[0]

    }
  # =====================================================
# SEGMENT PROFILE
# =====================================================

def cluster_profile(df):

    profile = (

        df

        .groupby(

            "Customer Segment"

        )[EMOTION_LABELS]

        .mean()

        .round(3)

    )

    return profile
  # =====================================================
# DISTRIBUTION
# =====================================================

def segment_distribution(df):

    return (

        df["Customer Segment"]

        .value_counts()

    )
