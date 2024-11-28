from pydantic import BaseModel
from typing import List


class PriceHistoryItemDTO(BaseModel):
    date: str
    price: float

    class Config:
        json_schema_extra = {
            "example": {
                "date": "2023-11-20",
                "price": 64000.00
            }
        }

class CryptocurrencyHistoryResponseDTO(BaseModel):
    id: str
    symbol: str
    currency: str
    history: List[PriceHistoryItemDTO]

    class Config:
        json_schema_extra = {
            "example": {
                "id": "bitcoin",
                "symbol": "BTC",
                "currency": "usd",
                "history": [
                    {"date": "2023-11-20", "price": 64000.00},
                    {"date": "2023-11-21", "price": 64500.00},
                    {"date": "2023-11-22", "price": 64200.00}
                ]
            }
        }