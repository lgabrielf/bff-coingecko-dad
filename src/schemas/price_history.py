from pydantic import BaseModel
from typing import List


class PriceHistoryItemDTO(BaseModel):
    date: str
    price: float


class CryptocurrencyHistoryResponseDTO(BaseModel):
    id: str
    symbol: str
    currency: str
    history: List[PriceHistoryItemDTO]
