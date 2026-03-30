from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from data.clients.postgres_client import get_db
from data.repositories.video_repo import VideoRepository
from core.services.video_service import VideoService
from handlers.storage.s3_client import S3Client

router = APIRouter(prefix="/videos", tags=["Videos"])


def get_video_service(db: Session = Depends(get_db)):
    repo = VideoRepository(db)
    return VideoService(repo)


@router.get("/")
def get_videos(service: VideoService = Depends(get_video_service)):
    videos = service.list_videos()
    s3_client = S3Client()

    def to_playable_url(url: str):
        s3_key = s3_client.get_s3_key_from_url(url)

        if not s3_key:
            return url

        try:
            return s3_client.generate_presigned_url(s3_key)
        except Exception:
            # Fallback to stored URL if signing fails for any reason.
            return url

    response = []

    for v in videos:
        playable_url = to_playable_url(v.url)
        response.append(
            {
                "id": v.id,
                "url": playable_url,
                "title": v.title,
                "quality_urls": {
                    "360p": playable_url,
                    "480p": playable_url,
                    "720p": playable_url,
                },
            }
        )

    return response