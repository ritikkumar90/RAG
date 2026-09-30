import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")


def chat_with_llm(query, model_name="openai/gpt-oss-20b", temperature=0.3):
    """
    Convenience function to directly chat with the LLM using Groq.
    """
    if not groq_api_key:
        raise ValueError("GROQ_API_KEY not found in environment variables.")
        
    llm_model = ChatGroq(
        model=model_name,
        temperature=temperature,
        api_key=groq_api_key,
        max_retries=1
    )
    response = llm_model.invoke(query)
    return response
