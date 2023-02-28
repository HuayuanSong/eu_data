import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns

from .definitions import *

## Functions for plotting ##
def lin_reg_plt(df, x, y, model):
    """Create linear regression plot.

    Returns:
        plotly.graph_objects
    """
    if model == "lowess":
        trendline_options = dict(frac=0.6)
    else:
        trendline_options = None

    # Plotly scatter plot for the data points
    fig = px.scatter(
        df,
        x=x,
        y=y,
        trendline=model,
        height=400,
        trendline_options=trendline_options,
        hover_data=["region_name"],
        trendline_color_override=px.colors.qualitative.D3[3],
        color_discrete_sequence=px.colors.qualitative.D3,
    )

    fig.update_layout(
        plot_bgcolor="white",
        legend=dict(orientation="h", title=""),
        margin=dict(l=1, r=1, t=18, b=1, pad=1),
    )

    return fig


def box_plt(df, variable):
    """Create Plotly box plot.

    Returns:
        plotly.graph_objects
    """
    fig = px.box(
        df,
        x="EU Region",
        y=variable,
        points="all",
        color_discrete_sequence=px.colors.qualitative.D3,
        hover_data=["region_name"],
        notched=True,
        title="",
        color="EU Region",
        height=400,
    )

    fig.update_layout(
        margin=dict(l=1, r=1, t=23, b=1, pad=1),
        plot_bgcolor="white",
        showlegend=False,
        yaxis_title="",
        xaxis_title="",
    )
    return fig


def kde_plt(df, variable):
    """Create kernel density estimation plot.

    Returns:
        plotly.graph_objects
    """
    fig, ax = plt.subplots(figsize=(10, 6))

    ax.grid(False)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.get_yaxis().set_ticks([])

    sns.kdeplot(data=df, x=variable, fill=True, alpha=0.15, hue="EU Region", ax=ax)

    return fig


def corr_heatmap(df):
    """Create correlation heat map."""
    fig, ax = plt.subplots(figsize=(10, 8))

    sns.heatmap(df.corr().round(decimals=2), annot=True, ax=ax)

    return fig
