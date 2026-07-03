"""
=========================================================
EMOTION PREDICTION
=========================================================
Fine-Tuned IndoBERT
=========================================================
"""

import streamlit as st
import pandas as pd

from modules.preprocessing import preprocess_text
from modules.prediction import (
    predict,
    predict_probability,
    predict_dataframe
)

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Emotion Prediction",
    page_icon="😊",
    layout="wide"
)

st.title("😊 Emotion Prediction")

st.markdown("---")

# ==========================================================
# CHECK DATASET
# ==========================================================

if "normal_df" not in st.session_state:

    st.warning(
        "Silakan lakukan proses Normalization terlebih dahulu."
    )

    st.stop()

dataset = st.session_state["normal_df"].copy()

# ==========================================================
# TAB
# ==========================================================

tab1, tab2 = st.tabs(
    [
        "Single Prediction",
        "Batch Prediction"
    ]
)

# ==========================================================
# SINGLE PREDICTION
# ==========================================================

with tab1:

    st.subheader("Single Review Prediction")

    text = st.text_area(

        "Masukkan Review",

        height=150

    )

    if st.button(

        "Predict Emotion",

        use_container_width=True

    ):

        if text.strip() == "":

            st.warning(
                "Review tidak boleh kosong."
            )

        else:

            processed = preprocess_text(text)

            result = predict(processed)

            probability = predict_probability(processed)

            st.markdown("---")

            col1, col2 = st.columns(2)

            with col1:

                st.metric(

                    "Emotion",

                    result["emotion"]

                )

            with col2:

                st.metric(

                    "Confidence",

                    f"{result['confidence']*100:.2f}%"

                )

            st.markdown("---")

            st.subheader(
                "Emotion Probability"
            )

            probability_df = pd.DataFrame({

                "Emotion": probability.keys(),

                "Probability (%)":

                [

                    round(i*100,2)

                    for i in probability.values()

                ]

            })

            st.dataframe(

                probability_df,

                use_container_width=True

            )

            st.bar_chart(

                probability_df.set_index("Emotion")

            )

# ==========================================================
# BATCH PREDICTION
# ==========================================================

with tab2:

    st.subheader(
        "Batch Emotion Prediction"
    )

    st.info(
        """
        Sistem akan melakukan prediksi
        terhadap seluruh dataset.
        """
    )

    st.write(
        f"Jumlah Review : {len(dataset)}"
    )

    if st.button(

        "Start Prediction",

        type="primary",

        use_container_width=True

    ):

        progress = st.progress(0)

        status = st.empty()

        result_df = dataset.copy()
      """
=========================================================
EMOTION PREDICTION
=========================================================
Fine-Tuned IndoBERT
=========================================================
"""

import streamlit as st
import pandas as pd

from modules.preprocessing import preprocess_text
from modules.prediction import (
    predict,
    predict_probability,
    predict_dataframe
)

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Emotion Prediction",
    page_icon="😊",
    layout="wide"
)

st.title("😊 Emotion Prediction")

st.markdown("---")

# ==========================================================
# CHECK DATASET
# ==========================================================

if "normal_df" not in st.session_state:

    st.warning(
        "Silakan lakukan proses Normalization terlebih dahulu."
    )

    st.stop()

dataset = st.session_state["normal_df"].copy()

# ==========================================================
# TAB
# ==========================================================

tab1, tab2 = st.tabs(
    [
        "Single Prediction",
        "Batch Prediction"
    ]
)

# ==========================================================
# SINGLE PREDICTION
# ==========================================================

with tab1:

    st.subheader("Single Review Prediction")

    text = st.text_area(

        "Masukkan Review",

        height=150

    )

    if st.button(

        "Predict Emotion",

        use_container_width=True

    ):

        if text.strip() == "":

            st.warning(
                "Review tidak boleh kosong."
            )

        else:

            processed = preprocess_text(text)

            result = predict(processed)

            probability = predict_probability(processed)

            st.markdown("---")

            col1, col2 = st.columns(2)

            with col1:

                st.metric(

                    "Emotion",

                    result["emotion"]

                )

            with col2:

                st.metric(

                    "Confidence",

                    f"{result['confidence']*100:.2f}%"

                )

            st.markdown("---")

            st.subheader(
                "Emotion Probability"
            )

            probability_df = pd.DataFrame({

                "Emotion": probability.keys(),

                "Probability (%)":

                [

                    round(i*100,2)

                    for i in probability.values()

                ]

            })

            st.dataframe(

                probability_df,

                use_container_width=True

            )

            st.bar_chart(

                probability_df.set_index("Emotion")

            )

# ==========================================================
# BATCH PREDICTION
# ==========================================================

with tab2:

    st.subheader(
        "Batch Emotion Prediction"
    )

    st.info(
        """
        Sistem akan melakukan prediksi
        terhadap seluruh dataset.
        """
    )

    st.write(
        f"Jumlah Review : {len(dataset)}"
    )

    if st.button(

        "Start Prediction",

        type="primary",

        use_container_width=True

    ):

        progress = st.progress(0)

        status = st.empty()

        result_df = dataset.copy()
              # ================================================
        # BATCH PREDICTION
        # ================================================

        total_review = len(result_df)

        emotion_list = []
        confidence_list = []

        frustration = []
        neutral = []
        sadness = []
        happiness = []

        for i, row in result_df.iterrows():

            text = str(row["normalization"])

            result = predict(text)

            prob = result["probability"]

            emotion_list.append(
                result["emotion"]
            )

            confidence_list.append(
                round(result["confidence"],4)
            )

            frustration.append(
                round(float(prob[0]),4)
            )

            neutral.append(
                round(float(prob[1]),4)
            )

            sadness.append(
                round(float(prob[2]),4)
            )

            happiness.append(
                round(float(prob[3]),4)
            )

            progress.progress(
                (i+1)/total_review
            )

            status.text(

                f"Processing {i+1} / {total_review}"

            )

        result_df["emotion"] = emotion_list

        result_df["confidence"] = confidence_list

        result_df["Frustrasi"] = frustration

        result_df["Netral"] = neutral

        result_df["Sedih"] = sadness

        result_df["Senang"] = happiness

        progress.empty()

        status.empty()

        st.success("Prediction Finished")
        # ================================================
        # SAVE SESSION
        # ================================================

        st.session_state["prediction_df"] = result_df
              st.markdown("---")

        st.subheader("Prediction Summary")

        col1,col2,col3,col4 = st.columns(4)

        with col1:

            st.metric(

                "Total Review",

                len(result_df)

            )

        with col2:

            st.metric(

                "Dominant Emotion",

                result_df["emotion"].mode()[0]

            )

        with col3:

            st.metric(

                "Average Confidence",

                f"{result_df['confidence'].mean()*100:.2f}%"

            )

        with col4:

            st.metric(

                "Emotion Class",

                result_df["emotion"].nunique()

            )
                  st.markdown("---")

        st.subheader("Prediction Result")

        st.dataframe(

            result_df,

            use_container_width=True,

            height=500

        )
              st.markdown("---")

        st.subheader("Emotion Distribution")

        emotion_count = (

            result_df["emotion"]

            .value_counts()

            .reset_index()

        )

        emotion_count.columns=[

            "Emotion",

            "Total"

        ]

        st.bar_chart(

            emotion_count,

            x="Emotion",

            y="Total"

        )
              st.markdown("---")

        csv = result_df.to_csv(

            index=False

        ).encode("utf-8-sig")

        st.download_button(

            "⬇ Download Prediction Result",

            csv,

            "prediction_result.csv",

            "text/csv"

        )
              st.success(

            """
            Prediction selesai.

            Silakan lanjut ke halaman
            Emotion Probability.
            """

        )
      
