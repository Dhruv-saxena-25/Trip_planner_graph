from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.chat_models import ChatOpenAI
from langchain_groq import ChatGroq
import os 

def get_llm(provider: str, model: str, api_keys: dict):
    if provider == "OpenAI":
        return ChatOpenAI(model=model, temperature=0.7)
    elif provider == "Groq":        
        return ChatGroq(model=model, api_key=api_keys["GROQ_API_KEY"], temperature=0.7)
    elif provider == "Gemini":
        os.environ["GOOGLE_API_KEY"] = api_keys["GOOGLE_API_KEY"]
        return ChatGoogleGenerativeAI(model=model)
    else:
        raise ValueError("Unsupported provider.")
