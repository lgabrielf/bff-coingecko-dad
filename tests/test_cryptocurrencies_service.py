import pytest
from unittest.mock import AsyncMock, patch
from src.services.cryptocurrencies_service import get_cryptocurrencies
from src.schemas import CryptocurrencyResponseDTO, CryptocurrencyItemDTO


@pytest.mark.asyncio
async def test_get_cryptocurrencies_success():

    mock_raw_data = [
        {
            'name': 'Bitcoin',
            'symbol': 'btc',
            'current_price': 30000,
            'market_cap': 600000000000,
        },
        {
            'name': 'Ethereum',
            'symbol': 'eth',
            'current_price': 2000,
            'market_cap': 250000000000,
        },
    ]

    with patch(
        "src.repositories.coingecko_repository.fetch_cryptocurrencies_from_api",
        new_callable=AsyncMock
    ) as mock_fetch:
        mock_fetch.return_value = mock_raw_data

        # Chama o serviço
        response = await get_cryptocurrencies(currency="usd", page=1, per_page=10)

        # Verificações
        assert isinstance(response, CryptocurrencyResponseDTO)
        assert response.current_page == 1
        assert len(response.cryptocurrencies) == 10

        # Checa se os dados foram mapeados corretamente para o DTO
        first_coin = response.cryptocurrencies[0]
        assert isinstance(first_coin, CryptocurrencyItemDTO)
        assert first_coin.name == "Bitcoin"
        assert first_coin.symbol == "BTC"  # symbol uppercased
