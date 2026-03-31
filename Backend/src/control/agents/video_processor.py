import os
import sys

# Allow running this worker as a script from Backend/src without package setup.
SRC_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if SRC_ROOT not in sys.path:
    sys.path.insert(0, SRC_ROOT)

from handlers.kafka.consumer import start_consumer
from core.services.transcode_service import process_video_task


def process_video(data):
    video_id = data.get("video_id")
    print(f"🎬 Processing video: {video_id}")
    process_video_task(data)


def run():
    print(" Video Processor Worker started...")

    start_consumer(process_video)


if __name__ == "__main__":
    run()