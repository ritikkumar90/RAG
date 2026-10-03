import os
from components.dataLoader import doc_loader
from components.chunks import doc_chunks
from components.vectorStore import store_in_chroma
from components.retriever import retrieve_docs
from components.llmModel import chat_with_llm

def main():
    print("Starting pipeline test...")
    
    # 0. Setup a test file
    test_file = "./docs/documents1.txt"
    if not os.path.exists(test_file):
        with open(test_file, "w") as f:
            f.write("RAG stands for Retrieval-Augmented Generation. It is a powerful AI technique.")
        print(f"Created a sample test file: {test_file}")

    # 1. DataLoader
    print("\n--- 1. Testing DataLoader ---")
    try:
        documents = doc_loader(test_file)
        print(f"✅ Success! Loaded {len(documents)} documents.")
    except Exception as e:
        print(f"❌ Failed at DataLoader: {e}")
        return

    # 2. Chunking
    print("\n--- 2. Testing Chunking ---")
    try:
        chunks = doc_chunks(documents)
        print(f"✅ Success! Created {len(chunks)} chunks.")
    except Exception as e:
        print(f"❌ Failed at Chunking: {e}")
        return

    # 3. Vector Store & Embeddings
    print("\n--- 3. Testing Vector Store (Chroma) & Embedding ---")
    try:
        # This will call the EmbeddingModel which uses the ngrok URL
        store_in_chroma(chunks)
        print("✅ Success! Stored chunks in ChromaDB.")
    except Exception as e:
        print(f"❌ Failed at Vector Store/Embedding: {e}")
        print("Hint: Check if your ngrok URL is active in .env")
        return

    # 4. Retriever
    query = "what is Generative AI"
    print(f"\n--- 4. Testing Retriever with query: '{query}' ---")
    try:
        retrieved_docs = retrieve_docs(query)
        print(f"✅ Success! Retrieved {len(retrieved_docs)} documents.")
        if retrieved_docs:
            print(f"Top doc snippet: {retrieved_docs[0].page_content[:50]}...")
    except Exception as e:
        print(f"❌ Failed at Retriever: {e}")
        return

    # 5. LLM Call
    print("\n--- 5. Testing LLM Call ---")
    try:
        context_texts = [doc.page_content for doc in retrieved_docs]
        context = "\n\n".join(context_texts)
        
        prompt = f"""
            Answer the user's question based on the following context. If the answer is not in the context, say you don't know.

            Context:
            {context}

            Question: {query}
            """
        
        response = chat_with_llm(prompt)
        answer = response.content if hasattr(response, "content") else str(response)
        print("✅ Success! LLM generated a response.")
        print(f"\nFinal Answer: {answer}")
        
    except Exception as e:
        print(f"❌ Failed at LLM Call: {e}")
        return

if __name__ == "__main__":
    main()