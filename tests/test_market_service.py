import pytest
from unittest.mock import AsyncMock, patch
from src.services.market_service import get_market_summary


@pytest.mark.asyncio
async def test_get_market_summary():
    mock_data = [
        {
            "name": "Bitcoin",
            "symbol": "btc",
            "market_cap": 900000000,
            "price_change_percentage_24h": 2.5,
        },
        {
            "name": "Ethereum",
            "symbol": "eth",
            "market_cap": 400000000,
            "price_change_percentage_24h": 5.0,
        },
        {
            "name": "Solana",
            "symbol": "sol",
            "market_cap": 300000000,
            "price_change_percentage_24h": -1.2,
        },
        {
            "name": "Cardano",
            "symbol": "ada",
            "market_cap": 200000000,
            "price_change_percentage_24h": 0.5,
        },
    ]

    with patch(
        "src.services.market_service.fetch_cryptocurrencies_from_api",
        new=AsyncMock(return_value=mock_data),
    ):
        result = await get_market_summary("usd")

        assert result.top_gainer.name == "Ethereum"
        assert result.top_loser.name == "Solana"
        assert len(result.top_market_cap) == 3
        assert result.top_market_cap[0].name == "Bitcoin"
