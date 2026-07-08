"""
=========================================================
MODEL EVALUATION
=========================================================
"""

import streamlit as st

from modules.utils import (
    require_session
)

from modules.model_evaluation import (
    get_all_metrics,
    best_model,
    metric_bar,
    radar_chart,
    MODEL_REPOS
)

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Model Evaluation",
    page_icon="🏆",
    layout="wide"
)

require_session()

# =====================================================
# TITLE
# =====================================================

st.title("🏆 Model Evaluation")

st.markdown(
"""
Perbandingan performa tiga model Transformer
yang digunakan pada penelitian.

- IndoBERT
- mBERT
- DeBERTa
"""
)

# =====================================================
# LOAD DATA
# =====================================================

with st.spinner("Loading evaluation metrics..."):

    metrics_df = get_all_metrics()

best = best_model(metrics_df)

# =====================================================
# BEST MODEL
# =====================================================

st.success(

f"""
### 🏆 Best Model

Model terbaik berdasarkan **F1 Score**

**{best['Model']}**

Accuracy :

**{best['Accuracy']:.2%}**

F1 Score :

**{best['F1 Score']:.2%}**
"""
)

# =====================================================
# METRIC CARD
# =====================================================

st.subheader("📊 Performance Metrics")

col1,col2,col3,col4,col5 = st.columns(5)

with col1:

    st.metric(

        "Accuracy",

        f"{best['Accuracy']:.2%}"

    )

with col2:

    st.metric(

        "Precision",

        f"{best['Precision']:.2%}"

    )

with col3:

    st.metric(

        "Recall",

        f"{best['Recall']:.2%}"

    )

with col4:

    st.metric(

        "F1 Score",

        f"{best['F1 Score']:.2%}"

    )

with col5:

    st.metric(

        "Loss",

        f"{best['Loss']:.4f}"

    )

st.divider()

# =====================================================
# PERFORMANCE TABLE
# =====================================================

st.subheader("📋 Model Comparison")

show_df = metrics_df.copy()

show_df["Accuracy"] = show_df["Accuracy"].map(
    lambda x:f"{x:.2%}"
)

show_df["Precision"] = show_df["Precision"].map(
    lambda x:f"{x:.2%}"
)

show_df["Recall"] = show_df["Recall"].map(
    lambda x:f"{x:.2%}"
)

show_df["F1 Score"] = show_df["F1 Score"].map(
    lambda x:f"{x:.2%}"
)

show_df["Loss"] = show_df["Loss"].map(
    lambda x:f"{x:.4f}"
)

st.dataframe(

    show_df,

    use_container_width=True,

    hide_index=True

)

st.divider()

# =====================================================
# COMPARISON CHART
# =====================================================

st.subheader("📈 Model Comparison Chart")

left,right = st.columns(2)

with left:

    st.plotly_chart(

        metric_bar(

            metrics_df,

            "Accuracy"

        ),

        use_container_width=True

    )

with right:

    st.plotly_chart(

        metric_bar(

            metrics_df,

            "F1 Score"

        ),

        use_container_width=True

    )

left,right = st.columns(2)

with left:

    st.plotly_chart(

        metric_bar(

            metrics_df,

            "Precision"

        ),

        use_container_width=True

    )

with right:

    st.plotly_chart(

        metric_bar(

            metrics_df,

            "Recall"

        ),

        use_container_width=True

    )

st.divider()

# =====================================================
# RADAR CHART
# =====================================================

st.subheader("📡 Overall Performance")

st.plotly_chart(

    radar_chart(

        metrics_df

    ),

    use_container_width=True

)

st.divider()
