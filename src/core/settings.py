import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    # Database settings
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://lambda_user:lambda_password@localhost:5432/lambda_db")
    
    # Security settings
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    
    # Application settings
    APP_NAME: str = os.getenv("APP_NAME", "Lambda AWS Python FastAPI")
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    
    # AWS settings
    AWS_REGION: str = os.getenv("AWS_REGION", "us-east-1")
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
