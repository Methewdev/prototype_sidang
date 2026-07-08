import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sklearn.metrics import (
    accuracy_score,
    precision_recall_fscore_support,
    confusion_matrix,
    classification_report
)

#====================================================
# HITUNG METRIK
#====================================================

def evaluate_model(y_true, y_pred):

    acc = accuracy_score(y_true, y_pred)

    precision, recall, f1, _ = precision_recall_fscore_support(
        y_true,
        y_pred,
        average="weighted"
    )

    return {
        "Accuracy": acc,
        "Precision": precision,
        "Recall": recall,
        "F1 Score": f1
    }


#====================================================
# DATAFRAME METRIK
#====================================================

def metric_dataframe(results):

    df = pd.DataFrame(results).T

    df = df.reset_index()

    df.columns = [
        "Model",
        "Accuracy",
        "Precision",
        "Recall",
        "F1 Score"
    ]

    return df


#====================================================
# CONFUSION MATRIX
#====================================================

def get_confusion_matrix(y_true, y_pred):

    return confusion_matrix(y_true, y_pred)


#====================================================
# CLASSIFICATION REPORT
#====================================================

def get_classification_report(y_true, y_pred):

    report = classification_report(
        y_true,
        y_pred,
        output_dict=True
    )

    return pd.DataFrame(report).transpose()


#====================================================
# BAR CHART
#====================================================

def metric_bar(df, metric):

    fig = px.bar(
        df,
        x="Model",
        y=metric,
        color="Model",
        text=df[metric].round(4),
        title=f"{metric} Comparison"
    )

    fig.update_layout(height=500)

    return fig


#====================================================
# RADAR CHART
#====================================================

def radar_chart(df):

    categories = [
        "Accuracy",
        "Precision",
        "Recall",
        "F1 Score"
    ]

    fig = go.Figure()

    for i in range(len(df)):

        fig.add_trace(go.Scatterpolar(

            r=[
                df.iloc[i]["Accuracy"],
                df.iloc[i]["Precision"],
                df.iloc[i]["Recall"],
                df.iloc[i]["F1 Score"]
            ],

            theta=categories,

            fill="toself",

            name=df.iloc[i]["Model"]

        ))

    fig.update_layout(

        polar=dict(radialaxis=dict(visible=True, range=[0,1])),

        height=600

    )

    return fig
