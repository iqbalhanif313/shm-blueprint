import pandas as pd
import os
import time
import json
import asyncio
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from confluent_kafka import SerializingProducer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer
from confluent_kafka.serialization import StringSerializer

producer_conf = {
    'bootstrap.servers': 'localhost:9092',
    'key.serializer': StringSerializer('utf_8'),  # String serializer for the key
    'value.serializer': None  # We'll assign the AvroSerializer later
}

# Schema Registry configuration
schema_registry_conf = {
    'url': 'http://localhost:8081'
}

data_to_read = ["A1", "A2"]

# Create a Schema Registry client
schema_registry_client = SchemaRegistryClient(schema_registry_conf)

# Fetch the latest schema from the schema registry for the topic
subject_name = 'sensor-acc-value'
schema_info = schema_registry_client.get_latest_version(subject_name)
schema = schema_info.schema

# Create AvroSerializer for the value
avro_serializer = AvroSerializer(schema_registry_client, schema, lambda obj, ctx: obj)

# Update producer configuration with AvroSerializer for the value
producer_conf['value.serializer'] = avro_serializer

# Create a SerializingProducer
producer = SerializingProducer(producer_conf)

def delivery_report(err, msg):
    """ Delivery report callback called once for each message produced to indicate delivery result.
        Triggered by poll() or flush(). """
    # if err is not None:
    #     print(f'Message delivery failed: {err}')
    # else:
    #     print(f'Message delivered to {msg.topic()} [{msg.partition()}]')

def read_all_csvs_in_folder(folder_path):
    # List all files in the folder
    files = os.listdir(folder_path)
    # Filter for CSV files
    csv_files = [f for f in files if f.endswith('.csv')]
    
    # Dictionary to store DataFrames
    dataframes = {}
    
    # Loop through CSV files and read them into DataFrames
    for csv_file in csv_files:
        file_path = os.path.join(folder_path, csv_file)
        df = pd.read_csv(file_path)
        # print(csv_file)
        # print(df['TIMESTAMP'])
        # df['TIMESTAMP'] = pd.to_datetime(df['TIMESTAMP'])  # Convert TIMESTAMP to datetime
        dataframes[csv_file] = df
        print(f"Loaded {csv_file} with {len(df)} rows and {len(df.columns)} columns")
        
    return dataframes

def produce_message(topic, message):
    """ Produce a message to Kafka. """
    if topic in data_to_read :
        print(message)
        producer.produce(topic="sensor-acc",key="acc_data_"+topic,  value=message, on_delivery=delivery_report)
    producer.poll(0)

def parse_timestamp(timestamp_str):
    # Define possible timestamp formats
    formats = [
        '%Y-%m-%d %H:%M:%S.%f',  # Format with 6 digits of microseconds
        '%Y-%m-%d %H:%M:%S.%f',  # Format with 3 digits of milliseconds
        '%Y-%m-%d %H:%M:%S',      # Format without milliseconds  # Format with 2 digits of milliseconds (example)
    ]
    
    for fmt in formats:
        try:
            # Attempt to parse the timestamp with the given format
            return datetime.strptime(timestamp_str, fmt)
        except ValueError:
            continue
    
    # If no format worked, raise an error
    raise ValueError(f"Time data '{timestamp_str}' does not match any expected format")



async def process_row(row, executor):
    print(f"TIMESTAMP: {row['TIMESTAMP']}")

    # Send data to Kafka
    loop = asyncio.get_event_loop()
    tasks = []
    for column in row.index:
        if column not in ['TIMESTAMP']:
            # Extract milliseconds from the original TIMESTAMP
            original_timestamp = parse_timestamp(row['TIMESTAMP'])
            milliseconds = original_timestamp.microsecond // 1000
            
            # Get the current date and time
            now = datetime.now()
            
            # Construct the new timestamp with the current date and time but original milliseconds
            new_timestamp = now.replace(microsecond=milliseconds * 1000)
            
            # Format the new timestamp as a string
            new_timestamp_str = new_timestamp.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]  # Remove the last 3 digits from microseconds
            
            message = {
                "TIMESTAMP": new_timestamp_str,
                "data": row[column],
                "sensor": column
            }
            topic = column
            tasks.append(loop.run_in_executor(executor, produce_message, topic, message))
    
    await asyncio.gather(*tasks)

async def process_dataframes(dataframes):
    # Create a ThreadPoolExecutor
    executor = ThreadPoolExecutor(max_workers=10)
    
    # Loop through each DataFrame
    for file_name, df in dataframes.items():
        print(f"\nProcessing {file_name}")
        
        # Calculate the interval between consecutive timestamps
        # df['INTERVAL'] = df['TIMESTAMP'].diff().fillna(pd.Timedelta(seconds=0))
        
        # Loop through each row in the DataFrame
        for index, row in df.iterrows():
            # if index > 0:  # Skip the delay for the first row
                # interval_seconds = row['INTERVAL'].total_seconds()
                # print(f"Waiting for {interval_seconds} seconds")
                # print(interval_seconds - 0.0025)
            time.sleep(0.05)
            
            print(f"\nRow {index}:")
            await process_row(row, executor)

# Folder path containing the CSV files
folder_path = '../data/acc-sg'

# Read all CSV files
dataframes = read_all_csvs_in_folder(folder_path)


# Process each DataFrame asynchronously
asyncio.run(process_dataframes(dataframes))

# Wait for all messages to be delivered
producer.flush()
