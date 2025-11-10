from confluent_kafka import Producer, Consumer
import json

KAFKA_BOOTSTRAP_SERVERS = "localhost:9092"
KAFKA_GROUP_ID = "inventory-service-group"


# src/kafka/config.py
def create_kafka_producer() -> Producer:
    producer_config = {
        "bootstrap.servers": "localhost:9092",
        "linger.ms": 5,  # Giảm latency
        "batch.num.messages": 100,
        "queue.buffering.max.ms": 50,
    }
    return Producer(producer_config)

def create_kafka_consumer(topics: list[str]) -> Consumer:
    consumer_config = {
        "bootstrap.servers": "localhost:9092",
        "group.id": "inventory-service-group",
        "auto.offset.reset": "earliest",
        "enable.auto.commit": True,
        "auto.commit.interval.ms": 1000,
    }
    consumer = Consumer(consumer_config)
    consumer.subscribe(topics)
    return consumer
