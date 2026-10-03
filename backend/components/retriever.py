from langchain_chroma import Chroma
# from components.embedFunction import EmbeddingModel
from langchain_huggingface import HuggingFaceEmbeddings


embedding=HuggingFaceEmbeddings(model="BAAI/bge-small-en-v1.5")
def get_retriever(persist_directory="./chroma_db", search_kwargs=None):
    """
    Initializes and returns a retriever from the Chroma vector store.
    """
    if search_kwargs is None:
        search_kwargs = {"k": 4}  # default to retrieving top 4 documents
        
    vectorstore = Chroma(
        persist_directory=persist_directory,
        embedding_function=embedding
    )
    
    return vectorstore.as_retriever(search_kwargs=search_kwargs)

def retrieve_docs(query, persist_directory="./chroma_db", search_kwargs=None):
    """
    Convenience function to retrieve documents for a given query directly.
    """
    retriever = get_retriever(persist_directory, search_kwargs)
    return retriever.invoke(query)
