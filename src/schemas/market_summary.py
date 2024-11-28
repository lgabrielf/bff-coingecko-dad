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


class MarketSummaryResponseDTO(BaseModel):
    top_market_cap: List[CryptocurrencySummaryItemDTO]
    top_gainer: CryptocurrencySummaryItemDTO
    top_loser: CryptocurrencySummaryItemDTO

    class Config:
        from_attributes = True
        exclude_none = True
