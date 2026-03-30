from confluent_kafka import Producer
from config.settings import settings
import json

conf = {
    "bootstrap.servers": settings.kafka_bootstrap_servers,
    "security.protocol": "SSL",
    "ssl.ca.location": settings.kafka_ca_path,
    "ssl.certificate.location": settings.kafka_cert_path,
    "ssl.key.location": settings.kafka_key_path,
}

producer = Producer(conf)


def publish_event(topic: str, data: dict):
    try:
        producer.produce(topic, json.dumps(data).encode("utf-8"))
        producer.flush()
        print("Event published:", data)
    except Exception as e:
        print("Kafka publish error:", str(e))