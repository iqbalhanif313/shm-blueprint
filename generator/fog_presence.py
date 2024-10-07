import asyncio
import json
import numpy as np
import pandas as pd
from confluent_kafka import Producer
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Configuration for Kafka producer
# conf = {'bootstrap.servers': "localhost:9092"}  # Change to your Kafka broker
# producer = Producer(**conf)

# Parameters
n_samples = 8000  # Number of data points
fog_probabilities = [0.2]  # Probabilities for FP1, FP2, FP3

# Generate fog presence data for FP1, FP2, FP3
fog_presence_fp1 = np.random.choice([False, True], size=n_samples, p=[1 - fog_probabilities[0], fog_probabilities[0]])

# Generate timestamps starting from now, with a 1-second interval between each row
start_time = datetime.now()
timestamps = [start_time + timedelta(seconds=1 * i) for i in range(n_samples)]

# Create a DataFrame for better visualization
sensor_df = pd.DataFrame({
    'FP1': fog_presence_fp1,
    'TIMESTAMP': timestamps
})

csv_filename = '../data/fog-presence/sensor_data.csv'
sensor_df.to_csv(csv_filename, index=False)
print(f"Sensor data has been saved to {csv_filename}")

# Plotting the distribution of fog presence before sending to Kafka
def plot_fog_presence_distribution(sensor_df):
    for column in ['FP1']:
        plt.figure(figsize=(10, 6))
        sensor_df[column].value_counts().plot(kind='bar', color='skyblue')
        plt.title(f"Distribution of {column} Fog Presence")
        plt.xlabel("Fog Presence (True/False)")
        plt.ylabel("Frequency")
        plt.show()

# Entry point to run the asyncio loop
async def main():
    plot_fog_presence_distribution(sensor_df)

if __name__ == "__main__":
    asyncio.run(main())
