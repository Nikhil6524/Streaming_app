from handlers.search.opensearch_client import client

print(client.info())
print(client.indices.exists(index="videos"))