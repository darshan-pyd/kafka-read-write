# main.py
import os, json
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from kafka import KafkaProducer
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

# HTTP Basic Authentication
security = HTTPBasic()

# Kafka Configuration
KAFKA_SERVER = os.getenv("KAFKA_SERVER", "localhost:9092")
TOPIC_NAME = os.getenv("KAFKA_TOPIC", "my_topic")

kafka_producer_config = {
    "bootstrap_servers": KAFKA_SERVER,
    "acks": "all",  # Change this according to your requirements
    # Add any other Kafka producer configurations as needed
}
# Kafka Producer
producer = KafkaProducer(**kafka_producer_config)

app = FastAPI()

# Pydantic model for JSON payload
class Item(BaseModel):
    name: str
    description: str = None

# FastAPI endpoint to accept JSON payload
@app.post("/send-to-kafka")
async def send_to_kafka(item: Item, credentials: HTTPBasicCredentials = Depends(security)):
    # Check username and password
    correct_username = os.getenv("USER_DETAIL", "test_user")
    correct_password = os.getenv("PASSWORD", "test_password")

    if credentials.username != correct_username or credentials.password != correct_password:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Convert Pydantic model to dictionary
    payload = item.dict()
    json_payload = json.dumps(payload)

    # Send the payload to Kafka
    producer.send(TOPIC_NAME, value=json_payload.encode("utf-8"))

    return {"message": "Payload sent to Kafka"}

if __name__ == "__main__":
    # Run the FastAPI application
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)