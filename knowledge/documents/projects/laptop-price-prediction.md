# Laptop Price Prediction — Machine Learning

## Overview
An end-to-end Machine Learning system that predicts laptop prices from hardware specifications using data preprocessing, feature engineering, Scikit-learn pipelines, and a Random Forest Regressor.

## Problem
Laptop prices vary significantly based on hardware specifications, making it difficult to estimate a fair market price manually.

## Solution
Developed a machine learning regression pipeline that preprocesses laptop specifications, engineers meaningful hardware features, and predicts laptop prices using Random Forest regression.

## Architecture
End-to-end machine learning architecture consisting of laptop specification preprocessing, feature engineering, exploratory analysis, categorical encoding through ColumnTransformer, Random Forest regression, model evaluation using R² and MAE, and Pickle-based model serialization.

## Technologies
- Python
- Pandas
- NumPy
- Scikit-learn
- Machine Learning
- Random Forest
- Regression
- Feature Engineering
- EDA
- Data Preprocessing

## Features
- Complete data preprocessing pipeline for cleaning and transforming raw laptop specifications.
- Feature engineering for display resolution, PPI, CPU categories, storage capacities, GPU brands, and operating systems.
- Exploratory Data Analysis covering company, laptop type, RAM, CPU, GPU, operating system, touchscreen, IPS display, and price relationships.
- Scikit-learn machine learning pipeline combining categorical feature transformation with a Random Forest Regressor.
- Serialized trained pipeline using Pickle, making the model ready for integration with Streamlit, Flask, or FastAPI applications.

## My Contribution
Built the complete ML workflow including data preprocessing, feature engineering, EDA, categorical transformation, Scikit-learn pipeline construction, Random Forest training, model evaluation, and model serialization.

## Challenges
- Handling inconsistent laptop specification formats such as RAM, weight, CPU, GPU, storage, and screen resolution.

## Results
- 100 Random Forest Estimators
- 15 Maximum Tree Depth
- 0.75 Feature Sampling
- High R² + Low MAE Evaluation Metrics

## Links
- **GitHub**: https://github.com/sAkhil2027/Laptop-Price-Prediction
- **Demo**: N/A
