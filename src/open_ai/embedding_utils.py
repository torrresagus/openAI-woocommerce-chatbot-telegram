import os
import openai
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file


openai.api_key  = os.environ['OPENAI_API_KEY']

# Function to get the embedding of a text
def get_embedding(text, model="text-embedding-ada-002"):
    if len(text) == 0:
        return None
    response = openai.Embedding.create(input=[text], model=model)
    print(text , " -> embedding done")
    return response