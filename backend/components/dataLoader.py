from langchain_community.document_loaders import TextLoader, PyPDFLoader, CSVLoader, WebBaseLoader
import os


def doc_loader(doc_path):
    # i have to extract extention so I can determine the file type
    if doc_path.startswith("http://") or doc_path.startswith("https://"):
        loader = WebBaseLoader(doc_path)
        return loader.load()

    _, extension = os.path.splitext(doc_path)
    extension = extension.lower()
    if extension==".txt":
        loader = TextLoader(doc_path)
    elif extension==".pdf":
        loader = PyPDFLoader(doc_path)
    elif extension == ".csv":
        loader =CSVLoader(doc_path)
    else: 
        raise ValueError(f"Unsupported file extension: {extension}")

    return loader.load()