import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from DPRAGStore.QdrantStore import QdrantStore
from Embedding import EmbeddingClass
from requests.utils import proxy_bypass_environment
from Model import Model
from flask import Flask, request, jsonify
import json

def ask(question, context):
    model = Model("Derek")
    response = model.respond(question, context)
    message = ""
    for line in response.iter_lines(decode_unicode=True):
        if line:
            try:
                # Parse line as JSON object
                json_data = json.loads(line)
                # Print message content
                if "message" in json_data and "content" in json_data["message"]:
                        message += json_data["message"]["content"]
            except json.JSONDecodeError:
                message += f"\nFailed to parse line: {line}"

    return message

def search(question):
    qdrant_client = QdrantStore()
    embedding = EmbeddingClass()
    encoded = embedding.encode(question)
    search_result = qdrant_client.search(
        encoded["embeddings"][0]
        , limit=1)
    return search_result[0]

if __name__ == "__main__":
    question = "what is Part 2 of PDPA?"
    context = search(question)
    context = context.payload['text']
    answer = ask(question, context)
    print(answer)
    # search_result = search("Who governs PDPA?")
    # print(search_result.payload['text'])