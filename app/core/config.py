"""
Core configuration for the Product Enrichment application.
"""

import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Application configuration."""
    
    # Azure OpenAI Settings
    AZURE_OPENAI_ENDPOINT: str = os.getenv("AZURE_OPENAI_ENDPOINT", "")
    AZURE_OPENAI_API_KEY: str = os.getenv("AZURE_OPENAI_API_KEY", "")
    AZURE_OPENAI_DEPLOYMENT_NAME: str = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-4o")
    AZURE_OPENAI_API_VERSION: str = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview")
    CLASSIFIER_DEPLOYMENT: str = os.getenv("CLASSIFIER_DEPLOYMENT", "gpt-4o")
    ENRICHER_DEPLOYMENT: str = os.getenv("ENRICHER_DEPLOYMENT", "gpt-4o")
    OPENAI_TEMPERATURE: float = float(os.getenv("OPENAI_TEMPERATURE", "0.3"))
    
    # Server Settings
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    
    # Excel Settings
    INPUT_PRODUCTS_PATH: str = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "data",
        "products.xlsx"
    )
    
    @classmethod
    def validate(cls):
        """Validate required configuration."""
        if not cls.AZURE_OPENAI_API_KEY:
            raise ValueError("AZURE_OPENAI_API_KEY is required in .env file")
        if not cls.AZURE_OPENAI_ENDPOINT:
            raise ValueError("AZURE_OPENAI_ENDPOINT is required in .env file")
        return True


config = Config()
