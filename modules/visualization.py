import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# =====================================================
# MISSING VALUE
# =====================================================

def missing_value_chart(df):

    missing = pd.DataFrame({

        "Column": df.columns,

        "Missing":

            df.isnull().sum().values

    })

    fig = px.bar(

        missing,

        x="Column",

        y="Missing",

        text="Missing",

        color="Missing"

    )

    fig.update_layout(

        title="Missing Value Distribution",

        xaxis_title="Column",

        yaxis_title="Total Missing",

        height=450

    )

    return fig
  # =====================================================
# RATING DISTRIBUTION
# =====================================================

def rating_distribution_chart(df):

    rating = (

        df["score"]

        .value_counts()

        .sort_index()

        .reset_index()

    )

    rating.columns = [

        "Rating",

        "Total"

    ]

    fig = px.bar(

        rating,

        x="Rating",

        y="Total",

        text="Total",

        color="Rating"

    )

    fig.update_layout(

        title="Rating Distribution",

        height=450

    )

    return fig
  # =====================================================
# REVIEW LENGTH
# =====================================================

def review_length_chart(df, text_column):

    data = df.copy()

    data["Review Length"] = (

        data[text_column]

        .fillna("")

        .astype(str)

        .str.split()

        .apply(len)

    )

    fig = px.histogram(

        data,

        x="Review Length",

        nbins=40

    )

    fig.update_layout(

        title="Review Length Distribution",

        height=450

    )

    return fig
  # =====================================================
# DUPLICATE
# =====================================================

def duplicate_chart(df):

    duplicate = int(df.duplicated().sum())

    unique = len(df) - duplicate

    fig = px.pie(

        names=[

            "Unique",

            "Duplicate"

        ],

        values=[

            unique,

            duplicate

        ],

        hole=0.45

    )

    fig.update_layout(

        title="Duplicate Distribution",

        height=450

    )

    return fig
