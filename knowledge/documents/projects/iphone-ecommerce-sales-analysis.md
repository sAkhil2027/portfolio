# iPhone E-Commerce Sales Analysis — EDA & Business Insights

## Overview
An end-to-end Exploratory Data Analysis (EDA) project on Indian iPhone e-commerce data using Python, Pandas, Matplotlib, and Seaborn to uncover product demand, pricing patterns, platform behavior, geographic trends, and purchasing patterns.

## Problem
E-commerce product data contains multiple dimensions such as model, storage, color, platform, location, date, and price, making it difficult to identify meaningful demand patterns.

## Solution
Built a comprehensive EDA pipeline that cleans and transforms raw iPhone e-commerce data into structured product, geographic, platform, and temporal features.

## Architecture
End-to-end exploratory analytics architecture consisting of raw e-commerce data ingestion, data-quality inspection, redundant-column removal, missing-location handling, date transformation, regex-based product feature extraction, Pandas aggregation, platform and geographic analysis, temporal analysis, product-level pricing analysis, and Matplotlib/Seaborn visualization.

## Technologies
- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- EDA
- Data Analysis
- Feature Engineering
- Pricing Analysis
- E-Commerce Analytics

## Features
- Comprehensive data-quality analysis identifying empty, low-variation, redundant, and identifier columns along with duplicate records.
- Temporal feature engineering from transaction dates including year, month, month name, day of month, day name, weekend flag, and quarter.
- Product feature extraction using regular expressions to derive iPhone model, generation, storage capacity, and color from product names.
- Platform-level pricing analysis comparing Amazon, Flipkart, and JioMart using record volume and price distributions.

## My Contribution
Performed the complete data analysis workflow including data cleaning, missing-value handling, duplicate investigation, date feature engineering, product attribute extraction, platform comparison, geographic analysis, seasonality analysis, pricing analysis, aggregation, and business-oriented visualization.

## Challenges
- Handling inconsistent product names while extracting model, generation, storage, and color attributes.

## Results
- 5,843 Dataset Records
- 151 Unique Products
- 3 E-Commerce Platforms
- 347 Unique Dates

## Links
- **GitHub**: https://github.com/sAkhil2027/iphone_dataset_analysis
- **Demo**: N/A
