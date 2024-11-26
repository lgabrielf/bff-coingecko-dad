from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    COINGECKO_API_KEY: str
    FASTAPI_PREFIX: str = 'bff'    
    FASTAPI_DEBUG: bool = False
    FASTAPI_DESCRIPTION: str = (
        'Backend for Frontend (BFF) para consumir a API CoinGecko, fornecendo endpoints otimizados para listagem de criptomoedas, resumo de mercado e histórico de preços.'
    )
    FASTAPI_TITLE: str = 'Backend for Frontend - Desafio Técnico'

    model_config = SettingsConfigDict(
        case_sensitive=True,
        extra='ignore',
        env_file=('.env.test', '.env.staging', '.env', '.env.prod'),
        env_file_encoding='utf-8',
    )

settings = Settings(_env_file='.env', _env_file_encoding='utf-8')