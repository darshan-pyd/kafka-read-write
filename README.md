# FastAPI with Kafka Integration

This project demonstrates the integration of [FastAPI](https://fastapi.tiangolo.com/) with [Apache Kafka](https://kafka.apache.org/) for asynchronous messaging.

## Prerequisites

Before running the application, ensure that you have the following installed:

- [Apache Kafka](https://kafka.apache.org/)
- [Python](https://www.python.org/) (preferably Python 3.7 or higher)
- [Mongodb](https://www.mongodb.com/docs/manual/installation/) or [Use docker image of mongodb](https://hub.docker.com/_/mongo)

## Getting Started

## Installation Steps

### 1. Clone repository
    - $ git clone <git-url> --branch main

### 2. Move to directory
    - cd <project_dir>

### 3. Add env file
    - Need to create `.env` file at root level
        - cp sample.env .env (mac/linux)
        - copy sample.env .env (windows)

### 4. Create virtualenv & activate virtualenv
Create virtual enviroment for Django with the help of `virtualenv` if you don't have it installed virtualenv you can install by
```bash
~/pip3 install virtualenv
```

```bash
~/virtualenv -p python3 env
```

```bash
~/source env/bin/activate (mac/linux)
> \env\Scripts\activate.bat (windows)
```

### 5. Install required library
(env)$ pip3 install -r requirements.txt


### 6. Start Zookeeper

```bash
~/kafka_2.13-3.0.0/bin/zookeeper-server-start.sh ~/kafka_2.13-3.0.0/config/zookeeper.properties

This command starts Zookeeper, which is required for Kafka coordination. Run in seperate terminal
```

### 7. Start Kafka Server
```bash
~/kafka_2.13-3.0.0/bin/kafka-server-start.sh ~/kafka_2.13-3.0.0/config/server.properties

This command starts the Kafka server, the central component of the Kafka ecosystem. Run in seperate terminal
```

### 8. Run FastAPI Application
uvicorn main:app --reload

This command starts the FastAPI application using the Uvicorn ASGI server. Run in seperate terminal

### 9. Run Kafka Consumer
python kafka_consumer.py

This command starts the Kafka consumer process, which reads messages from a Kafka topic and performs actions, such as inserting data into a MongoDB database. Run in seperate terminal


### Application Details
    - The FastAPI application is running at http://localhost:8000.
    - Kafka topics and configuration are defined in the Kafka server properties.
    - The Kafka consumer is configured in kafka_consumer.py.

### Usage
    - Access the FastAPI Swagger documentation at http://localhost:8000/docs for API details.
    - API will read token from Authorization header. Add header as `Authorization Bearer test_token`
    - Produce messages to the Kafka topic using your producer application.
    - The Kafka consumer will process messages and insert data into the configured database

### Kafka Producer
    - In a separate terminal or application, use a Kafka producer to send messages to the configured Kafka topic.

### Cleanup
    - To stop the processes, use Ctrl+C in the terminal.

### Additional Notes
    - Make sure to customize configuration files and scripts based on your specific requirements.
    - Adjust Kafka topic names, database configurations, and other settings as needed.
