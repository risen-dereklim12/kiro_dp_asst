from requests.utils import proxy_bypass_environment
from Model import Model
from flask import Flask, request, jsonify
import json

question = "What is PDPA?"
model = Model("Derek")
response = model.respond(question)
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

print(message)