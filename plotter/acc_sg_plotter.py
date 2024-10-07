import os
import pandas as pd
import matplotlib.pyplot as plt

def plot_aggregated_distributions(directory_path):
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

            # Drop non-numerical columns and keep only the specified columns
            df = df.drop(columns=['TIMESTAMP', 'RECORD'], errors='ignore')

            # Filter the DataFrame to only include columns of interest
            df = df[columns_to_plot].dropna(how='all')  # Drop rows if all selected columns are NaN

            # Append the data to the aggregated DataFrame
            aggregated_data = pd.concat([aggregated_data, df], ignore_index=True)

    # Iterate over each of the specified columns in the aggregated DataFrame
    for column in columns_to_plot:
        if column in aggregated_data.columns:  # Check if the column exists in the aggregated data
            plt.figure(figsize=(10, 6))
            
            # Plot the distribution of the column
            plt.hist(aggregated_data[column], bins=50, alpha=0.7)
            plt.title(f"Aggregated Distribution of {column}")
            plt.xlabel("Value")
            plt.ylabel("Frequency")
            
            # Show the plot
            plt.show()

# Specify the path to the folder containing your CSV files
directory_path = "../data/acc-sg/"

# Call the function to aggregate and plot the distributions
plot_aggregated_distributions(directory_path)