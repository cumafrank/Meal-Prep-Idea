import os
import dotenv
from dotenv import load_dotenv, find_dotenv

import cohere

#_ = load_dotenv(find_dotenv())

co = cohere.Client(os.environ["COHERE_API_KEY"]) # Your Cohere API key

response = co.chat(message="Hello", model="command-r-plus")
print(response.text)