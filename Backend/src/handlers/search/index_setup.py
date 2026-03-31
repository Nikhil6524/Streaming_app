from handlers.search.opensearch_client import client

INDEX_NAME = "videos"


def create_index():
    if client.indices.exists(INDEX_NAME):
        return

    body = {
        "settings": {
            "index": {
                "number_of_shards": 1
            }
        },
        "mappings": {
            "properties": {
                "title": {
                    "type": "text"
                },
                "video_id": {
                    "type": "keyword"
                },
                "hls_url": {
                    "type": "keyword"
                }
            }
        }
    }

    client.indices.create(index=INDEX_NAME, body=body)