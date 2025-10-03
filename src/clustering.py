from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import pandas as pd

df = pd.read_csv("./data/interim/sku_kpi.csv")

features = ["Rate_of_sale", "Revenue_contribution", "Units_per_transaction"]

scaler = StandardScaler()
features_std = scaler.fit_transform(df[features])

km = KMeans(n_clusters=3, random_state=10, n_init=100)
labels = km.fit_predict(features_std)
df["Cluster"] = labels

df.to_csv("./data/processed/clustered_kpis.csv", index=False)
