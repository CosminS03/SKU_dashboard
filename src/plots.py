from src import config
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats.mstats import winsorize
import pandas as pd
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
import plotly.graph_objects as go


def violin_plot(data: pd.Series, name: str):
    sns.violinplot(data=data, color=config.light_color_palette[1])
    plt.title(f"{name} Distribution")
    plt.show()


def winsorized_violin_plot(
    data: pd.Series, name: str, lowerPerc: float, upperPerc: float
):
    winsorized_data = winsorize(data, limits=[lowerPerc, upperPerc])
    sns.violinplot(data=winsorized_data, color=config.light_color_palette[1])
    plt.title(f"{name} Distribution")
    plt.show()


def percent_of_total_plot(data: pd.DataFrame, feature: str, title: str):
    df = (
        data[~data["InvoiceNo"].str.startswith("C")]
        .groupby("SKU")[feature]
        .sum()
        .reset_index()
    )
    df = df.sort_values(by=feature, ascending=False).reset_index()

    df["Cumulative"] = df[feature].cumsum() / df[feature].sum() * 100

    fig, ax1 = plt.subplots()

    cutoff_mask = df["Cumulative"] <= 80
    palette = [
        config.light_color_palette[1] if c else config.dark_color_palette[2]
        for c in cutoff_mask
    ]

    ax1.bar(x=df.index, height=df[feature], width=1.0, color=palette)
    ax1.set_ylabel("")
    ax1.set_xlabel("")
    ax1.set_xticks([])

    ax2 = ax1.twinx()
    ax2.plot(df.index, df["Cumulative"], color=config.light_color_palette[0])
    ax2.set_ylim(0, 110)
    ax2.axhline(80, color="gray", linestyle="--")
    ax2.set_ylabel("")

    highlight_patch = Patch(color=config.light_color_palette[1], label="SKUs <= 80%")
    others_patch = Patch(color=config.dark_color_palette[2], label="SKUs > 80%")
    cumulative_line = Line2D(
        [0],
        [0],
        color=config.light_color_palette[0],
        linestyle="-",
        label="Cumulative %",
    )
    threshold_line = Line2D(
        [0], [0], color="gray", linestyle="--", label="80% threshold"
    )

    ax1.legend(
        handles=[highlight_patch, others_patch, cumulative_line, threshold_line],
        loc="center right",
        frameon=True,
    )

    plt.title(f"{title} Pareto chart")
    plt.show()


def waterfall_plot(df: pd.DataFrame, sales: bool):
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
    df["Month"] = df["InvoiceDate"].dt.strftime("%Y-%m")

    if sales:
        waterfall = (
            df[~df["InvoiceNo"].str.startswith("C")]
            .groupby(by="Month")["Quantity"]
            .sum()
        )
    else:
        waterfall = (
            df[df["InvoiceNo"].str.startswith("C")]
            .groupby(by="Month")["Quantity"]
            .sum()
            .abs()
        )

    waterfall = waterfall.reset_index()
    waterfall["Measure"] = "relative"
    waterfall = waterfall.sort_values(by="Month")
    waterfall["Measure"].iloc[-1] = "total"

    fig = go.Figure(
        go.Waterfall(
            name="Cash flow plot",
            orientation="v",
            x=waterfall["Month"],
            y=waterfall["Quantity"],
            measure=waterfall["Measure"],
        )
    )

    if sales:
        fig.update_layout(title="Cash Inflows")

        fig.update_traces(
            increasing=dict(marker=dict(color=config.light_color_palette[4])),
            totals=dict(marker=dict(color=config.dark_color_palette[2])),
        )

        fig.show()
    else:
        fig.update_layout(title="Cash Outflows")

        fig.update_traces(
            increasing=dict(marker=dict(color=config.light_color_palette[3])),
            totals=dict(marker=dict(color=config.dark_color_palette[3])),
        )

        fig.show()


def ros_distribution(data: pd.Series):
    sns.kdeplot(
        data=data,
        fill=True,
        linewidth=2,
        color=config.light_color_palette[4],
        alpha=0.6,
        bw_adjust=0.6,
    )

    plt.title("Rate of Sale Distribution")
    plt.grid(True, linestyle="--", alpha=0.6)

    plt.show()
