import asyncio
import pandas as pd
import matplotlib.pyplot as plt
import os

# Function to read all CSV files from a folder and concatenate them into a single DataFrame
def read_all_csv_files(folder_path):
    # Initialize an empty list to store individual DataFrames
    data_frames = []
    
    # Loop through all files in the specified folder
    for file_name in os.listdir(folder_path):
        # Check if the file has a .csv extension
        if file_name.endswith('.csv'):
            csv_file_path = os.path.join(folder_path, file_name)
            # Read the CSV file into a DataFrame and append to the list
            df = pd.read_csv(csv_file_path)
            data_frames.append(df)
            print(f"Read data from {csv_file_path}")
    
    # Concatenate all the DataFrames into a single DataFrame
    if data_frames:
        sensor_data = pd.concat(data_frames, ignore_index=True)
    else:
        raise ValueError(f"No CSV files found in the specified folder: {folder_path}")
    
    # Parse the timestamp column to datetime format (if it exists)
    if 'TIMESTAMP' in sensor_data.columns:
        sensor_data['TIMESTAMP'] = pd.to_datetime(sensor_data['TIMESTAMP'])

    return sensor_data

# Function to map categories to numerical values for plotting
def map_categories_to_values(df, column_name):
    category_mapping = {'low': 1, 'moderate': 2, 'high': 3}
    df['CategoryValue'] = df[column_name].map(category_mapping)
    return df

# Function to plot the time series of vibration intensity using a step plot
def plot_vibration_timeseries(sensor_data):
    if 'TIMESTAMP' in sensor_data.columns and 'vibration' in sensor_data.columns:
        # Map the vibration intensity categories to numeric values for plotting
        sensor_data = map_categories_to_values(sensor_data, 'vibration')
        
        plt.figure(figsize=(12, 6))
        
        # Create a step plot for vibration intensity over time
        plt.step(sensor_data['TIMESTAMP'], sensor_data['CategoryValue'], label='Vibration Intensity', color='blue', where='post')
        
        # Configure plot settings
        plt.title("Time Series of Vibration Intensity")
        plt.xlabel("Time")
        plt.ylabel("Vibration Intensity (1=Low, 2=Moderate, 3=High)")
        plt.yticks([1, 2, 3], ['Low', 'Moderate', 'High'])  # Label the y-axis with category names
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.show()
    else:
        print("Required columns ('TIMESTAMP', 'vibration_intensity') not found in the data.")

# Main async function to read data from all CSV files and plot the distribution and time series
async def main():
    # Specify the folder path
    folder_path = '../data/vibration'  # Update this path as needed

    # Read all CSV files from the specified folder and combine them into one DataFrame
    sensor_data = read_all_csv_files(folder_path)

    # Plot the time series of vibration intensity
    plot_vibration_timeseries(sensor_data)

# Run the async loop
if __name__ == "__main__":
    asyncio.run(main())
