from langchain_chroma import Chroma
from components.embedFunction import EmbeddingModel
from dotenv import load_dotenv
import os

load_dotenv()

url = os.getenv("URL")
# Safe initialization in case URL is not set yet
embedding_model = EmbeddingModel(url) if url else None

def store_in_chroma(chunks, embedding_model=embedding_model, persist_directory="./chroma_db"):
    # This automatically embeds your chunks and saves them to the disk
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        persist_directory=persist_directory
    )
    print(f"Successfully saved {len(chunks)} chunks to ChromaDB in {persist_directory}!")
    return vectorstore
