"""
=========================================================
EMOTION PROBABILITY
=========================================================
"""

import streamlit as st

from modules.utils import (
    require_session,
    download_csv
)

from modules.emotion_probability import (
    dataframe_probability,
    probability_summary,
    probability_heatmap,
    average_probability,
    average_probability_chart
)

st.set_page_config(
    page_title="Emotion Probability",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Emotion Probability")

st.markdown("---")

# =====================================================
# LOAD PREDICTION
# =====================================================

prediction_df = require_session(
    "prediction_df",
    "Silakan lakukan Emotion Prediction terlebih dahulu."
)

# =====================================================
# BUILD PROBABILITY
# =====================================================

probability_df = dataframe_probability(
    prediction_df
)

summary = probability_summary(
    probability_df
)

# =====================================================
# SUMMARY
# =====================================================

c1, c2 = st.columns(2)

c1.metric(
    "Average Confidence",
    f"{summary['Average Confidence']} %"
)

c2.metric(
    "Dominant Emotion",
    summary["Dominant Emotion"]
)

st.markdown("---")

# =====================================================
# AVERAGE TABLE
# =====================================================

st.subheader("Average Probability")

avg = average_probability(
    probability_df
)

st.dataframe(
    avg,
    use_container_width=True
)

st.markdown("---")

# =====================================================
# BAR
# =====================================================

st.subheader("Average Probability Chart")

st.plotly_chart(
    average_probability_chart(
        probability_df
    ),
    use_container_width=True
)

st.markdown("---")

# =====================================================
# HEATMAP
# =====================================================

st.subheader("Probability Heatmap")

st.plotly_chart(
    probability_heatmap(
        probability_df
    ),
    use_container_width=True
)

st.markdown("---")

# =====================================================
# TABLE
# =====================================================

st.subheader("Emotion Probability")

display = probability_df[

    [

        "emotion",

        "confidence",

        "Frustrasi",

        "Netral",

        "Sedih",

        "Senang"

    ]

]

st.dataframe(

    display,

    use_container_width=True,

    height=500

)

st.markdown("---")

# =====================================================
# DOWNLOAD
# =====================================================

st.download_button(

    label="⬇ Download Probability",

    data=download_csv(

        probability_df

    ),

    file_name="emotion_probability.csv",

    mime="text/csv",

    use_container_width=True

)
# =====================================================
# LOAD CLUSTER MODEL
# =====================================================

def load_cluster_model():

    model_file = MODEL_PATH / "kmeans.pkl"

    scaler_file = MODEL_PATH / "scaler.pkl"

    if model_file.exists() and scaler_file.exists():

        model = joblib.load(model_file)

        scaler = joblib.load(scaler_file)

    else:

        scaler = StandardScaler()

        model = KMeans(

            n_clusters=N_CLUSTER,

            random_state=RANDOM_STATE,

            n_init="auto"

        )

    return scaler, model
  # =====================================================
# CUSTOMER SEGMENTATION
# =====================================================

def customer_segmentation(df):

    data = df.copy()

    scaler, model = load_cluster_model()

    feature = data[EMOTION_LABELS]

    X = scaler.fit_transform(feature)

    cluster = model.fit_predict(X)

    data["Cluster"] = cluster

    data["Customer Segment"] = (

        "Segment "

        +

        (cluster + 1).astype(str)

    )

    return data
  # =====================================================
# SAVE MODEL
# =====================================================

def save_cluster_model(model, scaler):

    joblib.dump(

        model,

        MODEL_PATH / "kmeans.pkl"

    )

    joblib.dump(

        scaler,

        MODEL_PATH / "scaler.pkl"

    )
  # =====================================================
# SUMMARY
# =====================================================

def segment_summary(df):

    summary = (

        df["Customer Segment"]

        .value_counts()

        .reset_index()

    )

    summary.columns = [

        "Segment",

        "Total Customer"

    ]

    summary["Percentage"] = (

        summary["Total Customer"]

        /

        summary["Total Customer"].sum()

        *100

    ).round(2)

    return summary
  # =====================================================
# PROFILE
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
# DOMINANT EMOTION
# =====================================================

def dominant_emotion(df):

    profile = cluster_profile(df)

    return profile.idxmax(axis=1)
  # =====================================================
# SILHOUETTE
# =====================================================

def silhouette(df):

    scaler = StandardScaler()

    X = scaler.fit_transform(

        df[EMOTION_LABELS]

    )

    model = KMeans(

        n_clusters=N_CLUSTER,

        random_state=RANDOM_STATE,

        n_init="auto"

    )

    cluster = model.fit_predict(X)

    return round(

        silhouette_score(

            X,

            cluster

        ),

        3

    )
  # =====================================================
# STATISTICS
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
