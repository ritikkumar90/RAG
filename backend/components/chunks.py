from langchain_text_splitters import RecursiveCharacterTextSplitter

def doc_chunks(documents):
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=50)
    chunks = splitter.split_documents(documents)
    return chunks

