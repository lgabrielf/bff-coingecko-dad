import pytest
from httpx import AsyncClient
from src.main import app

@pytest.mark.asyncio
async def test_list_cryptocurrencies_success():
    """
    Testa o endpoint /bff/cryptocurrencies para uma requisição bem-sucedida.
    """
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/bff/cryptocurrencies", params={"currency": "usd", "page": 1, "per_page": 5})

    # Verifica o status HTTP
    assert response.status_code == 200

    # Verifica a estrutura da resposta
    data = response.json()
    assert "current_page" in data
    assert "cryptocurrencies" in data
    assert isinstance(data["cryptocurrencies"], list)

    # Verifica que os itens possuem a estrutura esperada
    for crypto in data["cryptocurrencies"]:
        assert "name" in crypto
        assert "symbol" in crypto
        assert "price" in crypto
        assert "market_cap" in crypto

@pytest.mark.asyncio
async def test_list_cryptocurrencies_invalid_currency():
    """
    Testa o endpoint /bff/cryptocurrencies com um parâmetro de moeda inválido.
    """
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/bff/cryptocurrencies", params={"currency": "invalid", "page": 1, "per_page": 5})

    # Verifica o status HTTP para erro
    assert response.status_code == 400

    # Verifica a mensagem de erro
    data = response.json()
    assert data["detail"] == "Moeda de cotação inválida. Use 'usd' ou 'eur'."

@pytest.mark.asyncio
async def test_list_cryptocurrencies_pagination():
    """
    Testa a paginação no endpoint /bff/cryptocurrencies.
    """
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/bff/cryptocurrencies", params={"currency": "usd", "page": 2, "per_page": 5})

    # Verifica o status HTTP
    assert response.status_code == 200

    # Verifica que a página atual está correta
    data = response.json()
    assert data["current_page"] == 2
    assert isinstance(data["cryptocurrencies"], list)
