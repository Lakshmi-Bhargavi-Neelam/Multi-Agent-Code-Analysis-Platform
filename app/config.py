import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq


load_dotenv()


class Config:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY")
    LANGCHAIN_TRACING_V2 = "true"
    LANGCHAIN_PROJECT = "code-analysis-agent"

    MODEL_NAME = "llama-3.1-8b-instant"
    @classmethod
    def get_llm(cls):
        return ChatGroq(
            groq_api_key=cls.GROQ_API_KEY,
            model_name=cls.MODEL_NAME,
            temperature=0.7
        )