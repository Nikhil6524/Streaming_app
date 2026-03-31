from data.clients.postgres_client import SessionLocal
from data.models.postgres.video_model import Video
from handlers.search.index_video import index_video


def run_backfill():
    db = SessionLocal()

    try:
        videos = db.query(Video).all()
        print(f"Found {len(videos)} videos in DB")

        indexed = 0
        failed = 0

        for video in videos:
            try:
                index_video(video)
                indexed += 1
            except Exception as exc:
                failed += 1
                print(f"Failed to index video_id={video.id}: {exc}")

        print(f"Backfill complete. indexed={indexed}, failed={failed}")
    finally:
        db.close()


if __name__ == "__main__":
    run_backfill()
