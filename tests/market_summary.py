import pytest
from httpx import AsyncClient
from src.main import app


@pytest.mark.asyncio
async def test_market_summary():
    async with AsyncClient(app=app, base_url='http://test') as ac:
        response = await ac.get('/bff/market/summary?currency=usd')

    assert response.status_code == 200
    data = response.json()
    assert 'top_market_cap' in data
    assert 'top_gainer' in data
    assert 'top_loser' in data
    assert len(data['top_market_cap']) == 3
