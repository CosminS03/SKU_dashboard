import pandas as pd

df = pd.read_csv("./data/raw/online_retail.csv")

df["Description"] = df.groupby("StockCode")["Description"].transform(
    lambda x: x.ffill().bfill()
)
df["Description"] = df["Description"].fillna("No description")
df["CustomerID"] = df["CustomerID"].fillna("No account")

df.to_csv("./data/interim/online_retail_generally_cleaned.csv", index=False)
