import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set Seaborn style for better aesthetics
sns.set(style="whitegrid")

# Read the first CSV file (output data)
df1 = pd.read_csv('../acc_sensor_alerts.csv')

# Convert 'TIMESTAMP' to datetime format in the first CSV
df1['TIMESTAMP'] = pd.to_datetime(df1['TIMESTAMP'], errors='coerce')

# Ensure 'ACC_DATA' is numeric and drop NaN values
df1['ACC_DATA'] = pd.to_numeric(df1['ACC_DATA'], errors='coerce')
df1 = df1.dropna(subset=['ACC_SENSOR', 'ACC_DATA'])

# Read the second CSV file for comparison (input data)
df2 = pd.read_csv('../acc_sensor_aligned.csv')

# Convert 'TIMESTAMP' to datetime format in the second CSV
df2['TIMESTAMP'] = pd.to_datetime(df2['TIMESTAMP'], errors='coerce')

# Ensure 'DATA' is numeric and drop NaN values
df2['DATA'] = pd.to_numeric(df2['DATA'], errors='coerce')
df2 = df2.dropna(subset=['SENSOR', 'DATA'])

# Sort the second CSV by 'TIMESTAMP' before plotting
df2 = df2.sort_values(by='TIMESTAMP')

# Plot the distribution of output (ACC_DATA) in a histogram with KDE
plt.figure(figsize=(10, 6))
sns.histplot(df1['ACC_DATA'], kde=True, color='blue', bins=30, label='Output Data (ACC_DATA)', kde_kws={'linewidth': 2})
plt.xlabel('ACC_DATA')
plt.ylabel('Density')
plt.title('Distribution of Output Data (ACC_DATA)')
plt.legend()
plt.tight_layout()
plt.show()

# Plot the distribution of input (DATA from second CSV) in a histogram with KDE
plt.figure(figsize=(10, 6))
sns.histplot(df2['DATA'], kde=True, color='purple', bins=30, label='Input Data (Comparison)', kde_kws={'linewidth': 2})
plt.xlabel('Input Data')
plt.ylabel('Density')
plt.title('Distribution of Input Data (Comparison)')
plt.legend()
plt.tight_layout()
plt.show()
