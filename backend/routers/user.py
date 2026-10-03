from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from schemas import QueryRequest
import os
import shutil

from components.dataLoader import doc_loader
from components.chunks import doc_chunks
from components.vectorStore import store_in_chroma
from components.retriever import retrieve_docs
from components.llmModel import chat_with_llm

router = APIRouter(prefix="/user")

@router.post("/upload", summary="Upload a document to the RAG pipeline")
async def upload_document(file: UploadFile = File(...)):
    try:
        # Create docs directory if it doesn't exist
        os.makedirs("./docs", exist_ok=True)
        file_path = f"./docs/{file.filename}"
        
        # Save the uploaded filet 
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # 1. DataLoader
        documents = doc_loader(file_path)
        
        # 2. Chunking
        chunks = doc_chunks(documents)
        
        # 3. Store in ChromaDB
        store_in_chroma(chunks)
        
        return {"message": f"Successfully processed and stored {len(chunks)} chunks from {file.filename}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/ask", summary="Ask a question about the uploaded documents")
async def ask_question(request: QueryRequest):
    try:
        query = request.query
        
        # Retrieve relevant documents
        retrieved_docs = retrieve_docs(query)
        
        if not retrieved_docs:
            return {"answer": "No relevant documents found in the database.", "context": []}
            
        # Combine retrieved documents into a single string for context
        context_texts = [doc.page_content for doc in retrieved_docs]
        context = "\n\n".join(context_texts)
        
        # Create the final prompt with both context and the query
        prompt = f"""
            Answer the user's question based on the following context. If the answer is not in the context, say you don't know.

            Context:
            {context}

            Question: {query}
            """

        # Pass the combined prompt to the LLM
        response = chat_with_llm(prompt)
        
        # Handle LangChain's AIMessage response object
        answer = response.content if hasattr(response, "content") else str(response)
        
        return {
            "answer": answer,
            "context": context_texts
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
