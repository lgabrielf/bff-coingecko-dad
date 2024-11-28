from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    COINGECKO_API_KEY: str
    FASTAPI_PREFIX: str = 'bff'
    FASTAPI_DEBUG: bool = False
    FASTAPI_DESCRIPTION: str = 'Backend for Frontend (BFF) para consumir a API CoinGecko, fornecendo endpoints otimizados para listagem de criptomoedas, resumo de mercado e histórico de preços.'
    FASTAPI_TITLE: str = 'Backend for Frontend - Desafio Técnico'
    JWT_SECRET: str = 'JZDsEmQ0XsTDH8MCMXQzvsnlNrQanGV5QM4z6j6dpFk'
    DB_USERNAME: str = 'DB_USERNAME'
    DB_PASSWORD: str = 'DB_PASSWORD'
    DB_IPADDRES: str = '127.0.0.1'
    DB_PORT: str = '5432'
    DB_SCHEMA: str = 'SCHEMA'
    ALGORITHM: str = 'HS256'
    # token válido por 1 semana (em minutos)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7
    """
    import secrets 
    token: str = secrets.token_urlsafe(32)
    """

    @property
    def DB_URL(self) -> str:
        return f'postgresql+asyncpg://{self.DB_USERNAME}:{self.DB_PASSWORD}@{self.DB_IPADDRES}:{self.DB_PORT}/{self.DB_SCHEMA}'

    model_config = SettingsConfigDict(
        case_sensitive=True,
        extra='ignore',
        env_file=('.env.test', '.env.staging', '.env', '.env.prod'),
        env_file_encoding='utf-8',
    )


settings = Settings(_env_file='.env', _env_file_encoding='utf-8')
print(settings.DB_URL)