from fastapi import FastAPI
from src.controllers import cryptocurrency
from src.controllers import market_summary
from src.controllers import price_history
from src.config.config import settings

app = FastAPI(
    title=settings.FASTAPI_TITLE,
    description=settings.FASTAPI_DESCRIPTION,
    debug=settings.FASTAPI_DEBUG,
    openapi_url=('/openapi.json' if settings.FASTAPI_DEBUG else None),
    docs_url=('/docs' if settings.FASTAPI_DEBUG else None),
    redoc_url=('/redocs' if settings.FASTAPI_DEBUG else None),
)

app.include_router(
    cryptocurrency.router,
    tags=['Top Cryptocurrencies'],
    prefix=f'/{settings.FASTAPI_PREFIX}',
)
app.include_router(
    market_summary.router,
    tags=['Cryptocurrency Market'],
    prefix=f'/{settings.FASTAPI_PREFIX}',
)
app.include_router(
    price_history.router,
    tags=['Cryptocurrency History'],
    prefix=f'/{settings.FASTAPI_PREFIX}',
)