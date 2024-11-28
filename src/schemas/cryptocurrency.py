from pydantic import BaseModel
from typing import List


class CryptocurrencyItemDTO(BaseModel):
    name: str
    symbol: str
    price: float
    market_cap: int


class CryptocurrencyResponseDTO(BaseModel):
    current_page: int
    cryptocurrencies: List[CryptocurrencyItemDTO]
