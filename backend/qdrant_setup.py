from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance

QDRANT_URL = "http://localhost:6333"
COLLECTION_NAME = "organizational_knowledge"

client = QdrantClient(url=QDRANT_URL)


def create_collection():
    collections = client.get_collections().collections

    exists = any(
        collection.name == COLLECTION_NAME
        for collection in collections
    )

    if not exists:
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=384,
                distance=Distance.COSINE
            )
        )

        print(f"Collection '{COLLECTION_NAME}' created successfully")

    else:
        print(f"Collection '{COLLECTION_NAME}' already exists")