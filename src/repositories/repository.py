import httpx
import datetime
from fastapi import HTTPException
from src.config.config import settings

COINGECKO_BASE_URL = "https://api.coingecko.com/api/v3"

async def fetch_cryptocurrencies_from_api(currency: str, page: int, per_page: int):
    """
    Faz a chamada para a API CoinGecko e retorna os dados brutos.
    """
    url = f"{COINGECKO_BASE_URL}/coins/markets"
    params = {
        "vs_currency": currency,
        "order": "market_cap_desc",
        "per_page": per_page,
        "page": page,
        "sparkline": False
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Erro ao acessar a CoinGecko API.")
    
    return response.json()

async def fetch_cryptocurrency_history_from_api(vs_currency: str, crypto_id: str, start_timestamp: int, end_timestamp: int):
    """
    Obtém o histórico de preços de uma criptomoeda específica da API CoinGecko.
    """
    url = f"{COINGECKO_BASE_URL}/coins/{crypto_id}/market_chart/range"
    params = {
        "vs_currency": vs_currency,
        "from": start_timestamp,
        "to": end_timestamp

    }
    headers = {
        "accept": "application/json",
        "x-cg-demo-api-key": settings.coingecko_api_key
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params, headers=headers)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Erro ao acessar a CoinGecko API.")

    data = response.json()

    # Retorne os dados no formato esperado
    return [
        {
            "date": item[0] / 1000,
            "price": item[1]
        }
        for item in data.get("prices", [])
    ]