from pydantic_settings import BaseSettings
from pydantic import field_validator
from typing import List, Union
import os

class Settings(BaseSettings):
    database_url: str
    gemini_api_key: str
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    cors_origins: Union[str, List[str]] = "http://localhost:3000,http://localhost:5173"
    environment: str = "development"
    
    class Config:
        env_file = ".env"
        
    @field_validator('cors_origins', mode='before')
    @classmethod
    def parse_cors_origins(cls, v):
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(',')]
        return v

settings = Settings()
