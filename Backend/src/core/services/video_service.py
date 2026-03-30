from handlers.storage.s3_client import S3Client
from data.repositories.video_repo import VideoRepository
import uuid


class VideoService:
    def __init__(self, repo: VideoRepository):
        self.repo = repo
        self.s3 = S3Client()

    def upload_video(self, file, user_id: str, title: str):
        filename = f"{uuid.uuid4()}.mp4"

        url = self.s3.upload_file(file.file, filename)

        video = self.repo.create_video({
            "title": title,
            "url": url,
            "owner_id": user_id
        })

        return video
    def list_videos(self):
        return self.repo.get_all_videos()