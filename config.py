import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # LLM Settings
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai")
    
    # Database
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://localhost/preagent")
    CHROMA_PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR", "./database/chroma")
    
    # Redis
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    
    # Agent Config
    MAX_ITERATIONS = int(os.getenv("MAX_ITERATIONS", "5"))
    TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))
    MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4-turbo-preview")

config = Config()
