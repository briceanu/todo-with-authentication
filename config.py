from pydantic_settings import BaseSettings  # Correct import

class Settings(BaseSettings):
    THE_NAME: str
 

    class Config:
        env_file = ".env"

# Create a settings instance
settings = Settings()