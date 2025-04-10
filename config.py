from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    GNEWS_API_KEY = os.getenv('GNEWS_API_KEY')
    GROQ_API_KEY = os.getenv('GROQ_API_KEY')
    MODEL_NAME = os.getenv('MODEL_NAME')
    EMBEDDING_MODEL = os.getenv('EMBEDDING_MODEL')
    
    @staticmethod
    def validate():
        required_keys = [
            ('GNEWS_API_KEY', Config.GNEWS_API_KEY),
            ('GROQ_API_KEY', Config.GROQ_API_KEY)
        ]
        
        missing = [name for name, value in required_keys if not value]
        if missing:
            raise ValueError(f"Missing required environment variables: {', '.join(missing)}")