# main.py
import os, json
from fastapi import FastAPI, Depends, HTTPException, Form
from fastapi.security import OAuth2PasswordBearer
from kafka import KafkaProducer
from dotenv import load_dotenv

load_dotenv()

# # OAuth2.0 Authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

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

# # Function to validate username and password
def validate_user_password(username: str, password: str):
    # Replace this with your own dynamic authentication logic
    correct_username = os.getenv("USER_DETAIL", "test_user")
    correct_password = os.getenv("PASSWORD", "test_password")

    return username == correct_username and password == correct_password

# FastAPI endpoint to accept JSON payload
@app.post("/send-to-kafka")
async def send_to_kafka(username: str = Form(...), password: str = Form(...), token: str = Depends(oauth2_scheme), item_name: str = Form(...), item_description: str = Form(None)):
    # Validate the token
    if token != "test_token":
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Validate the username and password using the custom validation function
    if not validate_user_password(username, password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # preparing request payload from form-data
    payload = {
        "name":item_name,
        "description":item_description
    }

    json_payload = json.dumps(payload)

    # Send the payload to Kafka
    producer.send(TOPIC_NAME, value=json_payload.encode("utf-8"))

    return {"message": "Payload sent to Kafka"}

if __name__ == "__main__":
    # Run the FastAPI application
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
