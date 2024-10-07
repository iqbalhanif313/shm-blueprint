import pandas as pd

def modify_timestamp_interval(file_path, output_path, interval_change=0.050):
    """
    Modify the TIMESTAMP values by changing the interval without resampling.

    Parameters:
    file_path (str): The path to the CSV file containing the data.
    output_path (str): The path to save the modified CSV file.
    interval_change (float): The interval change in seconds. Default is 0.050 seconds.

    Returns:
    None
    """
    # Read the CSV file into a DataFrame
    df = pd.read_csv(file_path)

    # Convert the TIMESTAMP column to datetime format
    df['TIMESTAMP'] = pd.to_datetime(df['TIMESTAMP'], errors='coerce')

    # Drop rows with invalid or NaT in TIMESTAMP
    df = df.dropna(subset=['TIMESTAMP'])

    # Reset index to ensure consistent iteration
    df.reset_index(drop=True, inplace=True)

    # Get the initial TIMESTAMP value as a reference point
    initial_timestamp = df['TIMESTAMP'].iloc[0]

    # Replace the TIMESTAMP values by adding the fixed interval change
    for i in range(len(df)):
        new_timestamp = initial_timestamp + pd.to_timedelta(i * interval_change, unit='s')
        df.at[i, 'TIMESTAMP'] = new_timestamp

    # Save the modified DataFrame to a new CSV file
    df.to_csv(output_path, index=False)
    print(f"Modified file saved as: {output_path}")

# Specify the path to your CSV file and output file
file_path = "../backup/CR6_IP_table_SG_ACC_2018_02_13_1258.csv"
output_path = "../acc-sg/CR6_IP_table_SG_ACC_2018_02_13_1258_sample_modified.csv"

# Modify the TIMESTAMP interval and save to a new CSV
modify_timestamp_interval(file_path, output_path)
