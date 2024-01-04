# kafka_consumer.py
import os, json
from kafka import KafkaConsumer
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

# Kafka configuration
KAFKA_SERVER = os.getenv("KAFKA_SERVER", "localhost:9092")
TOPIC_NAME = os.getenv("KAFKA_TOPIC", "my_topic")

# MongoDB Configuration
MONGO_CONNECTION_STRING = os.getenv("MONGO_CONNECTION_STRING", "mongodb://localhost:27017")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "my_topics")
MONGO_COLLECTION_NAME = os.getenv("MONGO_COLLECTION_NAME", "topicss")

# MongoDB Client
mongo_client = MongoClient(MONGO_CONNECTION_STRING)
mongo_db = mongo_client[MONGO_DB_NAME]
mongo_collection = mongo_db[MONGO_COLLECTION_NAME]

processed_messages = set()  # Use a set to track processed messages

def consume_messages():
    consumer = KafkaConsumer(TOPIC_NAME, bootstrap_servers=KAFKA_SERVER)
    for message in consumer:
        try:
            # Print the raw message value
            print("Received message:", message.value)

            # Decode and load JSON payload from Kafka message value
            payload = json.loads(message.value.decode("utf-8"))

            # Insert payload into MongoDB
            with MongoClient(MONGO_CONNECTION_STRING) as mongo_client:
                mongo_db = mongo_client[MONGO_DB_NAME]
                mongo_collection = mongo_db[MONGO_COLLECTION_NAME]
                try:
                    mongo_collection.insert_one(payload)
                    print("Data inserted into MongoDB:")

                    # Add the message to the set of processed messages
                    processed_messages.add(message.value)
                except Exception as e:
                    print("Error inserting data into MongoDB:", e)

        except Exception as e:
            print(f"Error processing message: {e}")


# Start the Kafka consumer in a separate process
import multiprocessing
kafka_consumer_process = multiprocessing.Process(target=consume_messages)
kafka_consumer_process.start()

if __name__ == "__main__":
    # Start the Kafka consumer process
    import multiprocessing
    kafka_consumer_process = multiprocessing.Process(target=consume_messages)
    kafka_consumer_process.start()