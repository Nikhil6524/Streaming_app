from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from data.clients.postgres_client import get_db
from data.repositories.video_repo import VideoRepository
from core.services.video_service import VideoService

router = APIRouter(prefix="/videos", tags=["Videos"])


def get_video_service(db: Session = Depends(get_db)):
    repo = VideoRepository(db)
    return VideoService(repo)


@router.get("/")
def get_videos(service: VideoService = Depends(get_video_service)):
    videos = service.list_videos()

    return [
        {
            "id": v.id,
            "url": v.url,
            "title": v.title
        }
        for v in videos
    ]