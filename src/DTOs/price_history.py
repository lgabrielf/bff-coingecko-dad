from pydantic import BaseModel
from typing import List

class PriceHistoryItem(BaseModel):
    date: str
    price: float

class CryptocurrencyHistory(BaseModel):
    id: str
    symbol: str
    currency: str
    history: List[PriceHistoryItem]
