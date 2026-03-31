from handlers.storage.s3_client import S3Client
from data.repositories.video_repo import VideoRepository
import uuid
from handlers.kafka.producer import publish_event
from config.settings import settings


class VideoService:
    def __init__(self, repo: VideoRepository):
        self.repo = repo
        self.s3 = S3Client()

    def upload_video(self, file, user_id: str, title: str):
        """Upload a single video file to S3 and persist metadata.

        The caller provides a human-readable title which is stored
        alongside the generated filename URL.
        """

        filename = f"{uuid.uuid4()}.mp4"

        url = self.s3.upload_file(file.file, filename)

        video = self.repo.create_video({
            "title": title,
            "url": url,
            "owner_id": user_id,
        })
        video_data = {
        "video_id": video.id,
        "user_id": video.owner_id,
        "s3_url": video.url,
    }

        publish_event(settings.kafka_topic, video_data)

        return video
    def list_videos(self):
        return self.repo.get_all_videos()