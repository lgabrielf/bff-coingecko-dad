from pydantic import BaseModel
from typing import List

class CryptocurrencySummaryItem(BaseModel):
    name: str
    symbol: str
    market_cap: int

class MarketSummary(BaseModel):
    top_market_cap: List[CryptocurrencySummaryItem]
    top_gainer: CryptocurrencySummaryItem
    top_loser: CryptocurrencySummaryItem