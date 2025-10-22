import pandas as pd


def closest_value(df: pd.DataFrame, value: int) -> int:
    diff = (df["Quantity"] - value).abs()
    return diff.idxmin()


def get_sample_ids(df: pd.DataFrame) -> set[int]:
    coef = int(int(len(df) / 10) / 5) + 1

    quants = {df.iloc[closest_value(df, df["Quantity"].quantile(0))]["SKU"]}
    for i in range(1, 5):
        for j in range(0, coef):
            quants.add(
                df.iloc[closest_value(df, df["Quantity"].quantile(0.25 * i)) - j]["SKU"]
            )

    return quants


def sampler(df: pd.DataFrame, merged: pd.DataFrame, cluster: str) -> pd.DataFrame:
    data = merged[merged["Performance"] == cluster]
    data = (
        data.groupby("SKU")["Quantity"]
        .sum()
        .reset_index()
        .sort_values(by="Quantity")
        .reset_index()
        .drop(columns="index")
    )
    df = df[df["SKU"].isin(get_sample_ids(data))]
    return df


df = pd.read_csv("./data/interim/online_retail_no_outliers.csv")
cl = pd.read_csv("./data/processed/clustered_kpis.csv")

merged = pd.merge(df, cl, on="SKU", how="inner")

sample = pd.concat(
    [sampler(df, merged, "Low"), sampler(df, merged, "Moderate")], ignore_index=True
)

sample = pd.concat([sample, sampler(df, merged, "High")], ignore_index=True)

sample.to_csv("./data/processed/sample.csv", index=False)
