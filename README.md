NYC Airbnb Price Prediction Pipeline 

This project implements an end-to-end Machine Learning pipeline to predict short-term rental prices in NYC using MLflow, Hydra, and Weights & Biases. 

Project Overview
The goal is to build a reproducible, traceable pipeline that can handle new data updates weekly. The pipeline includes data cleaning, automated testing, hyperparameter optimization, and model deployment (aliasing).
<img width="1446" height="415" alt="image" src="https://github.com/user-attachments/assets/1bcc8cda-a509-45b1-9370-2246bd057a70" />
<img width="1673" height="680" alt="image" src="https://github.com/user-attachments/assets/3f135661-5cc4-4bc8-af7d-1a920497349c" />


Pipeline Steps
The pipeline consists of the following modular steps:
1. Download Data: Fetches the raw dataset from W&B.
2. Basic Cleaning: Removes outliers, handles missing values, and filters coordinates outside NYC boundaries.
3. Data Check: Runs automated tests (Pytest) to ensure data integrity and detect drift.
4. Data Splitting: Segregates data into training/validation and test sets.
5. Train Random Forest: Trains a regression model with automated logging of metrics and artifacts.
6. Test: Evaluates the production-ready model on the unseen test set.

Final Results
After optimizing the model using a grid search (15 runs), the best model was selected based on the lowest Mean Absolute Error (MAE).

Best R² Score: 0.58
Best MAE: 32.45
Model Version: v7 (as prod)

How to Run
To reproduce the results or run the pipeline on new data, follow these steps:
1. Setup Environment
conda env create -f environment.yml
conda activate nyc_airbnb_dev
2. Execute the Entire Pipeline
To run all steps using the default configuration:
mlflow run .
3. Run on New Data Sample (e.g., sample2.csv)
To test the pipeline's robustness against new data:
mlflow run . -P hydra_options="etl.sample='sample2.csv'"

Releases 
v1.0.0: Initial stable release (caught geographical outliers).
v1.0.1: Added coordinate filtering to handle noisy data in sample2.csv.

wandb project path:
https://wandb.ai/shadenalzomai-general-organization-for-social-insurance/nyc_airbnb

Github repositry for the project
https://github.com/ShadenAlzomai/build-ml-pipeline-for-short-term-rental-prices
