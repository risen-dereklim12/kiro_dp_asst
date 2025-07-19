from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct, Filter, FieldCondition, MatchValue
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from DPBrain.Embedding import EmbeddingClass

# memory_size = number_of_vectors * vector_dimension * 4 bytes * 1.5
# Using 768 dimension vectors as I am using snowflake-arctic-embed:110m embedding model

class QdrantStore:
    def __init__(self, url="http://localhost:6333", collection_name="pdpa_collection", vector_size=768, distance=Distance.DOT):
        self.client = QdrantClient(url=url)
        self.collection_name = collection_name
        self.vector_size = vector_size
        self.distance = distance

    def create_collection(self):
        collections = self.client.get_collections().collections
        if any(c.name == self.collection_name for c in collections):
            print(f"Collection '{self.collection_name}' already exists.")
            return
        self.client.create_collection(
            collection_name=self.collection_name,
            vectors_config=VectorParams(size=self.vector_size, distance=self.distance),
        )
        print(f"Collection '{self.collection_name}' created.")

    def upsert(self, points):
        """
        points: list of PointStruct
        """
        operation_info = self.client.upsert(
            collection_name=self.collection_name,
            wait=True,
            points=points,
        )
        return operation_info

    def search(self, query_vector, city=None, limit=1):
        must_conditions = []
        if city:
            must_conditions.append(
                FieldCondition(
                    key="city",
                    match=MatchValue(value=city)
                )
            )
        query_filter = Filter(must=must_conditions) if must_conditions else None
        results = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            query_filter=query_filter,
            with_payload=True,
            limit=limit,
        )
        return results

if __name__ == "__main__":
    qdrant_client = QdrantStore()
    embedding = EmbeddingClass()
    encoded = embedding.encode("What is PDPA")
    # qdrant_client.create_collection()
    # points = [
    #     PointStruct(id=1, vector=[0.05, 0.61, 0.76, 0.74], payload={"city": "Berlin"}),
    # ]
    # operation_info = qdrant_client.upsert(points)
    # print(operation_info)
    search_result = qdrant_client.search(
        encoded["embeddings"][0]
        , limit=3)
    print(search_result)