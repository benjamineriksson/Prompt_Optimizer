import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY')
    DEEPSEEK_API_URL = 'https://api.deepseek.com/v1/chat/completions'
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', '*')
    
    # Rate limiting
    REQUESTS_PER_MINUTE = 30
    
    # Model configuration
    DEFAULT_MODEL = 'deepseek-chat'
    REASONING_MODEL = 'deepseek-reasoner'
    
    @staticmethod
    def validate_config():
        """Validate that required configuration is present"""
        if not Config.DEEPSEEK_API_KEY:
            raise ValueError("DEEPSEEK_API_KEY environment variable is required")
        
        return True
