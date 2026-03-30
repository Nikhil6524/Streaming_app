from sqlalchemy import Column, String
from data.clients.postgres_client import Base
import uuid


class Video(Base):
    __tablename__ = "videos"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String)
    url = Column(String)
    owner_id = Column(String)