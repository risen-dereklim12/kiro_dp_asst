from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from DPBrain.Model import Model
from DPBrain.Embedding import EmbeddingClass
from DPRAGStore.QdrantStore import QdrantStore
import json

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}})

def search(question):
    qdrant_client = QdrantStore()
    embedding = EmbeddingClass()
    encoded = embedding.encode(question)
    search_result = qdrant_client.search(
        encoded["embeddings"][0]
        , limit=1)
    return search_result[0]

@app.route('/api/ask', methods=['POST', 'OPTIONS'])
@cross_origin(origins='http://localhost:5173')
def ask():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No JSON body found'}), 400
    question = data.get('question', '')
    model = Model("Derek")
    context = search(question)
    print(question)
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
    return jsonify({
        'question': question,
        'answer': f"{message}"
    })

if __name__ == '__main__':
    app.run(port=5000)
