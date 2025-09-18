import pandas as pd

df = pd.read_csv("./data/interim/online_retail_transformed.csv")

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

df.to_csv("./data/interim/online_retail_no_outliers.csv", index=False)
