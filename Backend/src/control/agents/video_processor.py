import os
from handlers.kafka.consumer import start_consumer
from handlers.storage.s3_client import download_file, upload_file
from utils.transcoder import generate_hls, generate_thumbnail

TEMP_DIR = "temp"


def process_video(data):
    video_id = data["video_id"]
    s3_url = data["s3_url"]

    print(f"🎬 Processing video: {video_id}")

    # Extract S3 key
    s3_key = s3_url.split(".com/")[-1]

    os.makedirs(TEMP_DIR, exist_ok=True)

    input_path = os.path.join(TEMP_DIR, f"{video_id}.mp4")

    # ⬇ Download from S3
    download_file(s3_key, input_path)

    # 🎥 Transcode (HLS)
    output_dir = os.path.join(TEMP_DIR, video_id)
    master_playlist = generate_hls(input_path, output_dir)

    # 🖼 Thumbnail
    thumbnail = generate_thumbnail(input_path, output_dir)

    # ⬆ Upload ALL generated files
    uploaded_urls = {}

    for root, _, files in os.walk(output_dir):
        for file in files:
            local_path = os.path.join(root, file)
            s3_key_out = f"processed/{video_id}/{file}"

            url = upload_file(local_path, s3_key_out)
            uploaded_urls[file] = url

    print("✅ Upload complete")

    print("📺 Master Playlist URL:")
    print(f"https://{data.get('bucket','')}.s3.amazonaws.com/processed/{video_id}/master.m3u8")


def run():
    print(" Video Processor Worker started...")

    start_consumer(process_video)


if __name__ == "__main__":
    run()