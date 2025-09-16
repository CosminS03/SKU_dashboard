from src import config
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats.mstats import winsorize
import pandas as pd
from matplotlib.patches import Patch
from matplotlib.lines import Line2D


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

    sku_order = df["SKU"].to_list()

    fig, ax1 = plt.subplots()

    cutoff_mask = df["Cumulative"] <= 80
    palette = [
        config.light_color_palette[1] if c else config.dark_color_palette[2]
        for c in cutoff_mask
    ]

    sns.barplot(x="SKU", y=feature, data=df, ax=ax1, palette=palette, order=sku_order)
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
