# src/get_data.py

import zipfile
import os
import pandas as pd

def prepare_local_data():
    """
    Checks for the local zip file, extracts it, and prepares the data.
    This script does NOT download anything.
    """
    
    # Define file paths
    zip_path = "data/CMAPSSData.zip"
    output_dir = "data/"
    output_csv_path = "data/RUL_FD001.csv"

    # --- Step 1: Check if the raw data exists ---
    if not os.path.exists(zip_path):
        print("Error: `CMAPSSData.zip` not found in the `data` directory.")
        print("Please download the file from the NASA website:")
        print("https://data.nasa.gov/Aerospace/Turbofan-Engine-Degradation-Simulation-Data-Set/vrks-gjie")
        print("And place it in the 'data' folder before running this script again.")
        return # Stop execution

    # --- Step 2: Check if the data is already processed ---
    if os.path.exists(output_csv_path):
        print("Processed data already exists. Skipping preparation.")
        return

    # --- Step 3: Unzip and process the data ---
    print(f"Found {zip_path}. Unzipping and processing...")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(output_dir)
    print(f"Data extracted to {output_dir}")

    # Define column names for the dataset
    columns = [
        'RUL'
    ]
    #columns += [f'sensor_measurement_{i}' for i in range(1, 22)]
    
    # Load the specific training file we'll use (FD001)
    train_path = os.path.join(output_dir, 'RUL_FD001.txt')
    df = pd.read_csv(train_path, sep=' ', header=None)

    # Drop the last two empty columns that are created by the space delimiter
    df.drop(columns=[1], inplace=True)
    
    # Assign the correct column names
    df.columns = columns
    
    # Save the processed data to a clean CSV file
    df.to_csv(output_csv_path, index=False)
    print(f"Processed data successfully saved to {output_csv_path}")


if __name__ == "__main__":
    if not os.path.exists("data"):
        os.makedirs("data")
    prepare_local_data()