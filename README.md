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

### KPIs used
In the creation of this project several KPIs were calculated. All of them were calculated at the SKU level, not globally.
Revenue contribution represents 