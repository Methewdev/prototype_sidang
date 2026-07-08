"""
=========================================================
MODEL EVALUATION MODULE
=========================================================
"""

import json
import pandas as pd

from huggingface_hub import hf_hub_download

import plotly.express as px
import plotly.graph_objects as go


# =====================================================
# HUGGINGFACE MODEL REPOSITORY
# =====================================================

MODEL_REPOS = {

    "IndoBERT": "envidevelopment/livin-emotion-indobert",

    "mBERT": "envidevelopment/livin-emotion-mbert",

    "DeBERTa": "envidevelopment/livin-emotion-deberta"

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
# LOAD ALL METRICS
# =====================================================

def get_all_metrics():

    rows = []

    for model_name, repo in MODEL_REPOS.items():

        try:

            metric = load_metrics(repo)

            rows.append({

                "Model": model_name,

                "Accuracy": metric.get("accuracy", 0),

                "Precision": metric.get("precision", 0),

                "Recall": metric.get("recall", 0),

                "F1 Score": metric.get("f1_score", 0)

            })

        except Exception as e:

            print(f"{model_name} : {e}")

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

    ranking = df.sort_values(

        by="F1 Score",

        ascending=False

    ).reset_index(drop=True)

    ranking.insert(

        0,

        "Rank",

        range(1, len(ranking) + 1)

    )

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

        showlegend=False,

        xaxis_title="Model",

        yaxis_title=metric

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

        title="Overall Model Performance",

        height=550,

        polar=dict(

            radialaxis=dict(

                visible=True,

                range=[0,1]

            )

        )

    )

    return fig


# =====================================================
# SUMMARY
# =====================================================

def summary_model(df):

    best = best_model(df)

    if best is None:

        return "No evaluation result."

    return f"""
🏆 Best Model : {best['Model']}

Accuracy : {best['Accuracy']:.2%}

Precision : {best['Precision']:.2%}

Recall : {best['Recall']:.2%}

F1 Score : {best['F1 Score']:.2%}
"""
