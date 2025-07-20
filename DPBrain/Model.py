import requests
import json

class Model:
    def __init__(self, model_name):
        # Base URL for the local Ollama API
        self.url = "http://localhost:11434/api/chat"
        self.model_name = model_name

    def respond(self, question, context): 
        template = f"Answer this question: {question} based on this context: {context}. If the context does not answer \
            the question, reply `This question is not found in my knowledge base.`"
        # Define the model and the input prompt
        payload = {
            "model": self.model_name,
            "messages": [ # Can set chat history in messages https://ollama.readthedocs.io/en/api/#generate-a-chat-completion
                    {
                        "role": "user", # system, user, assistant, or tool
                        "content": f"{template}",
                        # "images": [], list of images
                        # "tool_calls": [] # a list of tools the model wants to use
                    }
                ],
            # "raw": True, # Disable templating
            # "options": [], # additional model parameters listed in the documentation for the Modelfile such as temperature
            # "tools": [], # Streaming must be set to False if calling tools
            # stream: True, # if false the response will be returned as a single response object, rather than a stream of objects
            # keep_alive: 10, # controls how long the model will stay loaded into memory following the request (default: 5m)
        }

        # To grab responses as they are retrieved, set streaming to true
        response = requests.post(self.url, json=payload, stream=True)

        return response