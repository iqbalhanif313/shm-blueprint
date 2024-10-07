import csv
import os
from confluent_kafka import Consumer, KafkaException
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroDeserializer
from confluent_kafka.serialization import StringDeserializer

# Configuration for Kafka Consumer
consumer_conf = {
    'bootstrap.servers': 'localhost:9092',        # Kafka broker
    'group.id': 'acc-consumer-group',         # Consumer group ID
    'auto.offset.reset': 'earliest',              # Start from earliest message
    'enable.auto.commit': False,                   # Commit offsets automatically
}

# Schema Registry configuration
schema_registry_conf = {
    'url': 'http://localhost:8081'  # Schema Registry URL
}

# Topic to listen to
topic = 'FUSED_ACC_SENSOR_ALERTS'

# Output CSV file path
output_file = 'acc_sensor_alerts.csv'

# Create a Schema Registry client
schema_registry_client = SchemaRegistryClient(schema_registry_conf)

# Fetch the latest schema from the Schema Registry for the topic
subject_name = f'{topic}-value'  # The convention for schema subjects is '<topic_name>-value'
try:
    schema_info = schema_registry_client.get_latest_version(subject_name)
    avro_schema_str = schema_info.schema.schema_str
     # Debug print statement
except Exception as e:
    print(f"Failed to fetch schema for subject {subject_name}. Error: {e}")
    avro_schema_str = None

# Define a function to convert a dictionary to an object (if needed, customize for your use case)
def from_dict(data, ctx):
    """ Convert the Avro message data to a dictionary or object format. """
    return data

# Check if the schema was retrieved successfully before creating the deserializer
if avro_schema_str:
    # Create AvroDeserializer with the Avro schema string and the from_dict function
    avro_deserializer = AvroDeserializer(schema_str=avro_schema_str, schema_registry_client=schema_registry_client, from_dict=from_dict)
else:
    raise ValueError(f"Unable to initialize AvroDeserializer: Schema for {subject_name} not found or invalid")

# Create StringDeserializer for the key
# key_deserializer = BytesDeserializer()

# Create a Kafka Consumer
consumer = Consumer(consumer_conf)

# Subscribe to the topic
consumer.subscribe([topic])

# Check if CSV file already exists, if not, create it and write headers
file_exists = os.path.isfile(output_file)
with open(output_file, mode='a', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    # Write the header only if the file does not exist
    if not file_exists:
        csv_writer.writerow(['TIMESTAMP','ACC_SENSOR', 'ACC_DATA', 'ACC_STATUS','VIBRATION_DATA','TEMPERATURE_DATA','FOG_PRESENCE_DATA','WEATHER_ALERT_DATA' ])  # Modify these headers based on your schema

try:
    while True:
        # Poll for new messages with a timeout of 1 second
        msg = consumer.poll(timeout=1.0)

        # If no message is received, continue
        if msg is None:
            continue

        # If an error occurs, print the error and skip to the next message
        if msg.error():
            print(f"Consumer error: {msg.error()}")
            continue

        # Deserialize key and value using the deserializers
        # key = key_deserializer(msg.key(), None) if msg.key() else 'None'  # Decode key manually
        value = avro_deserializer(msg.value(), None) if msg.value() else 'None'

        # Print the message (optional)
        print(f"Received message: , value={value}")

        # Write the received message to CSV file
        with open(output_file, mode='a', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow([
                    value.get('TIMESTAMP', 'None'),
                    value.get('ACC_SENSOR', 'None'),
                    value.get('ACC_DATA', 'None'),
                    value.get('ACC_STATUS', 'None'),
                    value.get('VIBRATION_DATA', 'None'),
                    value.get('TEMPERATURE_DATA', 'None'),
                    value.get('FOG_PRESENCE_DATA', 'None'),
                    value.get('WEATHER_ALERT_DATA', 'None')
                ])

# Handle keyboard interrupt
except KeyboardInterrupt:
    print("Consumer interrupted")

# Close the consumer on exit
finally:
    consumer.close()