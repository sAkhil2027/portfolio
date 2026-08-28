# Customer Churn Prediction & Lifetime Value ML Engine

## Overview
An end-to-end Machine Learning pipeline analyzing 25M+ customer transaction rows to predict subscription churn risk and calculate Customer Lifetime Value (CLV).

## Problem
High quarterly subscriber churn of 12% causing revenue leakage across 25M+ customer accounts without early warning signals.

## Solution
Built an automated XGBoost predictive ML pipeline that flags high-risk churn signals 30 days prior to cancellation and triggers retention offers with an 18% improvement in customer retention.

## Architecture
Employs feature engineering in Pandas/SQL, hyperparameter tuning with Optuna, experiment tracking with MLflow, XGBoost ensemble classification, SHAP model interpretability, and FastAPI microservice serving.

## Technologies
- Python
- Scikit-Learn
- XGBoost
- Pandas
- FastAPI
- Streamlit
- SQL
- Optuna
- MLflow

## Features
- Comprehensive Exploratory Data Analysis (EDA) uncovering key behavioral churn triggers.
- Feature engineering pipeline creating 45+ domain-specific metrics (recency, frequency, monetary value).
- SHAP (SHapley Additive exPlanations) model interpretability dashboard for executive decision making.
- Automated Streamlit interactive web application for marketing teams to run instant predictions.

## My Contribution
Architected the end-to-end ML pipeline, engineered 45+ domain features in Pandas/SQL, and integrated SHAP model interpretability.

## Challenges
- Handling class imbalance (9:1 non-churn ratio).
- Optimizing inference latency under 25ms for 500k daily predictions.

## Results
- 94.2% AUC-ROC Score
- 25M+ Records Analyzed
- 18% Churn Reduced
- < 25ms Inference Speed

## Links
- **GitHub**: https://github.com/akhil-data/customer-churn-ml
- **Demo**: https://churn-ml-demo.akhil.dev
