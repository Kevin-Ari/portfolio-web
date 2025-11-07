from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # Database - PostgreSQL URL
    DATABASE_URL: str
    
    # API
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    RELOAD: bool = True
    
    # CORS
    ALLOWED_ORIGINS: str = "http://localhost:3000,http://127.0.0.1:3000"
    
    # Email (opcional)
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    EMAIL_FROM: str = ""
    EMAIL_PASSWORD: str = ""
    
    class Config:
        env_file = "../.env"
    
    @property
    def origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]

settings = Settings()