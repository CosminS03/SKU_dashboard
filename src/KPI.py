import config as cfg
import pandas as pd
import numpy as np


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


df = pd.read_csv(
    "./data/interim/online_retail_no_outliers.csv", dtype={"InvoiceNo": str}
)

df["Revenue"] = round(df["Quantity"] * df["UnitPrice"], 2)
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

# Revenue contribution

rev_prct = (
    df[~df["InvoiceNo"].str.startswith("C")]
    .groupby(by="SKU")["Revenue"]
    .sum()
    .reset_index()
)

rev_prct["Revenue_contribution"] = round(
    rev_prct["Revenue"] / rev_prct["Revenue"].sum() * 100, 2
)

rev_prct = rev_prct.drop(columns=["Revenue"])

# Sales contribution

sls_prct = (
    df[~df["InvoiceNo"].str.startswith("C")]
    .groupby(by="SKU")["Quantity"]
    .sum()
    .reset_index()
)

sls_prct["Sales_contribution"] = round(
    sls_prct["Quantity"] / sls_prct["Quantity"].sum() * 100, 2
)

sls_prct = sls_prct.drop(columns=["Quantity"])

sku_df = pd.merge(rev_prct, sls_prct, on="SKU", how="outer")

# Sell through rate

units_sold_10 = calc_units(df, 2010, True)
units_bought_10 = calc_units(df, 2010, False)
units_sold_11 = calc_units(df, 2011, True)
units_bought_11 = calc_units(df, 2011, False)

str_2010 = pd.merge(
    units_sold_10, units_bought_10, on="SKU", how="outer", suffixes=["_sold", "_bought"]
)

str_2010 = str_2010.fillna(0)
str_2010["Sell_through_rate"] = (
    str_2010["Quantity_sold"] / str_2010["Quantity_bought"] * 100
)
str_2010["Sell_through_rate"] = str_2010["Sell_through_rate"].replace(
    [np.inf, -np.inf], 0
)

str_2011 = pd.merge(
    units_sold_11, units_bought_11, on="SKU", how="outer", suffixes=["_sold", "_bought"]
)

str_2011 = str_2011.fillna(0)
str_2011["Sell_through_rate"] = (
    str_2011["Quantity_sold"] / str_2011["Quantity_bought"] * 100
)
str_2011["Sell_through_rate"] = str_2011["Sell_through_rate"].replace(
    [np.inf, -np.inf], 0
)

STR = pd.merge(str_2010, str_2011, on="SKU", how="outer", suffixes=["_10", "_11"])
STR = STR.fillna(0)
STR["Sell_through_rate"] = (
    STR["Sell_through_rate_10"] * cfg.wght_2010
    + STR["Sell_through_rate_11"] * cfg.wght_2011
)

STR = STR.drop(
    columns=[
        "Quantity_sold_10",
        "Quantity_bought_10",
        "Sell_through_rate_10",
        "Quantity_sold_11",
        "Quantity_bought_11",
        "Sell_through_rate_11",
    ]
)

sku_df = pd.merge(sku_df, STR, on="SKU", how="outer")

# Rate of sale

ros = (
    df[~df["InvoiceNo"].str.startswith("C")]
    .groupby(by="SKU")["Quantity"]
    .sum()
    .reset_index()
)

date_span = df["InvoiceDate"].max() - df["InvoiceDate"].min()
no_weeks = date_span.days / 7

ros["Rate_of_sale"] = round(ros["Quantity"] / no_weeks, 2)

ros = ros.drop(columns=["Quantity"])

sku_df = pd.merge(sku_df, ros, on="SKU", how="outer")

# Gross margin

gross_profit = df.groupby(by="SKU")["Revenue"].sum().reset_index()
gross_profit = gross_profit.rename(columns={"Revenue": "Gross_profit"})
total_revenue = (
    df[~df["InvoiceNo"].str.startswith("C")]
    .groupby(by="SKU")["Revenue"]
    .sum()
    .reset_index()
)
total_revenue = total_revenue.rename(columns={"Revenue": "Total_revenue"})

gross_margin = pd.merge(gross_profit, total_revenue, on="SKU", how="outer")
gross_margin = gross_margin.fillna(0)
gross_margin["Gross_margin"] = round(
    gross_margin["Gross_profit"] / gross_margin["Total_revenue"] * 100, 2
)
gross_margin = gross_margin.replace([np.inf, -np.inf], 0)

gross_margin = gross_margin.drop(columns=["Gross_profit", "Total_revenue"])

sku_df = pd.merge(sku_df, gross_margin, on="SKU", how="outer")

# Units per transaction

total_transactions = df["InvoiceNo"].nunique()

upt = (
    df[~df["InvoiceNo"].str.startswith("C")]
    .groupby(by="SKU")["Quantity"]
    .sum()
    .reset_index()
)
upt["Units_per_transaction"] = round(upt["Quantity"] / total_transactions, 2)

upt = upt.drop(columns=["Quantity"])

sku_df = pd.merge(sku_df, upt, on="SKU", how="outer")

# SKU Description
sku_description = (
    df[["SKU", "Description"]]
    .drop_duplicates(subset=["SKU", "Description"])
    .groupby(by="SKU")["Description"]
    .first()
    .reset_index()
)

sku_df = pd.merge(sku_df, sku_description, on="SKU", how="left")
sku_df = sku_df.fillna(0)

sku_df.to_csv("./data/interim/sku_kpi.csv", index=False)
