import numpy as np
import asyncio
import pandas as pd
from sklearn.datasets import make_blobs
from confluent_kafka import Producer
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

# Generate synthetic data
def generate_data():
    # Number of samples
    n_samples = 8000

    # Define the desired proportions
    proportions = [0.3, 0.5, 0.2]  # 30% low, 50% moderate, 20% high

    # Generate synthetic data with make_blobs, 3 centers for 'low', 'moderate', 'high'
    X, y = make_blobs(n_samples=n_samples, centers=3, random_state=42)

    # Adjust the class distribution according to the desired proportions
    n_low = int(proportions[0] * n_samples)
    n_moderate = int(proportions[1] * n_samples)
    n_high = n_samples - n_low - n_moderate

    # Create an array that maps the number of samples to each class
    adjusted_y = np.concatenate([
        np.full(n_low, 0),       # 'low'
        np.full(n_moderate, 1),  # 'moderate'
        np.full(n_high, 2)       # 'high'
    ])

    # Shuffle the adjusted labels to mix the classes
    np.random.shuffle(adjusted_y)

    # Map the numeric classes to categorical vibration intensities
    vibration_labels = ['low', 'moderate', 'high']
    vibration_intensity = [vibration_labels[i] for i in adjusted_y]

    # Generate sequential timestamps starting from the current time
    start_time = datetime.now()
    timestamps = [start_time + timedelta(seconds=i) for i in range(n_samples)]

    # Create a DataFrame to store the data
    sensor_data = pd.DataFrame({
        'TIMESTAMP': timestamps,
        'vibration': vibration_intensity,
        "sensor": "V1"
    })

    csv_filename = '../data/vibration/vibration_data.csv'
    sensor_data.to_csv(csv_filename, index=False)
    print(f"Sensor vibration data has been saved to {csv_filename}")

    return sensor_data

# Plot the distribution of vibration intensity categories
def plot_vibration_distribution(sensor_data):
    plt.figure(figsize=(10, 6))
    sensor_data['vibration'].value_counts().plot(kind='bar', color=['blue', 'orange', 'green'])
    plt.title("Distribution of Vibration Intensity")
    plt.xlabel("Vibration Intensity")
    plt.ylabel("Frequency")
    plt.show()

# Main async function to iterate over rows and send each to Kafka
async def main():
    sensor_data = generate_data()

    plot_vibration_distribution(sensor_data)

# Run the async loop
if __name__ == "__main__":
    asyncio.run(main())
