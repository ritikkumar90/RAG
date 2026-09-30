from langchain_chroma import Chroma
from components.embedFunction import EmbeddingModel
from dotenv import load_dotenv
import os


load_dotenv()
url = os.getenv("URL")
embedding_model = EmbeddingModel(url)
def get_retriever(persist_directory="./chroma_db", search_kwargs=None):
    """
    Initializes and returns a retriever from the Chroma vector store.
    """
    if search_kwargs is None:
        search_kwargs = {"k": 4}  # default to retrieving top 4 documents
        
    vectorstore = Chroma(
        persist_directory=persist_directory,
        embedding_function=embedding_model
    )
    
    return vectorstore.as_retriever(search_kwargs=search_kwargs)

def retrieve_docs(query, persist_directory="./chroma_db", search_kwargs=None):
    """
    Convenience function to retrieve documents for a given query directly.
    """
    retriever = get_retriever(persist_directory, search_kwargs)
    return retriever.invoke(query)
