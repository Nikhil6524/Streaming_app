from handlers.search.opensearch_client import client
from handlers.storage.s3_client import S3Client

INDEX_NAME = "videos"


def search_videos(query: str):
    try:
        s3_client = S3Client()

        body = {
            "query": {
                "match": {
                    "title": {
                        "query": query,
                        "fuzziness": "AUTO"
                    }
                }
            }
        }

        res = client.search(index=INDEX_NAME, body=body)

        items = []

        for hit in res["hits"]["hits"]:
            source = hit["_source"]
            video_id = source.get("video_id")
            hls_url = source.get("hls_url")
            base_url = source.get("url")

            # If index has no hls_url yet, derive it from processed assets if present.
            if video_id and not hls_url:
                hls_key = f"processed/{video_id}/master.m3u8"
                if s3_client.object_exists(hls_key):
                    hls_url = s3_client.generate_presigned_url(hls_key)

            # Return a playable URL even when stored URL is private.
            if base_url:
                base_key = s3_client.get_s3_key_from_url(base_url)
                if base_key:
                    try:
                        base_url = s3_client.generate_presigned_url(base_key)
                    except Exception:
                        pass

            items.append(
                {
                    "id": video_id,
                    "title": source.get("title"),
                    "hls_url": hls_url,
                    "url": base_url,
                }
            )

        return items

    except Exception as e:
        print("SEARCH ERROR:", str(e))
        return {"error": str(e)}