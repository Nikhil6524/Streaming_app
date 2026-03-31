from pydantic_settings import BaseSettings
from pathlib import Path

# Points to Backend root
BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    # DATABASE
    database_url: str

    # AUTH
    google_client_id: str

    # AWS S3
    aws_access_key_id: str
    aws_secret_access_key: str
    aws_region: str
    aws_bucket_name: str

    # Kafka
    kafka_bootstrap_servers: str
    kafka_topic: str

    kafka_ca_path: str
    kafka_cert_path: str
    kafka_key_path: str

    opensearch_host: str
    opensearch_port: int
    opensearch_user: str
    opensearch_password: str

    class Config:
        env_file = BASE_DIR / ".env"
        env_file_encoding = "utf-8"


settings = Settings()

#  ADD THIS PART
settings.kafka_ca_path = str(BASE_DIR / settings.kafka_ca_path)
settings.kafka_cert_path = str(BASE_DIR / settings.kafka_cert_path)
settings.kafka_key_path = str(BASE_DIR / settings.kafka_key_path)