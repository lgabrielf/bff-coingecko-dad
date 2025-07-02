import pytest
from datetime import datetime
from unittest.mock import AsyncMock, patch

from src.services.price_service import get_cryptocurrency_history


@pytest.mark.asyncio
async def test_get_cryptocurrency_history():

    mock_data = [
        {"date": 1700438400, "price": 35000.0},  # 2023-11-20
        {"date": 1700524800, "price": 36000.0},  # 2023-11-21
        {"date": 1700611200, "price": 37000.0},  # 2023-11-22
    ]

    with patch(
        "src.services.price_service.fetch_cryptocurrency_history_from_api",
        new=AsyncMock(return_value=mock_data)
    ):
        result = await get_cryptocurrency_history(
            crypto_id="bitcoin",
            currency="usd",
            start_date="2023-11-20",
            end_date="2023-11-22"
        )

    assert result.id == "bitcoin"
    assert result.symbol == "BITCOIN"
    assert result.currency == "usd"
    assert len(result.history) == 3
    assert result.history[0].date == "2023-11-20"
    assert result.history[0].price == 35000.0
