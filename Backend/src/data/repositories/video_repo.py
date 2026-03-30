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
    
    def update_hls_url(self, video_id, hls_url):
        video = self.db.query(Video).filter(Video.id == video_id).first()
        if video:
            video.hls_url = hls_url
            video.status = "processed"
            self.db.commit()