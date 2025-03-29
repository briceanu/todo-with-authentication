from pydantic_settings import BaseSettings  

class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM : str  
 

    class Config:
        env_file = ".env"

# Create a settings instance
settings = Settings()