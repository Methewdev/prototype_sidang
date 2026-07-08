
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

            rows.append({

                "Model": model_name,

                "Accuracy": None,

                "Precision": None,

                "Recall": None,

                "F1 Score": None

            })

            print(f"{model_name} : {e}")

    return pd.DataFrame(rows)
  

    return summary
