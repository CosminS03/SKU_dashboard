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
The dataset used in this project was taken from kaggle. The following URL links towards the dataset: 
https://www.kaggle.com/datasets/thedevastator/online-retail-sales-and-customer-data
The dataset consists of 8 columns: InvoiceNo, StockCode, Description, Quantity, InvoiceDate, UnitPrice, CustomerID, Country.
InvoiceNo is the id of the transaction. It can be of two types: sales transaction or acquire transaction. The latter has IDs starting with the letter 'C'.
StockCode is the ID of products which is why it has been changed to 'SKU' in the analysis.
Description is a short description of the product.
Quantity is the numeric value of the quantity of the product involved in the transaction.
InvoiceDate is the date when the transaction took place.
UnitPrice is the numeric value of the price of one unit of the product involved in the transaction.
CustomerID is the unique ID of the purchaser/supplier.
Country is the name of the country that the product was shipped to or ordered from.
The data contains more selling transactions than acquisitions and as a consequence the final dashboard will depict a lot of great performing SKUs.

### KPIs used
In the creation of this project several KPIs were calculated. All of them were calculated at the SKU level, not globally.
Revenue contribution represents the percentage of the total revenue that can be attributed to the specific SKU.
Sales Contribution represents the percentage of the total units sold that can be attributed to the specific SKU.
Sell through rate measures the amount of inventory sold in a given period of time relative to the amount of inventory received in that same period. In other words, this KPI measures how quickly that specific SKU can be turned into revenue.
Rate of sale represents the total of units sold of a specific SKU in a period of time divided by the number of a subsection found in that period. In the case of this project, the number of weeks for the entire dataset was used. 
Gross margin represents the percentage of the total revenue that was translated into profit, before taxes.
Units per transaction measures the average number of units of a SKU that is sold in any given transaction.
These KPIs can be grouped into 3 categories: efficiency(sell through rate, rate of sale), profitability(revenue contribution, gross margin) and sales behavior(sales contribution, units per transaction).

### Methodology
1. Data cleaning
The raw dataset contained null values in the "Description" and "CustomerID" columns. Where possible, the missing values from the "Description" column have been filled with the values present in a differenct row that had the same "StockCode" value. In the case of descriptions that had no other rows with the same stock code and a non-null value, the "No description" sentence was used to fill the gap. The same approach was taken in the case of CustomerID, filling the missing values with "No account".
In the dataset there is also information describing transactions with a negative quantity that were not registered as acquisitions and thus, these rows were removed.
Transactions with a unit price of 0 were also removed, as they constituted accounting adjustments, which are not the concern of this project. This was also the case of rows with Stock Codes that were not formed form only numbers and rows with descriptions written in lower case.
The "StockCode" was changed to be called "SKU" in order to be consistent with the title of the project.
Another set of rows that were removed were the ones that contained outliers in the "Quantity" and "UnitPrice" columns. The outliers were the values higher than Q3 + 1.5 * IQR and the ones lower than Q1 - 1.5 * IQR, where Q1 is the first quartile, Q3 is the third quartile and IQR(InterQuartile Range) is Q3 - Q1.
Due to the skewness of some KPIs, SKUs that have sum of total units sold equal to one, were erase. As well as SKUs with a sell through rate of more than 100% since it is impossible to sell more than the available inventory.

2. KPI calculation
The KPIs mentioned above were calculated with the following formulas:
Revenue contribution: total revenue generated by the SKU / total global revenue
Sales contribution: total number of units of the SKU sold / total sales
Sell through rate: number of units of the SKU sold / number of units of the SKU received
Rate of sale: total number of units of the SKU sold / number of weeks in the period of sale
Gross margin: (total revenue generated by the SKU - total sum of units bought of that SKU) / total revenue generated by the SKU
Units per transaction: total bnumber of units of the SKU sold / total number of transactions.
Out of these KPIs three, one from each category, were chosen to train the clustering algorithm: rate of sale, revenue contribution and units per transaction.
These 3 features were standardized so that all of them have a mean of 0 and a standard deviation of 1. This was done so that features with higher values would not skew the clustering.

3. Clustering
The algorithm used in this project was K-Means. Below there are visualizations of the data before and after clustering.
Before:
![Data before clustering](notebooks/markdown/0.1-clustering_files/0.1-clustering_4_0.png)

After:
![Data after clustering](notebooks/markdown/0.1-clustering_files/0.1-clustering_8_0.png)
As evident from the images, the data was grouped into 3 clusters annotated based on performance as follows: "Low"(Red), "Moderate"(Yellow) and "High"(Blue).
Looking at the descriptive statistics of each cluster we can see that the low performers have a lower median values than the global ones for the Rate of sale and Revenue contribution KPIs, while the median is equal to the global one in the case of Units per transaction. The low performers are the main candidates for retiring.