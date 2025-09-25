import pandas as pd
import numpy as np
from src import config as cfg


def calc_units(df: pd.DataFrame, year: int, sold: bool):
    if sold:
        return (
            df[df["InvoiceDate"].dt.year == year][~df["InvoiceNo"].str.startswith("C")]
            .groupby(by="SKU")["Quantity"]
            .sum()
            .reset_index()
        )
    else:
        return (
            df[df["InvoiceDate"].dt.year == year][df["InvoiceNo"].str.startswith("C")]
            .groupby(by="SKU")["Quantity"]
            .sum()
            .abs()
            .reset_index()
        )


df = pd.read_csv("./data/interim/online_retail_transformed.csv")

# SKUs with the Quantity and UnitPrice values higher than Q3+1.5*IQR or lower than Q1-1.5*IQR

outliers = {}

for i, col in enumerate(["Quantity", "UnitPrice"]):
    upper_limit = df[col].quantile(0.75) + 1.5 * (
        df[col].quantile(0.75) - df[col].quantile(0.25)
    )
    lower_limit = df[col].quantile(0.25) - 1.5 * (
        df[col].quantile(0.75) - df[col].quantile(0.25)
    )

    outliers[i] = (df[col] > upper_limit) | (df[col] < lower_limit)

rows_to_delete = df[outliers[0] | outliers[1]].index

df.drop(rows_to_delete, inplace=True)

# SKUs with a sell through rate bigger than 100%

df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

units_sold_2010 = calc_units(df, 2010, True)
units_bought_2010 = calc_units(df, 2010, False)
units_sold_2011 = calc_units(df, 2011, True)
units_bought_2011 = calc_units(df, 2011, False)

df_str_2010 = pd.merge(
    units_sold_2010,
    units_bought_2010,
    on="SKU",
    how="outer",
    suffixes=["_sold", "_bought"],
)
df_str_2011 = pd.merge(
    units_sold_2011,
    units_bought_2011,
    on="SKU",
    how="outer",
    suffixes=["_sold", "_bought"],
)

df_str_2010 = df_str_2010.fillna(0)
df_str_2011 = df_str_2011.fillna(0)

df_str_2010["Sell_through_rate"] = (
    df_str_2010["Quantity_sold"] / df_str_2010["Quantity_bought"]
) * 100
df_str_2011["Sell_through_rate"] = (
    df_str_2011["Quantity_sold"] / df_str_2011["Quantity_bought"]
) * 100

df_str_2010["Sell_through_rate"] = df_str_2010["Sell_through_rate"].replace(
    [np.inf, -np.inf], 0
)
df_str_2011["Sell_through_rate"] = df_str_2011["Sell_through_rate"].replace(
    [np.inf, -np.inf], 0
)

df_str = pd.merge(
    df_str_2010, df_str_2011, on="SKU", how="outer", suffixes=["_10", "_11"]
)

df_str = df_str.fillna(0)

df_str["Sell_through_rate"] = (
    cfg.wght_2010 * df_str["Sell_through_rate_10"]
    + cfg.wght_2011 * df_str["Sell_through_rate_11"]
)

skus_to_delete = set(df_str[df_str["Sell_through_rate"] > 100]["SKU"].to_list())

# SKUs that have the total sum of sold units equal to 1

sku_sum = (
    df[~df["InvoiceNo"].str.startswith("C")]
    .groupby(by="SKU")["Quantity"]
    .sum()
    .reset_index()
)

skus_to_delete = skus_to_delete | set(
    sku_sum[sku_sum["Quantity"] == 1]["SKU"].to_list()
)

df = df[~df["SKU"].isin(skus_to_delete)]

df.to_csv("./data/interim/online_retail_no_outliers.csv", index=False)
