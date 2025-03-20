from kafka import KafkaProducer, KafkaConsumer
from pyspark.sql import SparkSession
import json

# Initialize Kafka Producer
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Initialize Spark Session
spark = SparkSession.builder \
    .appName("HealthcarePolicyProcessor") \
    .config("spark.sql.streaming.schemaInference", "true") \
    .getOrCreate()

# Function to send policy updates to Kafka
def send_policy_update(policy):
    producer.send("policy_updates", policy)
    print(f"Sent policy update: {policy}")

# Kafka Consumer to process updates
def consume_policy_updates():
    consumer = KafkaConsumer(
        "policy_updates",
        bootstrap_servers='localhost:9092',
        value_deserializer=lambda m: json.loads(m.decode('utf-8'))
    )
    
    for message in consumer:
        policy = message.value
        print(f"Received policy update: {policy}")
        process_policy_with_spark(policy)

# Function to process policy data with Spark
def process_policy_with_spark(policy):
    df = spark.createDataFrame([policy])
    df.show()
    # Here, we can apply transformations or store the processed data

if __name__ == "__main__":
    # Example policy update
    sample_policy = {"id": 4, "title": "Policy D", "content": "Includes outpatient care and emergency services."}
    send_policy_update(sample_policy)
    
    # Start consuming updates
    consume_policy_updates()
