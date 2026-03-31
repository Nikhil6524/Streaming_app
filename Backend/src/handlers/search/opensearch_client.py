from opensearchpy import OpenSearch
from config.settings import settings

client = OpenSearch(
    hosts=[{
        "host": settings.opensearch_host,
        "port": settings.opensearch_port
    }],
    http_auth=(settings.opensearch_user, settings.opensearch_password),
    use_ssl=True,
    verify_certs=True
)