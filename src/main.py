from fastapi import FastAPI
from controllers.currency import router as cryptocurrencies_router

app = FastAPI()

app.include_router(cryptocurrencies_router)