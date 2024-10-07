import os
import pandas as pd
import matplotlib.pyplot as plt

def plot_aggregated_distributions_and_time_series(directory_path):
    # Initialize an empty DataFrame to hold the aggregated data
    aggregated_data = pd.DataFrame()

    # Specify the columns to plot
    columns_to_plot = ['A1', 'A2', 'SG1', 'SG2']

    # Iterate over all files in the given directory
    for filename in os.listdir(directory_path):
        if filename.endswith(".csv"):  # Check if the file is a CSV
            file_path = os.path.join(directory_path, filename)
            print(f"Processing file: {file_path}")

            # Read the CSV file into a DataFrame
            df = pd.read_csv(file_path)

            # Drop non-numerical columns and keep only the specified columns along with TIMESTAMP
            df = df[['TIMESTAMP'] + columns_to_plot].drop(columns=['RECORD'], errors='ignore')

            # Convert the TIMESTAMP column to datetime format if it exists
            if 'TIMESTAMP' in df.columns:
                df['TIMESTAMP'] = pd.to_datetime(df['TIMESTAMP'], errors='coerce')
            
            # Filter the DataFrame to only include columns of interest
            df = df.dropna(how='all', subset=columns_to_plot)  # Drop rows if all selected columns are NaN

            # Append the data to the aggregated DataFrame
            aggregated_data = pd.concat([aggregated_data, df], ignore_index=True)

    # Sort the aggregated DataFrame by TIMESTAMP if it exists
    if 'TIMESTAMP' in aggregated_data.columns:
        aggregated_data = aggregated_data.sort_values(by='TIMESTAMP').reset_index(drop=True)
        print("Data sorted by TIMESTAMP.")

    # Plot aggregated distributions for each of the specified columns
    for column in columns_to_plot:
        if column in aggregated_data.columns:  # Check if the column exists in the aggregated data
            plt.figure(figsize=(10, 6))
            
            # Plot the distribution of the column
            plt.hist(aggregated_data[column].dropna(), bins=50, alpha=0.7, color='skyblue')
            plt.title(f"Aggregated Distribution of {column}")
            plt.xlabel("Value")
            plt.ylabel("Frequency")
            
            # Show the plot
            plt.show()
    
    # Plot time series for each of the specified columns if TIMESTAMP is present
    if 'TIMESTAMP' in aggregated_data.columns:
        for column in columns_to_plot:
            if column in aggregated_data.columns:  # Check if the column exists in the aggregated data
                plt.figure(figsize=(12, 6))
                
                # Plot the time series for the column
                plt.plot(aggregated_data['TIMESTAMP'], aggregated_data[column], marker='o', linestyle='-', color='teal')
                plt.title(f"Time Series of {column}")
                plt.xlabel("Timestamp")
                plt.ylabel(f"{column} Value")
                plt.xticks(rotation=45)
                plt.grid(True)
                
                # Show the plot
                plt.show()
    else:
        print("TIMESTAMP column not found in the aggregated DataFrame.")

# Specify the path to the folder containing your CSV files
directory_path = "../data/acc-sg/"

# Call the function to aggregate, sort, and plot the distributions and time series
plot_aggregated_distributions_and_time_series(directory_path)
