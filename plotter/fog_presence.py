import asyncio
import pandas as pd
import matplotlib.pyplot as plt
import os

# Define the folder containing the CSV files
csv_folder_path = '../data/fog-presence'  # Change to your folder path containing the CSV files

# Function to read all CSV files in a folder and concatenate them into a single DataFrame
def read_all_csv_files(folder_path):
    csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
    dataframes = []
    for csv_file in csv_files:
        csv_file_path = os.path.join(folder_path, csv_file)
        try:
            df = pd.read_csv(csv_file_path)
            print(f"Read {csv_file} with shape {df.shape}")
            dataframes.append(df)
        except Exception as e:
            print(f"Failed to read {csv_file_path}: {e}")
    if dataframes:
        combined_df = pd.concat(dataframes, ignore_index=True)
        print(f"Combined DataFrame shape: {combined_df.shape}")
        return combined_df
    else:
        print("No CSV files found or failed to read all files.")
        return pd.DataFrame()  # Return an empty DataFrame if no files were read

# Function to plot the distribution of fog presence
def plot_fog_presence_distribution(sensor_df):
    for column in sensor_df.columns:
        if column != 'TIMESTAMP':  # Exclude TIMESTAMP column if it exists
            plt.figure(figsize=(10, 6))
            sensor_df[column].value_counts().plot(kind='bar', color='skyblue')
            plt.title(f"Distribution of {column} Fog Presence")
            plt.xlabel("Fog Presence (True/False)")
            plt.ylabel("Frequency")
            plt.grid(True)
            plt.show()

# Function to plot the time-series of fog presence using a step plot
def plot_fog_presence_timeseries(sensor_df):
    if 'TIMESTAMP' in sensor_df.columns:
        # Convert TIMESTAMP column to datetime format
        sensor_df['TIMESTAMP'] = pd.to_datetime(sensor_df['TIMESTAMP'], errors='coerce')
        # Drop rows with invalid timestamps
        sensor_df = sensor_df.dropna(subset=['TIMESTAMP'])

        for column in sensor_df.columns:
            if column != 'TIMESTAMP':  # Exclude TIMESTAMP column
                plt.figure(figsize=(12, 6))
                
                # Use step plot for better visualization of binary data
                plt.step(sensor_df['TIMESTAMP'], sensor_df[column], label=column, color='green', alpha=0.8, where='post')
                
                plt.title(f"Time Series of {column} Fog Presence")
                plt.xlabel("Time")
                plt.ylabel("Fog Presence (True/False)")
                plt.ylim(-0.1, 1.1)  # Set y-axis limits to show binary values clearly
                plt.yticks([0, 1], labels=["False", "True"])  # Set y-tick labels to indicate True/False
                plt.xticks(rotation=45)
                plt.grid(True)
                plt.legend()
                plt.tight_layout()
                plt.show()
    else:
        print("TIMESTAMP column not found. Cannot plot time-series data.")

# Entry point to run the asyncio loop
async def main():
    # Read all CSV files from the folder
    sensor_df = read_all_csv_files(csv_folder_path)
    
    # Plot fog presence distribution if data is not empty
    if not sensor_df.empty:
        plot_fog_presence_distribution(sensor_df)
        plot_fog_presence_timeseries(sensor_df)
    else:
        print("No data to plot.")

if __name__ == "__main__":
    asyncio.run(main())
