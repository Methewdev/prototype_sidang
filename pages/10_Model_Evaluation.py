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
    radar_chart
)

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Model Evaluation",
    page_icon="🏆",
    layout="wide"
)

# Halaman ini tidak memerlukan session
# require_session()

# =====================================================
# TITLE
# =====================================================

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

**Model :** {best['Model']}

**Accuracy :** {best['Accuracy']:.2%}

**Precision :** {best['Precision']:.2%}

**Recall :** {best['Recall']:.2%}

**F1 Score :** {best['F1 Score']:.2%}
"""
)

# =====================================================
# METRIC CARD
# =====================================================

st.subheader("📊 Performance Metrics")

c1, c2, c3, c4 = st.columns(4)

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

st.dataframe(

    table,

    use_container_width=True,

    hide_index=True

)

st.divider()
# =====================================================
# PERFORMANCE VISUALIZATION
# =====================================================

st.subheader("📈 Performance Visualization")

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

st.subheader("📡 Overall Performance")

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

    ranking_show[col] = ranking_show[col].apply(
        lambda x: f"{x:.2%}"
    )

st.dataframe(

    ranking_show,

    use_container_width=True,

    hide_index=True

)

st.info(
"""
Model diurutkan berdasarkan **Weighted F1 Score**.

Semakin tinggi nilai **F1 Score**, semakin baik kemampuan model
dalam mengklasifikasikan emosi pengguna.
"""
)

st.divider()

        # ============================================
        # TRAINING HISTORY
        # ============================================

        st.markdown("### 📈 Training History")

        try:

            history = load_history(repo)

            st.plotly_chart(

                training_history_chart(

                    history

                ),

                use_container_width=True

            )

        except Exception as e:

            st.warning(
                f"Training History tidak ditemukan.\n\n{e}"
            )

st.divider()
