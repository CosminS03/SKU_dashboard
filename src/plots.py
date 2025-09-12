import config
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats.mstats import winsorize
import pandas as pd


def violin_plot(data: pd.Series, name: str):
    sns.violinplot(data=data, color=config.light_color_palette[1])
    plt.title(f"{name} Distribution")
    plt.show()


def winsorized_violin_plot(data: pd.Series, name: str):
    winsorized_data = winsorize(data, limits=[0.1, 0.1])
    sns.violinplot(data=winsorized_data, color=config.light_color_palette[1])
    plt.title(f"{name} Distribution")
    plt.show()
