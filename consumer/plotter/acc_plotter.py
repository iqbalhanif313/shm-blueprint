import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set Seaborn style for better aesthetics
sns.set(style="whitegrid")

# Step 1: Read the CSV file
df = pd.read_csv('../acc_sensor_alerts2x.csv')

# Step 2: Inspect the Data (Optional)
print("First few rows of the dataset:")
print(df.head())

# Step 3: Data Cleaning
# Ensure 'ACC_DATA' is numeric. If not, convert and handle errors.
df['ACC_DATA'] = pd.to_numeric(df['ACC_DATA'], errors='coerce')

# Drop rows with NaN in 'ACC_SENSOR' or 'ACC_DATA'
df = df.dropna(subset=['ACC_SENSOR', 'ACC_DATA'])

# Step 4: Classify Data by 'ACC_SENSOR'
# Create separate DataFrames for A1 and A2
df_A1 = df[df['ACC_SENSOR'] == 'A1']
df_A2 = df[df['ACC_SENSOR'] == 'A2']

# Optional: Print counts to verify
print("\nCounts by ACC_SENSOR:")
print(df['ACC_SENSOR'].value_counts())

# Step 5: Plot the Distribution of 'ACC_DATA' for each sensor separately

# Plot 1: Histogram for A1
plt.figure(figsize=(10, 6))
sns.histplot(df_A1['ACC_DATA'], color='blue', kde=True, stat="density", bins=30, alpha=0.6)
plt.title('Distribution of ACC_DATA for A1 Sensor')
plt.xlabel('ACC_DATA')
plt.ylabel('Density')
plt.show()

# Plot 2: Histogram for A2
plt.figure(figsize=(10, 6))
sns.histplot(df_A2['ACC_DATA'], color='orange', kde=True, stat="density", bins=30, alpha=0.6)
plt.title('Distribution of ACC_DATA for A2 Sensor')
plt.xlabel('ACC_DATA')
plt.ylabel('Density')
plt.show()

# Plot 3: Boxplot for A1
plt.figure(figsize=(8, 6))
sns.boxplot(x='ACC_SENSOR', y='ACC_DATA', data=df_A1, palette='Set2')
plt.title('Boxplot of ACC_DATA for A1 Sensor')
plt.xlabel('ACC_SENSOR')
plt.ylabel('ACC_DATA')
plt.show()

# Plot 4: Boxplot for A2
plt.figure(figsize=(8, 6))
sns.boxplot(x='ACC_SENSOR', y='ACC_DATA', data=df_A2, palette='Set2')
plt.title('Boxplot of ACC_DATA for A2 Sensor')
plt.xlabel('ACC_SENSOR')
plt.ylabel('ACC_DATA')
plt.show()

# Plot 5: Violin Plot for A1
plt.figure(figsize=(8, 6))
sns.violinplot(x='ACC_SENSOR', y='ACC_DATA', data=df_A1, palette='Set3')
plt.title('Violin Plot of ACC_DATA for A1 Sensor')
plt.xlabel('ACC_SENSOR')
plt.ylabel('ACC_DATA')
plt.show()

# Plot 6: Violin Plot for A2
plt.figure(figsize=(8, 6))
sns.violinplot(x='ACC_SENSOR', y='ACC_DATA', data=df_A2, palette='Set3')
plt.title('Violin Plot of ACC_DATA for A2 Sensor')
plt.xlabel('ACC_SENSOR')
plt.ylabel('ACC_DATA')
plt.show()
