import pytest
from httpx import AsyncClient
from src.main import app

@pytest.mark.asyncio
async def test_cryptocurrency_history():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/bff/cryptocurrencies/bitcoin/history?currency=usd&start_date=2023-11-20&end_date=2023-11-22")
    
    assert response.status_code == 200
    data = response.json()
    assert "history" in data
    assert len(data["history"]) > 0
    assert "date" in data["history"][0]
    assert "price" in data["history"][0]