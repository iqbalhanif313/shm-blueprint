import pandas as pd
import matplotlib.pyplot as plt
import os

# Function to read all CSV files from a folder and concatenate them into a single DataFrame
def read_all_csv_files(folder_path):
    data_frames = []
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.csv'):
            csv_file_path = os.path.join(folder_path, file_name)
            df = pd.read_csv(csv_file_path)
            data_frames.append(df)
            print(f"Read data from {csv_file_path}")
    
    if data_frames:
        sensor_data = pd.concat(data_frames, ignore_index=True)
    else:
        raise ValueError(f"No CSV files found in the specified folder: {folder_path}")
    
    # Parse the timestamp column to datetime format (if it exists)
    if 'TIMESTAMP' in sensor_data.columns:
        sensor_data['TIMESTAMP'] = pd.to_datetime(sensor_data['TIMESTAMP'])
    
    return sensor_data

# Function to plot the timeline of weather alerts
def plot_weather_alert_timeline(sensor_data):
    if 'TIMESTAMP' in sensor_data.columns and 'Weather_Alert' in sensor_data.columns:
        plt.figure(figsize=(12, 8))
        
        # Create a scatter plot for each weather alert type over time
        for alert_type in sensor_data['Weather_Alert'].unique():
            alert_data = sensor_data[sensor_data['Weather_Alert'] == alert_type]
            plt.scatter(alert_data['TIMESTAMP'], [alert_type] * len(alert_data), label=alert_type, alpha=0.7, s=100)
        
        # Configure plot settings
        plt.title("Timeline of Weather Alerts Over Time")
        plt.xlabel("Time")
        plt.ylabel("Weather Alert Type")
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.legend(title='Alert Type')
        plt.tight_layout()
        plt.show()
    else:
        print("Required columns ('TIMESTAMP', 'alert_type') not found in the data.")

# Main function to read the data and plot the timeline
def main():
    # Specify the folder path
    folder_path = '../data/weather-alert'  # Update this path as needed

    # Read all CSV files from the specified folder and combine them into one DataFrame
    sensor_data = read_all_csv_files(folder_path)

    # Plot the timeline of weather alerts
    plot_weather_alert_timeline(sensor_data)

# Run the main function
if __name__ == "__main__":
    main()
