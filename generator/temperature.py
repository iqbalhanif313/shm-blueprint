import asyncio
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import seaborn as sns

# Generate synthetic Gaussian-like data for three sensors
n_samples = 8000  # Increase number of samples to get a smoother Gaussian appearance
mean_temps = [20]  # Set the mean temperatures for T1, T2, and T3
std_dev_temps = [5]  # Set the standard deviation for all three sensors to control spread

# Generate normally distributed data centered around respective mean temperatures with standard deviations
np.random.seed(42)  # Seed for reproducibility
temperature_data_T1 = np.random.normal(loc=mean_temps[0], scale=std_dev_temps[0], size=n_samples)

# Create a DataFrame with the temperature data
sensor_data = pd.DataFrame({'T1': temperature_data_T1})

# Generate timestamps starting from the current datetime with 0.1 second intervals
start_time = datetime.now()
time_intervals = [start_time + timedelta(milliseconds=100 * i) for i in range(n_samples)]
sensor_data['TIMESTAMP'] = time_intervals

# Save the DataFrame to a CSV file
csv_filename = '../data/temperature/temperature_data.csv'
sensor_data.to_csv(csv_filename, index=False)
print(f"Gaussian-like temperature data for three sensors has been saved to {csv_filename}")



# Plot the distribution of temperature data
def plot_temperature_distribution(sensor_data):
    for sensor in ['T1']:
        plt.figure(figsize=(10, 6))
        plt.hist(sensor_data[sensor], bins=50, color='blue', alpha=0.7)
        plt.title(f"Temperature Distribution for {sensor}")
        plt.xlabel("Temperature (°C)")
        plt.ylabel("Frequency")
        plt.grid(True)
        plt.show()

# Entry point to run the asyncio loop
async def main():
    # Plot the distribution before sending data to Kafka
    plot_temperature_distribution(sensor_data)


if __name__ == "__main__":
    asyncio.run(main())
