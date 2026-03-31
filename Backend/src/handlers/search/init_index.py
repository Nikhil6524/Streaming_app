from handlers.search.opensearch_client import client

INDEX_NAME = "videos"


def create_index():
    if client.indices.exists(INDEX_NAME):
        print("Index already exists")
        return

    body = {
        "settings": {
            "index": {
                "number_of_shards": 1
            }
        },
        "mappings": {
            "properties": {
                "video_id": {"type": "keyword"},
                "title": {"type": "text"},
                "hls_url": {"type": "keyword"}
            }
        }
    }

    client.indices.create(index=INDEX_NAME, body=body)
    print("Index created ✅")


if __name__ == "__main__":
    create_index()