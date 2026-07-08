
# =====================================================
# MODEL EVALUATION MODULE
# =====================================================

import json
import pandas as pd

from huggingface_hub import hf_hub_download

import plotly.express as px
import plotly.graph_objects as go


# =====================================================
# HUGGINGFACE MODEL REPOSITORY
# =====================================================

MODEL_REPOS = {

    "Akurasi": "envidevelopment/livin-emotion-indobert",

}


# =====================================================
# LOAD METRICS
# =====================================================

def load_metrics(repo):

    file = hf_hub_download(

        repo_id=repo,

        filename="metrics.json"

    )

    with open(file, "r") as f:

        metrics = json.load(f)

    return metrics


# =====================================================
# LOAD CLASSIFICATION REPORT
# =====================================================

def load_report(repo):

    file = hf_hub_download(

        repo_id=repo,

        filename="classification_report.csv"

    )

    return pd.read_csv(file)


# =====================================================
# LOAD CONFUSION MATRIX
# =====================================================

def load_confusion_matrix(repo):

    file = hf_hub_download(

        repo_id=repo,

        filename="confusion_matrix.csv"

    )

    return pd.read_csv(

        file,

        index_col=0

    )


# =====================================================
# LOAD TRAINING HISTORY
# =====================================================

def load_history(repo):

    file = hf_hub_download(

        repo_id=repo,

        filename="history.csv"

    )

    return pd.read_csv(file)


# =====================================================
# LOAD ALL METRICS
# =====================================================

def get_all_metrics():

    rows = []

    for model_name, repo in MODEL_REPOS.items():

        metric = load_metrics(repo)

        rows.append({

            "Model": model_name,

            "Accuracy": metric.get("accuracy", 0),

            "Precision": metric.get("precision", 0),

            "Recall": metric.get("recall", 0),

            "F1 Score": metric.get("f1_score", 0),

            "Loss": metric.get("loss", 0)

        })

    return pd.DataFrame(rows)
    # =====================================================
# BEST MODEL
# =====================================================

def best_model(df):

    if df.empty:
        return None

    return df.sort_values(
        by="F1 Score",
        ascending=False
    ).iloc[0]


# =====================================================
# MODEL RANKING
# =====================================================

def ranking_model(df):

    ranking = df.copy()

    ranking = ranking.sort_values(
        by="F1 Score",
        ascending=False
    )

    ranking["Rank"] = range(1, len(ranking) + 1)

    return ranking


# =====================================================
# BAR CHART
# =====================================================

def metric_bar(df, metric):

    fig = px.bar(

        df,

        x="Model",

        y=metric,

        color="Model",

        text=df[metric].round(4)

    )

    fig.update_traces(

        textposition="outside"

    )

    fig.update_layout(

        title=f"{metric} Comparison",

        height=450,

        xaxis_title="Model",

        yaxis_title=metric,

        showlegend=False

    )

    return fig


# =====================================================
# LINE CHART
# =====================================================

def metric_line(df):

    data = df.melt(

        id_vars="Model",

        value_vars=[

            "Accuracy",

            "Precision",

            "Recall",

            "F1 Score"

        ],

        var_name="Metric",

        value_name="Score"

    )

    fig = px.line(

        data,

        x="Metric",

        y="Score",

        color="Model",

        markers=True

    )

    fig.update_layout(

        title="Performance Comparison",

        height=450

    )

    return fig


# =====================================================
# RADAR CHART
# =====================================================

def radar_chart(df):

    categories = [

        "Accuracy",

        "Precision",

        "Recall",

        "F1 Score"

    ]

    fig = go.Figure()

    for _, row in df.iterrows():

        fig.add_trace(

            go.Scatterpolar(

                r=[

                    row["Accuracy"],

                    row["Precision"],

                    row["Recall"],

                    row["F1 Score"]

                ],

                theta=categories,

                fill="toself",

                name=row["Model"]

            )

        )

    fig.update_layout(

        polar=dict(

            radialaxis=dict(

                visible=True,

                range=[0, 1]

            )

        ),

        height=600,

        title="Radar Performance Comparison"

    )

    return fig
    # =====================================================
# CONFUSION MATRIX
# =====================================================

def plot_confusion_matrix(cm_df, title="Confusion Matrix"):

    fig = px.imshow(

        cm_df,

        text_auto=True,

        color_continuous_scale="Blues",

        aspect="auto"

    )

    fig.update_layout(

        title=title,

        xaxis_title="Predicted Label",

        yaxis_title="True Label",

        height=500

    )

    return fig


# =====================================================
# TRAINING HISTORY
# =====================================================

def training_history_chart(history_df):

    fig = go.Figure()

    # Training Loss
    if "loss" in history_df.columns:

        train = history_df.dropna(subset=["loss"])

        fig.add_trace(

            go.Scatter(

                x=train["epoch"],

                y=train["loss"],

                mode="lines+markers",

                name="Training Loss"

            )

        )

    # Validation Loss
    if "eval_loss" in history_df.columns:

        valid = history_df.dropna(subset=["eval_loss"])

        fig.add_trace(

            go.Scatter(

                x=valid["epoch"],

                y=valid["eval_loss"],

                mode="lines+markers",

                name="Validation Loss"

            )

        )

    fig.update_layout(

        title="Training History",

        xaxis_title="Epoch",

        yaxis_title="Loss",

        height=450

    )

    return fig


# =====================================================
# DOWNLOAD METRICS
# =====================================================

def metrics_csv(df):

    return df.to_csv(

        index=False

    ).encode("utf-8")


# =====================================================
# DOWNLOAD REPORT
# =====================================================

def report_csv(df):

    return df.to_csv(

        index=False

    ).encode("utf-8")


# =====================================================
# DOWNLOAD HISTORY
# =====================================================

def history_csv(df):

    return df.to_csv(

        index=False

    ).encode("utf-8")


# =====================================================
# SUMMARY
# =====================================================

def summary_model(df):

    best = best_model(df)

    if best is None:

        return "No evaluation result."

    summary = f"""
Best Model : {best['Model']}

Accuracy : {best['Accuracy']:.2%}

Precision : {best['Precision']:.2%}

Recall : {best['Recall']:.2%}

F1 Score : {best['F1 Score']:.2%}

Loss : {best['Loss']:.4f}
"""

    return summary
