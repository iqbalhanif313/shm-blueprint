import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set Seaborn style for better aesthetics
sns.set(style="whitegrid")

# Read the CSV file and remove leading/trailing spaces from column headers
df = pd.read_csv('../sg_sensor_alerts_to_used.csv')
df.columns = df.columns.str.strip()  # Remove leading/trailing spaces from column names

# Check column names to verify
print("Column Names:", df.columns)

# Convert 'TIMESTAMP' to datetime format
df['TIMESTAMP'] = pd.to_datetime(df['TIMESTAMP'], errors='coerce')

# Ensure 'SG_DATA' is numeric and drop NaN values
df['SG_DATA'] = pd.to_numeric(df['SG_DATA'], errors='coerce')
df = df.dropna(subset=['SG_SENSOR', 'SG_DATA'])

# Get unique sensors
unique_sensors = df['SG_SENSOR'].unique()

# Set color mapping for alert statuses
alert_colors = {'lower_threshold_exceeded': 'blue', 'upper_threshold_exceeded': 'red'}

# Iterate through each sensor and create a separate plot
for sensor in unique_sensors:
    # Filter data for the current sensor
    sensor_data = df[df['SG_SENSOR'] == sensor]
    
    # Create a figure for each sensor
    plt.figure(figsize=(14, 8))
    
    # Plot the time series data for the current sensor
    sns.lineplot(x='TIMESTAMP', y='SG_DATA', data=sensor_data, marker='o', linestyle='-', color='gray', label=f'{sensor} SG_DATA')
    
    # Highlight alerts based on SG_STATUS
    for status, color in alert_colors.items():
        # Get alerts specific to the current sensor and status
        alerts = sensor_data[sensor_data['SG_STATUS'] == status]
        plt.scatter(alerts['TIMESTAMP'], alerts['SG_DATA'], color=color, s=100, zorder=5, label=f'{sensor} {status}')
    
    # Add labels and title
    plt.xlabel('Timestamp')
    plt.ylabel('SG_DATA')
    plt.title(f'Time Series of SG_DATA with Alerts Highlighted for {sensor} Sensor')
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
