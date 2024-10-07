import os
import pandas as pd
import matplotlib.pyplot as plt

# Define the directory containing the CSV files
csv_directory = '../data/temperature'  # Change this to the path of your folder containing CSV files

# Read all CSV files in the directory
def read_csv_files(directory):
    # List all CSV files in the directory
    csv_files = [f for f in os.listdir(directory) if f.endswith('.csv')]
    
    # Read each CSV file and store it in a list of DataFrames
    dataframes = []
    for csv_file in csv_files:
        file_path = os.path.join(directory, csv_file)
        df = pd.read_csv(file_path)
        dataframes.append(df)
        print(f"Read file: {file_path}, shape: {df.shape}")
    
    # Concatenate all DataFrames into one DataFrame
    if dataframes:
        combined_df = pd.concat(dataframes, ignore_index=True)
        return combined_df
    else:
        return pd.DataFrame()  # Return an empty DataFrame if no CSV files are found

# Plot the distribution of sensor data
def plot_temperature_distribution(sensor_df):
    # Check if there are any temperature columns to plot
    temperature_columns = [col for col in sensor_df.columns if col.startswith('T') and col != "TIMESTAMP" ]
    
    for sensor in temperature_columns:
        plt.figure(figsize=(10, 6))
        plt.hist(sensor_df[sensor].dropna(), bins=50, color='blue', alpha=0.7)
        plt.title(f"Temperature Distribution for {sensor}")
        plt.xlabel("Temperature (°C)")
        plt.ylabel("Frequency")
        plt.grid(True)
        plt.show()

# Plot the time-series of sensor data
def plot_temperature_timeseries(sensor_df):
    # Convert TIMESTAMP column to datetime format if it exists
    if 'TIMESTAMP' in sensor_df.columns:
        sensor_df['TIMESTAMP'] = pd.to_datetime(sensor_df['TIMESTAMP'], errors='coerce')
        
        # Drop rows with invalid timestamps
        sensor_df = sensor_df.dropna(subset=['TIMESTAMP'])

        # Check if there are any temperature columns to plot
        temperature_columns = [col for col in sensor_df.columns if col.startswith('T') and col != "TIMESTAMP"]
        
        for sensor in temperature_columns:
            plt.figure(figsize=(12, 6))
            plt.plot(sensor_df['TIMESTAMP'], sensor_df[sensor], label=sensor, color='orange')
            plt.title(f"Temperature Time Series for {sensor}")
            plt.xlabel("Time")
            plt.ylabel("Temperature (°C)")
            plt.xticks(rotation=45)
            plt.grid(True)
            plt.legend()
            plt.tight_layout()
            plt.show()
    else:
        print("TIMESTAMP column not found. Cannot plot time-series data.")

# Main function to read files and plot data distribution and time-series
def main():
    # Read all CSV files from the specified directory
    sensor_df = read_csv_files(csv_directory)

    # Check if there is data to plot
    if not sensor_df.empty:
        # Plot the distribution of sensor data
        plot_temperature_distribution(sensor_df)
        
        # Plot the time-series of sensor data
        plot_temperature_timeseries(sensor_df)
    else:
        print(f"No CSV files found in directory: {csv_directory}")

if __name__ == "__main__":
    main()
