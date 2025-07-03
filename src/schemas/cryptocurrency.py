from pydantic import BaseModel, ConfigDict
from typing import List


class CryptocurrencyItemDTO(BaseModel):
    name: str
    symbol: str
    price: float
    market_cap: int

    class ConfigDict:
        json_schema_extra = {
            "example": {
                "name": "Bitcoin",
                "symbol": "BTC",
                "price": 64000.00,
                "market_cap": 1200000000000
            }
        }


class CryptocurrencyResponseDTO(BaseModel):
    current_page: int
    cryptocurrencies: List[CryptocurrencyItemDTO]

    class ConfigDict:
        json_schema_extra = {
            "example": {
                "current_page": 1,
                "cryptocurrencies": [
                    {"name": "Bitcoin", "symbol": "BTC", "price": 64000.00, "market_cap": 1200000000000},
                    {"name": "Ethereum", "symbol": "ETH", "price": 4700.12, "market_cap": 560000000000}
                ]
            }
        }