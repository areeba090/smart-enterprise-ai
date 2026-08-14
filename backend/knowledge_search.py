# pyrefly: ignore [missing-import]
from qdrant_client import QdrantClient
from embeddings import generate_embedding
from qdrant_setup import COLLECTION_NAME


QDRANT_URL = "http://localhost:6333"

client = QdrantClient(url=QDRANT_URL)


def search_knowledge(query: str, limit: int = 3):

    query_vector = generate_embedding(query)

    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=limit
    ).points

    return results


if __name__ == "__main__":

    query = input("Enter your question: ")

    results = search_knowledge(query)

    for result in results:
        print("\nTitle:", result.payload.get("title"))
        print("Category:", result.payload.get("category"))
        print("Score:", result.score)
        print("Content:", result.payload.get("content"))