from handlers.search.opensearch_client import client

INDEX_NAME = "videos"


def index_video(video):
    hls_url = getattr(video, "hls_url", None)
    fallback_url = getattr(video, "url", None)

    doc = {
        "video_id": video.id,
        "title": video.title,
        "hls_url": hls_url,
        "url": fallback_url,
    }

    client.index(
        index=INDEX_NAME,
        id=video.id,
        body=doc
    )