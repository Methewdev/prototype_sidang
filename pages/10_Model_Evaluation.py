"""
=========================================================
MODEL EVALUATION
=========================================================
"""

import streamlit as st

from modules.utils import require_session

from modules.model_evaluation import (
    MODEL_REPOS,
    get_all_metrics,
    best_model,
    ranking_model,
    metric_bar,
    radar_chart,
    load_report,
    load_confusion_matrix,
    load_history,
    plot_confusion_matrix,
    training_history_chart
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

st.caption(
    "Perbandingan performa model Transformer "
    "IndoBERT, mBERT, dan DeBERTa."
)

# =====================================================
# LOAD METRICS
# =====================================================

try:

    with st.spinner("Loading evaluation..."):

        metrics_df = get_all_metrics()

except Exception as e:

    st.error(e)

    st.stop()

if metrics_df.empty:

    st.warning("Evaluation metrics tidak ditemukan.")

    st.stop()

best = best_model(metrics_df)

# =====================================================
# BEST MODEL
# =====================================================

st.success(
    f"""
🏆 **Best Model**

Model : **{best['Model']}**

Accuracy : **{best['Accuracy']:.2%}**

Precision : **{best['Precision']:.2%}**

Recall : **{best['Recall']:.2%}**

F1 Score : **{best['F1 Score']:.2%}**

Loss : **{best['Loss']:.4f}**
"""
)

# =====================================================
# METRIC CARD
# =====================================================

st.subheader("📊 Performance Metrics")

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric(
    "Accuracy",
    f"{best['Accuracy']:.2%}"
)

c2.metric(
    "Precision",
    f"{best['Precision']:.2%}"
)

c3.metric(
    "Recall",
    f"{best['Recall']:.2%}"
)

c4.metric(
    "F1 Score",
    f"{best['F1 Score']:.2%}"
)

c5.metric(
    "Loss",
    f"{best['Loss']:.4f}"
)

st.divider()

# =====================================================
# PERFORMANCE TABLE
# =====================================================

st.subheader("📋 Model Comparison")

table = metrics_df.copy()

for col in [

    "Accuracy",

    "Precision",

    "Recall",

    "F1 Score"

]:

    table[col] = table[col].apply(

        lambda x: f"{x:.2%}"

    )

table["Loss"] = table["Loss"].apply(

    lambda x: f"{x:.4f}"

)

st.dataframe(

    table,

    use_container_width=True,

    hide_index=True

)

st.divider()
