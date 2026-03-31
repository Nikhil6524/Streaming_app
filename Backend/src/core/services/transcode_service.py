import os
import shutil
from handlers.storage.s3_client import S3Client
from utils.transcoder import generate_hls, generate_thumbnail, generate_quality_mp4s
from data.clients.postgres_client import SessionLocal
from data.models.postgres.video_model import Video
from handlers.search.index_video import index_video

TEMP_DIR = "temp"


def process_video_task(data: dict):
    """Download original video, create renditions, and upload processed artifacts."""
    video_id = data["video_id"]
    s3_url = data["s3_url"]

    s3_client = S3Client()
    db = SessionLocal()

    s3_key = s3_client.get_s3_key_from_url(s3_url)
    if not s3_key:
        print("Could not extract S3 key from URL:", s3_url)
        return

    os.makedirs(TEMP_DIR, exist_ok=True)

    input_path = os.path.join(TEMP_DIR, f"{video_id}.mp4")
    output_dir = os.path.join(TEMP_DIR, video_id)

    try:
        s3_client.download_file(s3_key, input_path)

        # Generate processed outputs.
        generate_hls(input_path, output_dir)
        generate_quality_mp4s(input_path, output_dir)
        generate_thumbnail(input_path, output_dir)

        for root, _, files in os.walk(output_dir):
            for file_name in files:
                local_path = os.path.join(root, file_name)
                s3_key_out = f"processed/{video_id}/{file_name}"
                s3_client.upload_file(local_path, s3_key_out)

        # Refresh OpenSearch document with processed playback metadata.
        video = db.query(Video).filter(Video.id == video_id).first()
        if video:
            hls_key = f"processed/{video_id}/master.m3u8"
            hls_url = None
            if s3_client.object_exists(hls_key):
                hls_url = s3_client.generate_presigned_url(hls_key)

            # Keep index fresh even though DB model does not yet persist hls_url.
            if hls_url:
                setattr(video, "hls_url", hls_url)
            index_video(video)

        print(f"Transcoding complete for video_id={video_id}")
    except Exception as exc:
        print(f"Transcoding failed for video_id={video_id}: {exc}")
    finally:
        db.close()
        if os.path.exists(input_path):
            os.remove(input_path)
        if os.path.exists(output_dir):
            shutil.rmtree(output_dir, ignore_errors=True)
