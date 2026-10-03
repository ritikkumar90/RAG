from langchain_chroma import Chroma
from components.embedFunction import EmbeddingModel
from langchain_huggingface import HuggingFaceEmbeddings

embedding = HuggingFaceEmbeddings(
    model = "BAAI/bge-small-en-v1.5"
)
def store_in_chroma(chunks, embedding_model=embedding, persist_directory="./chroma_db"):
    # This automatically embeds your chunks and saves them to the disk
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        persist_directory=persist_directory
    )
    print(f"Successfully saved {len(chunks)} chunks to ChromaDB in {persist_directory}!")
    return vectorstore
