import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set Seaborn style for better aesthetics
sns.set(style="whitegrid")

# Step 1: Read the CSV file
df = pd.read_csv('../sg_sensor_alerts2x.csv')

# Step 2: Inspect the Data (Optional)
print("First few rows of the dataset:")
print(df.head())

# Step 3: Data Cleaning
# Ensure 'SG_DATA' is numeric. If not, convert and handle errors.
df['SG_DATA'] = pd.to_numeric(df['SG_DATA'], errors='coerce')

# Drop rows with NaN in 'SG_SENSOR' or 'SG_DATA'
df = df.dropna(subset=['SG_SENSOR', 'SG_DATA'])

# Step 4: Classify Data by 'SG_SENSOR'
# Create separate DataFrames for SG1 and SG2
df_SG1 = df[df['SG_SENSOR'] == 'SG1']
df_SG2 = df[df['SG_SENSOR'] == 'SG2']

# Optional: Print counts to verify
print("\nCounts by SG_SENSOR:")
print(df['SG_SENSOR'].value_counts())

# Step 5: Separate Plots for Each Sensor

# Option 1: Histogram with KDE for SG1
plt.figure(figsize=(10, 6))
sns.histplot(df_SG1['SG_DATA'], color='blue', kde=True, stat="density", bins=30, alpha=0.6)
plt.title('Distribution of SG_DATA for SG1 Sensor')
plt.xlabel('SG_DATA')
plt.ylabel('Density')
plt.show()

# Option 1: Histogram with KDE for SG2
plt.figure(figsize=(10, 6))
sns.histplot(df_SG2['SG_DATA'], color='orange', kde=True, stat="density", bins=30, alpha=0.6)
plt.title('Distribution of SG_DATA for SG2 Sensor')
plt.xlabel('SG_DATA')
plt.ylabel('Density')
plt.show()

# Option 2: Boxplot for SG1
plt.figure(figsize=(8, 6))
sns.boxplot(x='SG_SENSOR', y='SG_DATA', data=df_SG1, palette='Set2')
plt.title('Boxplot of SG_DATA for SG1 Sensor')
plt.xlabel('SG_SENSOR')
plt.ylabel('SG_DATA')
plt.show()

# Option 2: Boxplot for SG2
plt.figure(figsize=(8, 6))
sns.boxplot(x='SG_SENSOR', y='SG_DATA', data=df_SG2, palette='Set2')
plt.title('Boxplot of SG_DATA for SG2 Sensor')
plt.xlabel('SG_SENSOR')
plt.ylabel('SG_DATA')
plt.show()

# Option 3: Violin Plot for SG1
plt.figure(figsize=(8, 6))
sns.violinplot(x='SG_SENSOR', y='SG_DATA', data=df_SG1, palette='Set3')
plt.title('Violin Plot of SG_DATA for SG1 Sensor')
plt.xlabel('SG_SENSOR')
plt.ylabel('SG_DATA')
plt.show()

# Option 3: Violin Plot for SG2
plt.figure(figsize=(8, 6))
sns.violinplot(x='SG_SENSOR', y='SG_DATA', data=df_SG2, palette='Set3')
plt.title('Violin Plot of SG_DATA for SG2 Sensor')
plt.xlabel('SG_SENSOR')
plt.ylabel('SG_DATA')
plt.show()
