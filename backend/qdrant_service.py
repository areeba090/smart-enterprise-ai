# pyrefly: ignore [missing-import]
from qdrant_client import QdrantClient
# pyrefly: ignore [missing-import]
from qdrant_client.models import Distance, VectorParams, PointStruct

from embeddings import generate_embedding


QDRANT_URL = "http://localhost:6333"
COLLECTION_NAME = "organizational_knowledge"

client = QdrantClient(url=QDRANT_URL)


def create_collection():
    collections = client.get_collections().collections

    existing_collections = [collection.name for collection in collections]

    if COLLECTION_NAME not in existing_collections:
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=384,
                distance=Distance.COSINE
            )
        )


def add_knowledge(document_id, title, category, content, source):
    vector = generate_embedding(content)

    point = PointStruct(
        id=document_id,
        vector=vector,
        payload={
            "title": title,
            "category": category,
            "content": content,
            "source": source
        }
    )

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=[point]
    )


def search_knowledge(query: str, limit: int = 3):
    query_vector = generate_embedding(query)

    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=limit
    ).points

    return results