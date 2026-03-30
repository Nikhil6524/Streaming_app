from confluent_kafka import Consumer
from config.settings import settings
import json

conf = {
    "bootstrap.servers": settings.kafka_bootstrap_servers,
    "group.id": "video-group",
    "auto.offset.reset": "earliest",
    "security.protocol": "SSL",
    "ssl.ca.location": settings.kafka_ca_path,
    "ssl.certificate.location": settings.kafka_cert_path,
    "ssl.key.location": settings.kafka_key_path,
}

consumer = Consumer(conf)
consumer.subscribe([settings.kafka_topic])


def start_consumer(process_function):
    print(" Kafka Consumer started...")

    while True:
        msg = consumer.poll(1.0)

        if msg is None:
            continue

        if msg.error():
            print(" Kafka error:", msg.error())
            continue

        data = json.loads(msg.value().decode("utf-8"))

        process_function(data)