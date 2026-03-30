from sqlalchemy import Column, String
from data.clients.postgres_client import Base
import uuid

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, nullable=False)
    name = Column(String)
    picture = Column(String)
    google_id = Column(String, unique=True, nullable=False)