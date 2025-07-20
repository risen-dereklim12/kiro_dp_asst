import ollama
from qdrant_client.grpc import Document
import sys
import os
import json
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pathlib import Path

class EmbeddingClass:
    def __init__(self, model="snowflake-arctic-embed:110m"):
        self.model = model

    def embed(self, documents):
        vectors = []
        # store each document in a vector embedding database
        for i, d in enumerate(documents):
            response = ollama.embed(model="snowflake-arctic-embed:110m", input=d["text"])
            vector = response["embeddings"]
            if response["embeddings"]:
                if isinstance(vector[0], list):  # it's a list of lists
                    vectors.append(vector[0])
            else:
                print("No embeddings in response", {type(response)})
        return vectors

    def encode(self, input_text):
        response = ollama.embed(model="snowflake-arctic-embed:110m", input=input_text)
        return response

if __name__ == "__main__":
    embedding = EmbeddingClass()
    file_path = Path.home() / "kiro_dp_asst" / "Documents" / "document1.json"
    with file_path.open("r") as file:
        data = file.read()
    documents = json.loads(data)
    vectors = embedding.embed(documents)
    print(vectors)
    # # for p in points:
    # #     operation_info = embedding.qdrant_client.upsert(points)
    # #     print(operation_info)
    # search_result = embedding.search_vector(points, limit=1)
    # if search_result:
    #     print(search_result[0].payload['text'])
    # else:
    #     print("No results found or search_result is None")
    # encoded = embedding.encode("What is PDPA")
    # print(encoded["embeddings"][0])