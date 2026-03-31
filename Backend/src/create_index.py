from handlers.search.opensearch_client import client

INDEX_NAME = "videos"

# Delete if exists (safe reset)
if client.indices.exists(index=INDEX_NAME):
    client.indices.delete(index=INDEX_NAME)
    print("Old index deleted")

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

response = client.indices.create(index=INDEX_NAME, body=body)
print("CREATE RESPONSE:", response)

print("Index exists now?:", client.indices.exists(index=INDEX_NAME))