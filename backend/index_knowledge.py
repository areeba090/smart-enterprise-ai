# pyrefly: ignore [missing-import]
from qdrant_client import QdrantClient
# pyrefly: ignore [missing-import]
from qdrant_client.models import PointStruct

from mongodb import db
from embeddings import generate_embedding
from qdrant_setup import create_collection, COLLECTION_NAME


QDRANT_URL = "http://localhost:6333"

client = QdrantClient(url=QDRANT_URL)


def index_knowledge():

    # Delete old collection so old embeddings are not mixed
    # with the new clean embeddings.
    collections = client.get_collections().collections

    exists = any(
        collection.name == COLLECTION_NAME
        for collection in collections
    )

    if exists:
        client.delete_collection(COLLECTION_NAME)
        print("Old collection deleted")

    # Create a fresh collection
    create_collection()

    # Get knowledge documents except the mixed/duplicate document
    documents = list(
        db.organizational_knowledge.find(
            {
                "title": {
                    "$ne": "Organizational Business and Technical Knowledge"
                }
            }
        )
    )

    points = []

    for index, document in enumerate(documents):

        content = document.get("content", "")

        vector = generate_embedding(content)

        payload = {
            "title": document.get("title"),
            "category": document.get("category"),
            "source": document.get("source"),
            "content": content,
            "access_level": document.get("access_level"),
            "created_at": str(document.get("created_at"))
        }

        points.append(
            PointStruct(
                id=index + 1,
                vector=vector,
                payload=payload
            )
        )

    if points:
        client.upsert(
            collection_name=COLLECTION_NAME,
            points=points
        )

    print(
        f"{len(points)} knowledge documents indexed successfully"
    )


if __name__ == "__main__":
    index_knowledge()