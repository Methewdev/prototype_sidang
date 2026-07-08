
# =========================================================
MODEL EVALUATION
# =========================================================

import streamlit as st

from modules.utils import require_session

from modules.model_evaluation import (
    MODEL_REPOS,
    get_all_metrics,
    best_model,
    metric_bar,
    radar_chart,
    load_report,
    load_confusion_matrix,
    load_history,
    plot_confusion_matrix,
    training_history_chart,
    ranking_model,
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
Perbandingan performa model Transformer yang digunakan
dalam penelitian Customer Retention.
"""
)

# =====================================================
# LOAD DATA
# =====================================================

try:

    with st.spinner("Loading evaluation metrics..."):

        metrics_df = get_all_metrics()

except Exception as e:

    st.error(f"Failed loading metrics.\n\n{e}")

    st.stop()

if metrics_df.empty:

    st.warning("Metrics tidak ditemukan.")

    st.stop()

best = best_model(metrics_df)

# =====================================================
# BEST MODEL
# =====================================================

st.success(

f"""
🏆 **Best Model**

Model terbaik berdasarkan **Weighted F1 Score**

**{best['Model']}**

Accuracy : **{best['Accuracy']:.2%}**

Precision : **{best['Precision']:.2%}**

Recall : **{best['Recall']:.2%}**

F1 Score : **{best['F1 Score']:.2%}**
"""

)

# =====================================================
# METRIC CARD
# =====================================================

st.subheader("📊 Performance Metrics")

c1,c2,c3,c4,c5 = st.columns(5)

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

    table[col] = table[col].map(

        lambda x:f"{x:.2%}"

    )

table["Loss"] = table["Loss"].map(

    lambda x:f"{x:.4f}"

)

st.dataframe(

    table,

    use_container_width=True,

    hide_index=True

)

st.download_button(

    "⬇ Download Metrics",

    metrics_df.to_csv(index=False),

    file_name="metrics.csv",

    mime="text/csv"

)

st.divider()
# =====================================================
# PERFORMANCE VISUALIZATION
# =====================================================

st.subheader("📈 Performance Comparison")

col1, col2 = st.columns(2)

with col1:

    st.plotly_chart(
        metric_bar(
            metrics_df,
            "Accuracy"
        ),
        use_container_width=True
    )

with col2:

    st.plotly_chart(
        metric_bar(
            metrics_df,
            "Precision"
        ),
        use_container_width=True
    )

col3, col4 = st.columns(2)

with col3:

    st.plotly_chart(
        metric_bar(
            metrics_df,
            "Recall"
        ),
        use_container_width=True
    )

with col4:

    st.plotly_chart(
        metric_bar(
            metrics_df,
            "F1 Score"
        ),
        use_container_width=True
    )

st.divider()

# =====================================================
# RADAR CHART
# =====================================================

st.subheader("📡 Overall Model Performance")

st.plotly_chart(

    radar_chart(
        metrics_df
    ),

    use_container_width=True

)

st.divider()

# =====================================================
# MODEL RANKING
# =====================================================

st.subheader("🥇 Model Ranking")

ranking_df = ranking_model(metrics_df)

ranking_show = ranking_df.copy()

for col in [

    "Accuracy",

    "Precision",

    "Recall",

    "F1 Score"

]:

    ranking_show[col] = ranking_show[col].map(

        lambda x: f"{x:.2%}"

    )

ranking_show["Loss"] = ranking_show["Loss"].map(

    lambda x: f"{x:.4f}"

)

st.dataframe(

    ranking_show,

    use_container_width=True,

    hide_index=True

)

st.info(

"""
Ranking dihitung berdasarkan nilai **Weighted F1 Score**.
Model dengan nilai F1 tertinggi menjadi model terbaik.
"""

)

st.divider()
# =====================================================
# DETAIL MODEL EVALUATION
# =====================================================

st.subheader("📑 Detail Evaluation")

tab1, tab2, tab3 = st.tabs(
    [
        "🤖 IndoBERT",
        "🌐 mBERT",
        "🚀 DeBERTa"
    ]
)
with tab1:

    repo = MODEL_REPOS["IndoBERT"]

    st.markdown("## 🤖 IndoBERT")

    # ----------------------------------
    # Classification Report
    # ----------------------------------

    st.markdown("### 📄 Classification Report")

    report = load_report(repo)

    st.dataframe(
        report,
        use_container_width=True,
        hide_index=True
    )

    # ----------------------------------
    # Confusion Matrix
    # ----------------------------------

    st.markdown("### 🔥 Confusion Matrix")

    cm = load_confusion_matrix(repo)

    st.plotly_chart(
        plot_confusion_matrix(
            cm,
            "IndoBERT Confusion Matrix"
        ),
        use_container_width=True
    )

    # ----------------------------------
    # Training History
    # ----------------------------------

    st.markdown("### 📈 Training History")

    history = load_history(repo)

    st.plotly_chart(
        training_history_chart(
            history
        ),
        use_container_width=True
    )
    with tab2:

    repo = MODEL_REPOS["mBERT"]

    st.markdown("## 🌐 mBERT")

    st.markdown("### 📄 Classification Report")

    report = load_report(repo)

    st.dataframe(
        report,
        use_container_width=True,
        hide_index=True
    )

    st.markdown("### 🔥 Confusion Matrix")

    cm = load_confusion_matrix(repo)

    st.plotly_chart(
        plot_confusion_matrix(
            cm,
            "mBERT Confusion Matrix"
        ),
        use_container_width=True
    )

    st.markdown("### 📈 Training History")

    history = load_history(repo)

    st.plotly_chart(
        training_history_chart(
            history
        ),
        use_container_width=True
    )
    with tab3:

    repo = MODEL_REPOS["DeBERTa"]

    st.markdown("## 🚀 DeBERTa")

    st.markdown("### 📄 Classification Report")

    report = load_report(repo)

    st.dataframe(
        report,
        use_container_width=True,
        hide_index=True
    )

    st.markdown("### 🔥 Confusion Matrix")

    cm = load_confusion_matrix(repo)

    st.plotly_chart(
        plot_confusion_matrix(
            cm,
            "DeBERTa Confusion Matrix"
        ),
        use_container_width=True
    )

    st.markdown("### 📈 Training History")

    history = load_history(repo)

    st.plotly_chart(
        training_history_chart(
            history
        ),
        use_container_width=True
    )

st.divider()
