import os
import json

from confluent_kafka import Consumer

from config.settings import settings
from handlers.storage.s3_client import S3Client
from utils.transcoder import generate_hls, generate_thumbnail
from handlers.search.index_video import index_video

from data.clients.postgres_client import SessionLocal
from data.models.postgres.video_model import Video


TEMP_DIR = "temp"


# =========================
# PROCESS VIDEO
# =========================
def process_video(data):
    """
    Main worker logic:
    1. Download video from S3
    2. Transcode to HLS
    3. Upload processed files to S3
    4. Update DB
    5. Index in OpenSearch
    """

    video_id = data["video_id"]
    s3_url = data["s3_url"]

    print(f"🎬 Processing video: {video_id}")

    s3 = S3Client()
    db = SessionLocal()

    try:
        # =========================
        # 1. Extract S3 key
        # =========================
        s3_key = s3_url.split(".com/")[-1]

        os.makedirs(TEMP_DIR, exist_ok=True)

        input_path = os.path.join(TEMP_DIR, f"{video_id}.mp4")

        # =========================
        # 2. Download original video
        # =========================
        print("⬇ Downloading from S3...")
        s3.download_file(s3_key, input_path)

        # =========================
        # 3. Transcode (HLS)
        # =========================
        output_dir = os.path.join(TEMP_DIR, video_id)

        print("🎥 Transcoding...")
        master_playlist = generate_hls(input_path, output_dir)

        # =========================
        # 4. Generate thumbnail
        # =========================
        print("🖼 Generating thumbnail...")
        thumbnail_path = generate_thumbnail(input_path, output_dir)

        # =========================
        # 5. Upload ALL generated files
        # =========================
        print("⬆ Uploading processed files...")

        for root, _, files in os.walk(output_dir):
            for file in files:
                local_path = os.path.join(root, file)
                s3_key_out = f"processed/{video_id}/{file}"

                s3.upload_file(local_path, s3_key_out)

        # Construct HLS URL
        hls_url = f"https://{settings.aws_bucket_name}.s3.amazonaws.com/processed/{video_id}/master.m3u8"

        thumbnail_url = f"https://{settings.aws_bucket_name}.s3.amazonaws.com/processed/{video_id}/thumbnail.jpg"

        # =========================
        # 6. Update DB
        # =========================
        print("🗄 Updating DB...")

        video = db.query(Video).filter(Video.id == video_id).first()

        if video:
            video.hls_url = hls_url
            video.status = "processed"
            db.commit()

        else:
            print("❌ Video not found in DB")

        # =========================
        # 7. Index in OpenSearch
        # =========================
        print("🔍 Indexing in OpenSearch...")

        if video:
            index_video(video)

        print("✅ Processing complete!")

    except Exception as e:
        print("❌ PROCESSING ERROR:", str(e))

    finally:
        db.close()


# =========================
# KAFKA CONSUMER
# =========================
def run():
    print("🚀 Video Processor started...")

    conf = {
        "bootstrap.servers": settings.kafka_bootstrap_servers,
        "group.id": "video-group",
        "auto.offset.reset": "earliest",
        "security.protocol": "SSL",
        "ssl.ca.location": settings.kafka_ca_path,
        "ssl.certificate.location": settings.kafka_cert_path,
        "ssl.key.location": settings.kafka_key_path,
    }

    consumer = Consumer(conf)
    consumer.subscribe([settings.kafka_topic])

    while True:
        msg = consumer.poll(1.0)

        if msg is None:
            continue

        if msg.error():
            print("❌ Kafka Error:", msg.error())
            continue

        data = json.loads(msg.value().decode("utf-8"))

        process_video(data)


# =========================
# ENTRY POINT
# =========================
if __name__ == "__main__":
    run()