import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set Seaborn style for better aesthetics
sns.set(style="whitegrid")

# Read the CSV file
df = pd.read_csv('../acc_sensor_alerts2x.csv')

# Convert 'TIMESTAMP' to datetime format
df['TIMESTAMP'] = pd.to_datetime(df['TIMESTAMP'], errors='coerce')

# Ensure 'ACC_DATA' is numeric and drop NaN values
df['ACC_DATA'] = pd.to_numeric(df['ACC_DATA'], errors='coerce')
df = df.dropna(subset=['ACC_SENSOR', 'ACC_DATA'])

# Get unique sensors
unique_sensors = df['ACC_SENSOR'].unique()

# Set color mapping for alert statuses
alert_colors = {'lower_threshold_exceeded': 'blue', 'upper_threshold_exceeded': 'red'}

# Iterate through each sensor and create a separate plot
for sensor in unique_sensors:
    # Filter data for the current sensor
    sensor_data = df[df['ACC_SENSOR'] == sensor]
    
    # Create a figure for each sensor
    plt.figure(figsize=(14, 8))
    
    # Plot the time series data for the current sensor
    sns.lineplot(x='TIMESTAMP', y='ACC_DATA', data=sensor_data, marker='o', linestyle='-', color='gray')
    
    # Highlight alerts based on ACC_STATUS
    for status, color in alert_colors.items():
        alerts = sensor_data[sensor_data['ACC_STATUS'] == status]
        plt.scatter(alerts['TIMESTAMP'], alerts['ACC_DATA'], color=color, s=100, zorder=5, label=status)
    
    # Add labels and title
    plt.xlabel('Timestamp')
    plt.ylabel('ACC_DATA')
    plt.title(f'Time Series of ACC_DATA with Alerts Highlighted for {sensor} Sensor')
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
