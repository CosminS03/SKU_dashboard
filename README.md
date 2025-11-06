# SKU Portfolio Evaluation Dashboard

## Overview

### Problem Statement
Stock Keeping Units(SKUs) are unique product identifiers used for sales and inventory tracking. Retiring underperforming SKUs helps reallocate resources, free capacity for innovation and align portfolios with consumer trends and brand strategies.
The usual process is slow and rigid: data is filtered by fixed KPI thresholds, reviewed separately by stakeholders and finalized in authority-driven meetings. This approach risks missing true underperformers, duplicates effort and can bias decisions.

### Solution Overview
A dashboard can centralize SKU evaluation, visualizing performance KPIs and using clustering techniques to group SKUs by performance level. This reduces reliance on rigid thresholds and provides a shared, unbiased view for all stakeholders, thus streamlining analysis and decision-making.

### Business Impact
A dashboard can accelerate evaluations, improve portfolio profitability and reduce operational complexity. Organizations using similar approaches have cut evaluation time by up to 75-80% and achieved revenue growth of ~8.6% year-over-year([Georgia Tech Capstone](https://capstone.isye.gatech.edu/research/coca-cola-portfolio-evaluation-process), [MetricsCart](https://metricscart.com/insights/sku-rationalization-in-e-commerce/)).

## Technical Documentation

### Dataset
The dataset used in this project comes from [Kaggle](https://www.kaggle.com/datasets/thedevastator/online-retail-sales-and-customer-data).
It includes eight columns:
| Column | Description |
| :--- | :--- |
| InvoiceNo | Transaction ID(IDs starting with "C" indicate purchases). |
| StockCode | Product identifier(renamed to SKU later). |
| Description | Short description of the product. |
| Quantity | Number of units per transaction. |
| InvoiceDate | Date of transaction. |
| UnitPrice | Price per product unit. |
| CustomerID | Unique customer or supplier ID. |
| Country | Country of origin or destination. |

### Methodology
#### Data Cleaning
The raw dataset contained missing values in the "Description" and "CustomerID" columns. When possible, missing descriptions were filled using values from other rows with the same SKU, otherwise, they were replaced with "No description". The same approach was applied to "CustomerID", substituting missing entries with "No account".<br>
The "StockCode" column was renamed to SKU to align with the project terminology and transactions with negative quantities that were not labeled as purchases, unit prices equal to zero or non-numeric SKU codes were removed, as they represented adjustments or invalid records. Similarly, rows with lowercase descriptions were excluded for consistency.<br>
Outliers were identified and removed using the interquartile range method, meaning that values beyond Q1 - 1.5 * (Q3-Q1) and Q3 + 1.5 * (Q3-Q1) were excluded. Additionally, SKUs with only one unit sold or with a sell-through rate above 100% were dropped, as such entries reflected data inconsistencies.

#### KPI Calculation
All KPIs used were calculated at the SKU level:<br>
Revenue Contribution = SKU revenue / total revenue <br>
Sales Contribution = SKU units sold / total units sold <br>
Sell-Through Rate = SKU units sold / SKU units purchased <br>
Rate of Sale = SKU units sold / number of weeks in the period of calculation <br>
Gross Margin = (SKU revenue - SKU costs) / SKU revenue <br>
Units per Transaction = SKU units sold / total number of transactions <br>

These KPIs fall into three categories:
- Efficiency: Sell-Through Rate, Rate of Sale.
- Profitability: Revenue Contribution, Gross Margin.
- Sales behavior: Sales Contribution, Units per Transaction.

One KPI from each category(Rate of Sale, Revenue Contribution and Units per Transaction) were standardized and used for clustering.

#### Clustering
Before clustering
![Data before clustering](notebooks/markdown/0.1-clustering_files/0.1-clustering_4_0.png)

After clustering
![Data after clustering](notebooks/markdown/0.1-clustering_files/0.1-clustering_8_0.png)

K-Means clustering was applied to group SKUs by performance.
| Cluster | Color | Label |
| :--- | :--- | :--- |
| 0 | Red | Low |
| 1 | Blue | High |
| 2 | Yellow | Moderate |

Low-performing SKUs consistently show lower median values than the global medians for rate of sale, revenue contribution and units per transaction, confirming their potential for retirement.

#### Sampling
Given the large number of SKUs in the dataset and the limited space available on the dashboard, a smaller representative sample was created to ensure that the Pareto and Revenue Composition charts remain readable while still reflecting the original data distribution.
A custom sampling method was designed to preserve the statistical shape of the dataset by prioritizing values near key quantiles. The process began by ordering SKUs according to their total sales and dividing them into three subsets corresponding to their performance clusters.
For each subset, the number of values to include around each quantile was determined using the following formula:
```
N = int(int(len(subset) / 10) / 5) + 1
```
This ensures that the resulting sample is approximately ten times smaller than the original dataset while maintaining representation across all five quartiles. The final sampled dataset includes the quantile points themselves and the N observations preceding Q1, Q2, Q3 and Q4.

#### Dashboard
The final outcome of this project is an interactive Tableau dashboard:
![Dashboard](images/Dashboard.png)

The dashboard consists of four visualizations and three sets of interactive buttons. The buttons in the top-left corner allow users to filter SKUs by the performance cluster. When all buttons are selected, all SKUs are displayed. Deselecting a button hides the SKUs in that cluster from all charts.

The two upper charts use color coding to distinguish SKU clusters: blue for High, yellow for Moderate and red for Low performers. Both are based on the sample dataset, ensuring readability while maintaining the overall distribution of the original data.

The Pareto Chart(upper-left) illustrates the Pareto principle in SKU performance. Each bar represents the selected measure(Revenue or Sales), ordered from highest to lowest, while the black line shows the running total of that measure. The buttons beside the chart let the users toggle between the two metrics.

The Revenue Composition chart(upper-right) is a stacked bar chart ranking SKUs from highest to lowest revenue. Each bar is divided into Profit and Cost sections, providing a clear breakdown of each SKU's revenue composition.

The KPI Distribution Chart(lower-left) visualizes the distribution of three key metrics through a bar chart, namely: Rate of Sale(ROS), Sell-Through Rate(STR) and Units per Transaction(UPT). The buttons beside the chart allow users to switch between KPIs, displaying one distribution at a time.

The Clustering Chart(lower-right) provides a clear view of SKU groupings and their performance patterns. It is a two-dimensional scatter plot with Units per Transaction on the X-axis and Revenue Contribution on the Y-axis, while Rate of Sale is represented by a color gradient ranging from white(low values) to blue(high values).

The full interactive dashboard is available on [Tableau Public](https://public.tableau.com/app/profile/cosmin.spanu/viz/SKU_17623529562380/SKUDashboard).

## Demo Guide
The code in this repository allows users to reproduce the dataset used in this project in any of its processing stages. To run the project, ensure that Python 3.12.2 is installed for executing scripts and managing dependencies through pip. On Windows, installing Chocolatey si recommended to enable the use of Makefile commands.

Additionally, Git is required to clone the repository and a Kaggle API key must be stored as an enviroment variable named KAGGLE_API_KEY within a .env file to enable automatic dataset download.

To begin, clone the repository and navigate into the project directory:
```
git clone https://github.com/CosminS03/SKU_dashboard.git
cd SKU_dashboard
```

Next, install all required libraries:
```
pip install -r requirements.txt
```

Once the enviroment is set up, users can generate the fully processed dataset by running:
```
make all
```

This command executes all steps defined in the Makefile. If preferred, each step can also be executed independently:
| Command | Description |
| :--- | :--- |
| make prepare | Creates the data directory containing raw, interim and processed folders. |
| make download | Downloads the raw dataset from Kaggle and saves it as online_retail.csv in the raw directory |
| make clean | Fills missing values and saves online_retail_generally_cleaned.csv in the interim directory |
| make delete | Removes invalid or irrelevant data and saves online_retail_transformed.csv in the interim directory |
| make outlier | Filters outliers and saves online_retail_no_outliers.csv in the interim directory |
| make features | Calculates all KPIs and stores sku_kpi.csv in the interim directory |
| make cluster | Performs clustering and saves clustered_kpis.csv in the processed directory |
| make sample | Creates a smaller version of the final dataset and saves sample.csv into the processed directory
| make cleanup | Removes temporary folders(raw and interim) to clean up the workspace |     