from fastapi import FastAPI
from src.controllers.controller import router as cryptocurrencies_router

app = FastAPI()

app.include_router(cryptocurrencies_router)