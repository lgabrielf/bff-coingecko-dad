import pytest
from httpx import AsyncClient
from src.main import app
from datetime import datetime

@pytest.mark.asyncio
async def test_cryptocurrency_history():
    crypto_id = "bitcoin"
    currency = "usd"
    start_date = "2023-11-20"
    end_date = "2023-11-22"

    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get(
            f"/bff/cryptocurrencies/{crypto_id}/history",
            params={
                "currency": currency,
                "start_date": start_date,
                "end_date": end_date,
            },
        )
    
    assert response.status_code == 200

    data = response.json()

    assert "id" in data
    assert data["id"] == crypto_id
    assert "symbol" in data
    assert "currency" in data
    assert data["currency"] == currency
    assert "history" in data

    history = data["history"]
    assert isinstance(history, list)
    for item in history:
        assert "date" in item
        assert "price" in item
        # Validar o formato da data e preço
        datetime.strptime(item["date"], "%Y-%m-%d")
        assert isinstance(item["price"], (int, float))