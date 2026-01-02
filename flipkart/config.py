import os
from dotenv import load_dotenv
load_dotenv() #hugging face api key will be loaded by this

class Config:
        ASTRA_DB_API_ENDPOINT = os.getenv("ASTRA_DB_API_ENDPOINT")
        ASTRA_DB_APPLICATION_TOKEN = os.getenv("ASTRA_DB_APPLICATION_TOKEN")
        ASTRA_DB_KEY_SPACE = os.getenv("ASTRA_DB_KEY_SPACE")
        # UGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
        GROQ_API_KEY = os.getenv("GROQ_API_KEY")
        EMBEDDING_MODEL = "BAAI/bge-base-en-v1.5"
        RAG_MODEL = "llama-3.1-8b-instant"