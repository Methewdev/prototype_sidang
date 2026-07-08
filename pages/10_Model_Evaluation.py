import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Model Evaluation",
    page_icon="🏆",
    layout="wide"
)

st.title("🏆 Model Evaluation")

# Data hasil evaluasi
df = pd.DataFrame({
    "Model": ["IndoBERT", "mBERT", "DeBERTa"],
    "Accuracy": [86.43, 84.78, 83.15],
    "Precision": [86.85, 84.92, 83.42],
    "Recall": [86.43, 84.78, 83.15],
    "F1 Score": [86.46, 84.81, 83.20]
})

st.subheader("Performance Comparison")
st.dataframe(df, use_container_width=True)

col1, col2 = st.columns(2)

with col1:
    fig = px.bar(
        df,
        x="Model",
        y="Accuracy",
        color="Model",
        text="Accuracy",
        title="Accuracy Comparison"
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig = px.bar(
        df,
        x="Model",
        y="F1 Score",
        color="Model",
        text="F1 Score",
        title="F1 Score Comparison"
    )
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Evaluation Metrics")
st.table(df)

best = df.sort_values("F1 Score", ascending=False).iloc[0]

st.success(
    f"""
Model terbaik adalah **{best['Model']}**
dengan Accuracy **{best['Accuracy']:.2f}%**
dan F1 Score **{best['F1 Score']:.2f}%**.
"""
)
