from sqlalchemy.orm import Session
from data.models.postgres.video_model import Video


class VideoRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_video(self, data: dict):
        video = Video(**data)
        self.db.add(video)
        self.db.commit()
        self.db.refresh(video)
        return video
    def get_all_videos(self):
        return self.db.query(Video).all()