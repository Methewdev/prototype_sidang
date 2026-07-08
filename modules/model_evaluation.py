"""
=========================================================
MODEL EVALUATION
=========================================================
"""

import json
import pandas as pd

from huggingface_hub import hf_hub_download

import plotly.express as px
import plotly.graph_objects as go
"""
=========================================================
MODEL REPOSITORY
=========================================================
"""

MODEL_REPOS = {

    "IndoBERT":
        "envidevelopment/livin-emotion-indobert",

    "mBERT":
        "envidevelopment/livin-emotion-mbert",

    "DeBERTa":
        "envidevelopment/livin-emotion-deberta"

}
"""
=========================================================
LOAD METRICS
=========================================================
"""

def load_metrics(repo):

    file = hf_hub_download(

        repo_id=repo,

        filename="metrics.json"

    )

    with open(file,"r") as f:

        metric = json.load(f)

    return metric
  """
=========================================================
LOAD CLASSIFICATION REPORT
=========================================================
"""

def load_report(repo):

    file = hf_hub_download(

        repo_id=repo,

        filename="classification_report.csv"

    )

    return pd.read_csv(file)
  """
=========================================================
LOAD CONFUSION MATRIX
=========================================================
"""

def load_confusion_matrix(repo):

    file = hf_hub_download(

        repo_id=repo,

        filename="confusion_matrix.csv"

    )

    return pd.read_csv(
        file,
        index_col=0
    )
  """
=========================================================
LOAD TRAINING HISTORY
=========================================================
"""

def load_history(repo):

    file = hf_hub_download(

        repo_id=repo,

        filename="history.csv"

    )

    return pd.read_csv(file)
  """
=========================================================
ALL METRICS
=========================================================
"""

def get_all_metrics():

    rows = []

    for model,repo in MODEL_REPOS.items():

        metric = load_metrics(repo)

        rows.append({

            "Model":model,

            "Accuracy":metric["accuracy"],

            "Precision":metric["precision"],

            "Recall":metric["recall"],

            "F1 Score":metric["f1_score"],

            "Loss":metric["loss"]

        })

    return pd.DataFrame(rows)
  """
=========================================================
BEST MODEL
=========================================================
"""

def best_model(df):

    return df.sort_values(

        "F1 Score",

        ascending=False

    ).iloc[0]
  """
=========================================================
BAR CHART
=========================================================
"""

def metric_bar(df,column):

    fig = px.bar(

        df,

        x="Model",

        y=column,

        color="Model",

        text=df[column].round(4)

    )

    fig.update_layout(

        height=420,

        title=f"{column} Comparison"

    )

    return fig
  """
=========================================================
RADAR CHART
=========================================================
"""

def radar_chart(df):

    categories=[

        "Accuracy",

        "Precision",

        "Recall",

        "F1 Score"

    ]

    fig=go.Figure()

    for _,row in df.iterrows():

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

        height=600,

        polar=dict(

            radialaxis=dict(

                visible=True,

                range=[0,1]

            )

        )

    )

    return fig
  """
=========================================================
CONFUSION MATRIX
=========================================================
"""

def plot_confusion_matrix(df,title):

    fig = px.imshow(

        df,

        text_auto=True,

        aspect="auto",

        color_continuous_scale="Blues"

    )

    fig.update_layout(

        title=title,

        height=500

    )

    return fig
  """
=========================================================
TRAINING HISTORY
=========================================================
"""

def training_history_chart(df):

    fig = go.Figure()

    if "loss" in df.columns:

        fig.add_trace(

            go.Scatter(

                x=df["epoch"],

                y=df["loss"],

                name="Training Loss"

            )

        )

    if "eval_loss" in df.columns:

        fig.add_trace(

            go.Scatter(

                x=df["epoch"],

                y=df["eval_loss"],

                name="Validation Loss"

            )

        )

    fig.update_layout(

        title="Training History",

        height=450

    )

    return fig
