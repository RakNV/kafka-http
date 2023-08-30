from pydantic import BaseSettings


class Kafka(BaseSettings):
    task_topic: str = "main_topic"
    bootstrap_servers: str = "kafka:9092"
    group_id: str = "main_service"
    consumer_timeout: int = 10000

    class Config:
        env_prefix = "KAFKA_"
        env_file = ".env"


class Service(BaseSettings):
    address: str = "0.0.0.0"
    port: int = 8080

    class Config:
        env_prefix = "SERVICE_"
        env_file = ".env"
