import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set Seaborn style for better aesthetics
sns.set(style="whitegrid")

# Read the first CSV file
df1 = pd.read_csv('../acc_sensor_alerts_final.csv')

# Convert 'TIMESTAMP' to datetime format in the first CSV
df1['TIMESTAMP'] = pd.to_datetime(df1['TIMESTAMP'], errors='coerce')

# Ensure 'ACC_DATA' is numeric and drop NaN values
df1['ACC_DATA'] = pd.to_numeric(df1['ACC_DATA'], errors='coerce')
df1 = df1.dropna(subset=['ACC_SENSOR', 'ACC_DATA'])

# Read the second CSV file for comparison
df2 = pd.read_csv('../acc_sensor_aligned_final.csv')

# Convert 'TIMESTAMP' to datetime format in the second CSV
df2['TIMESTAMP'] = pd.to_datetime(df2['TIMESTAMP'], errors='coerce')

# Ensure 'DATA' is numeric and drop NaN values
df2['DATA'] = pd.to_numeric(df2['DATA'], errors='coerce')
df2 = df2.dropna(subset=['SENSOR', 'DATA'])

# Sort the second CSV by 'TIMESTAMP' before plotting
df2 = df2.sort_values(by='TIMESTAMP')

# Get unique sensors from the first CSV
unique_sensors = df1['ACC_SENSOR'].unique()

# Set color mapping for alert statuses
alert_colors = {'lower_threshold_exceeded': 'blue', 'upper_threshold_exceeded': 'red'}

# Iterate through each sensor and create a separate plot
for sensor in unique_sensors:
    # Filter data for the current sensor from both datasets
    sensor_data1 = df1[df1['ACC_SENSOR'] == sensor]
    sensor_data2 = df2[df2['SENSOR'] == sensor]
    
    # Create a figure for each sensor
    plt.figure(figsize=(14, 8))
    
    # Plot only dots for the time series data from the first CSV
    sns.scatterplot(x='TIMESTAMP', y='ACC_DATA', data=sensor_data1, color='gray', s=20)
    
    # Plot the upper and lower thresholds as thicker lines
    plt.plot(sensor_data1['TIMESTAMP'], sensor_data1['UPPER_THRESHOLD'], color='green', linestyle='--', linewidth=2, label='Upper Threshold')
    plt.plot(sensor_data1['TIMESTAMP'], sensor_data1['LOWER_THRESHOLD'], color='orange', linestyle='--', linewidth=2, label='Lower Threshold')
    
    # Highlight alerts based on ACC_STATUS with reduced dot size
    for status, color in alert_colors.items():
        alerts = sensor_data1[sensor_data1['ACC_STATUS'] == status]
        plt.scatter(alerts['TIMESTAMP'], alerts['ACC_DATA'], color=color, s=50, zorder=5, label=status)
    
    # Plot the sorted comparison data from the second CSV as a flat line
    plt.plot(sensor_data2['TIMESTAMP'], sensor_data2['DATA'], color='purple', linestyle='-', linewidth=1.5, label='Input Data')
    
    # Add labels and title
    plt.xlabel('Timestamp')
    plt.ylabel('ACC_DATA')
    plt.title(f'Time Series of ACC_DATA with Alerts, Thresholds, and Input Data for {sensor} Sensor')
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
