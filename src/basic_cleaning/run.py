#!/usr/bin/env python
"""
Download raw data, filter price outliers, handle missing values, and remove duplicates.
"""
import argparse
import logging
import pandas as pd
import wandb
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()

def go(args):
    """
    Run the basic cleaning pipeline.
    """
    # Initialize a W&B run
    run = wandb.init(
        project="nyc_airbnb",
        job_type="basic_cleaning")
    
    # Log the configuration/arguments to W&B
    run.config.update(vars(args))

    logger.info("Downloading artifact: %s", args.input_artifact)
    # Download the input artifact and get its local path
    artifact_local_path = run.use_artifact(args.input_artifact).file()
    
    # Load the data into a pandas DataFrame
    df = pd.read_csv(artifact_local_path)

    # 1. Price Filtering
    logger.info("Filtering price outliers between %d and %d", args.min_price, args.max_price)
    idx = df['price'].between(args.min_price, args.max_price)
    df = df[idx].copy()

    # 2. DateTime Formatting
    logger.info("Converting 'last_review' column to datetime format")
    df['last_review'] = pd.to_datetime(df['last_review'])

    # 3. Handling Missing Values
    logger.info("Handling missing values (Imputing reviews and dropping missing names)")
    # Fill missing reviews_per_month with 0 as they likely have no reviews yet
    df['reviews_per_month'] = df['reviews_per_month'].fillna(0)
    # Drop records missing essential identity information (name or host_name)
    df = df.dropna(subset=['name', 'host_name'])

    # 4. Removing Duplicates
    logger.info("Removing duplicate rows from the dataset")
    df = df.drop_duplicates().reset_index(drop=True)

    # filter data outside NYC boundaries
    idx = df['longitude'].between(-74.25, -73.50) & df['latitude'].between(40.5, 41.2)
    df = df[idx].copy()

    # 5. Save and Upload Results
    logger.info("Saving cleaned data and uploading to W&B")
    

    # Using /tmp to ensure write permissions in the workspace environment
    output_path = "/tmp/clean_sample.csv"
    df.to_csv(output_path, index=False)

    # Create a new W&B artifact for the cleaned data
    artifact = wandb.Artifact(
        args.output_artifact,
        type=args.output_type,
        description=args.output_description,
    )
    artifact.add_file(output_path)
    
    # Log the artifact to W&B
    run.log_artifact(artifact)
    
    # Finish the W&B run
    run.finish()
    logger.info("Basic cleaning pipeline completed successfully")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Basic cleaning module for the Airbnb project")

    parser.add_argument(
        "--input_artifact", 
        type=str,
        help="The name of the input artifact (raw data)",
        required=True
    )

    parser.add_argument(
        "--output_artifact", 
        type=str,
        help="The name for the output artifact (cleaned data)",
        required=True
    )

    parser.add_argument(
        "--output_type", 
        type=str,
        help="The type of the output artifact",
        required=True
    )

    parser.add_argument(
        "--output_description", 
        type=str,
        help="A brief description of the cleaning process",
        required=True
    )

    parser.add_argument(
        "--min_price", 
        type=float,
        help="The minimum price to retain in the dataset",
        required=True
    )

    parser.add_argument(
        "--max_price", 
        type=float,
        help="The maximum price to retain in the dataset",
        required=True
    )

    args = parser.parse_args()
    go(args)