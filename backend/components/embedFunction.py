# from langchain_google_genai import GoogleGenerativeAIEmbeddings 
import os
# from dotenv import load_dotenv
from langchain_core.embeddings import Embeddings
import requests
from typing import List

class EmbeddingModel(Embeddings):
    def __init__(self, url):
        self.url = url

    def embed_documents(self, texts: List[str])-> List[List[float]]:
        payload = {"texts":texts}
        response = requests.post(url=self.url, json=payload)
        if response.ok:
            vectors=response.json()["embeddings"]
            return vectors
        else:
            raise Exception(f"API Error {response.status_code}: {response.text}")

    def embed_query(self, text: str)->List[List[float]]:
        return self.embed_documents([text])[0]


# load_dotenv()

# def doc_embed():
#     # We just need to return the model itself. ChromaDB will use it to embed!
#     embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
#     return embeddings
