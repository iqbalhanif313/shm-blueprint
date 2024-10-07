import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import random

# Parameters
n_samples = 500  # Number of weather alert data points

# Possible weather alerts
weather_alerts = [
    "Heatwave Warning", 
    "Flood Watch", 
    "Tornado Warning", 
    "Thunderstorm Watch", 
    "High Wind Alert",
    "Hailstorm Warning",
    "Blizzard Warning",
    "Heavy Rainfall Alert"
]

# Probabilities for each weather alert
alert_probabilities = [0.2, 0.15, 0.1, 0.15, 0.1, 0.1, 0.1, 0.1]  # Example probabilities

# Generate random weather alert data
generated_alerts = np.random.choice(weather_alerts, size=n_samples, p=alert_probabilities)

# Generate timestamps with random intervals (e.g., from 1 to 10 hours)
start_time = datetime.now()
time_intervals = [start_time + timedelta(hours=random.randint(1, 10) * i) for i in range(n_samples)]

# Create a DataFrame for better visualization
weather_df = pd.DataFrame({
    'Weather_Alert': generated_alerts,
    'TIMESTAMP': time_intervals
})

csv_filename = '../data/weather-alert/weather_alert_data.csv'
weather_df.to_csv(csv_filename, index=False)
print(f"Weather alert data has been saved to {csv_filename}")



# Plot the distribution of weather alerts
def plot_weather_alert_distribution(weather_df):
    plt.figure(figsize=(12, 8))
    weather_df['Weather_Alert'].value_counts().plot(kind='bar', color='skyblue')
    plt.title("Distribution of Weather Alerts", fontsize=16)
    plt.xlabel("Weather Alert Type", fontsize=14)
    plt.ylabel("Frequency", fontsize=14)
    plt.xticks(rotation=45, ha='right', fontsize=12)
    plt.yticks(fontsize=12)
    plt.show()

# Generate and plot the weather alert distribution
plot_weather_alert_distribution(weather_df)

