import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns

from .definitions import *

## Functions for plotting ##


def create_line(df, columns):
    """Create Plotly graph line.

    Returns:
        plotly.graph_objects
    """
    fig = px.line(
        data_frame=df,
        x="time",
        y=columns,
        line_shape="linear",
        render_mode="svg",
        color_discrete_sequence=px.colors.qualitative.D3,
    )

    hovertemplate = "%{x|%d/%m/%Y} <br>%{y:,.2f}"
    fig.update_traces(hovertemplate=hovertemplate)
    fig.update_traces(line_width=3)
    fig.update_layout(
        xaxis_title="",
        yaxis_title="",
        height=400,
        plot_bgcolor="white",
        legend=dict(orientation="h", title=""),
        margin=dict(l=22, r=1, t=18, b=1, pad=1),
    )
    fig.update_yaxes(automargin=False)

    return fig


def create_bar(df, columns):
    """Create Plotly bar plot.

    Returns:
        plotly.graph_objects
    """
    fig = px.bar(
        data_frame=df[-60:],
        x="time",
        y=columns,
        color_discrete_sequence=px.colors.qualitative.D3,
    )

    hovertemplate = "%{x|%d/%m/%Y} <br>%{y:,.2f}"
    fig.update_traces(hovertemplate=hovertemplate)
    fig.update_layout(
        xaxis_title="",
        yaxis_title="",
        height=400,
        plot_bgcolor="white",
        margin=dict(l=26, r=1, t=18, b=1, pad=1),
    )
    fig.update_yaxes(automargin=False)

    return fig


def create_figure(df, dict_selection):
    plot_type = dict_selection["plot_type"]
    columns = dict_selection["columns"]

    if plot_type == "line":
        fig = create_line(df, columns)

    elif plot_type == "bar":
        fig = create_bar(df, columns)

    return fig


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
