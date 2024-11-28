from pydantic import BaseModel
from typing import List, Optional


class CryptocurrencySummaryItemDTO(BaseModel):
    name: str
    symbol: str
    market_cap: Optional[int] = None
    percentage_change_24h: Optional[float] = None

    class Config:
        from_attributes = True
        exclude_none = True
        json_schema_extra = {
            "example": {
                "name": "Bitcoin",
                "symbol": "BTC",
                "market_cap": 1200000000000,
                "percentage_change_24h": 5.34
            }
        }

class MarketSummaryResponseDTO(BaseModel):
    top_market_cap: List[CryptocurrencySummaryItemDTO]
    top_gainer: CryptocurrencySummaryItemDTO
    top_loser: CryptocurrencySummaryItemDTO

    class Config:
        from_attributes = True
        exclude_none = True
        json_schema_extra = {
            "example": {
                "top_market_cap": [
                    {"name": "Bitcoin", "symbol": "BTC", "market_cap": 1200000000000, "percentage_change_24h": 5.34},
                    {"name": "Ethereum", "symbol": "ETH", "market_cap": 560000000000, "percentage_change_24h": 3.22},
                    {"name": "Tether", "symbol": "USDT", "market_cap": 130000000000, "percentage_change_24h": 0.01}
                ],
                "top_gainer": {"name": "Bitcoin", "symbol": "BTC", "market_cap": 1200000000000, "percentage_change_24h": 5.34},
                "top_loser": {"name": "Dogecoin", "symbol": "DOGE", "market_cap": 80000000000, "percentage_change_24h": -3.15}
            }
        }