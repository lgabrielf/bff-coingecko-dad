from pydantic import BaseModel
from typing import List

class CryptocurrencyItem(BaseModel):
    name: str
    symbol: str
    price: float
    market_cap: int

class CryptocurrencyResponse(BaseModel):
    current_page: int
    cryptocurrencies: List[CryptocurrencyItem]