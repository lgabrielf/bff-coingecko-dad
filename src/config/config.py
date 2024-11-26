from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    coingecko_api_key: str

    class Config:
        env_file = ".env"  # Arquivo que contém as variáveis de ambiente

settings = Settings()