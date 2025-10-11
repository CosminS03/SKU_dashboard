import pandas as pd

df = pd.read_csv("./data/interim/online_retail_generally_cleaned.csv")
df.drop(columns=["index"], inplace=True)

negative_quant = df["Quantity"] < 0
non_purchase_invoice = ~df["InvoiceNo"].str.startswith("C")
neg_non_purchase_invoice = negative_quant & non_purchase_invoice

prices_zero = df["UnitPrice"] == 0
"""
letters_only_stock_code = df["StockCode"].str.contains(r"^[a-zA-Z]+$")
numbers_only_stock_code = df["StockCode"].str.contains(r"^[0-9]+$")
letters_numbers_stock_code = df["StockCode"].str.contains(
    r"^(?=.*[a-zA-Z])(?=.*[0-9])[a-zA-Z0-9]+$"
)
sym_stock_code = ~(
    letters_only_stock_code | numbers_only_stock_code | letters_numbers_stock_code
)
"""
not_only_numbers_stock_code = ~(df["StockCode"].str.contains(r"^[0-9]+$"))
lower_description = ~(df["Description"].str.isupper())
"""
match_mask = (
    neg_non_purchase_invoice
    | prices_zero
    | letters_only_stock_code
    | letters_numbers_stock_code
    | sym_stock_code
    | lower_description
)
"""
match_mask = (
    neg_non_purchase_invoice
    | prices_zero
    | not_only_numbers_stock_code
    | lower_description
)
rows_to_delete = df[match_mask].index
df.drop(rows_to_delete, inplace=True)

df.rename(columns={"StockCode": "SKU"}, inplace=True)

df.to_csv("./data/interim/online_retail_transformed.csv", index=False)
