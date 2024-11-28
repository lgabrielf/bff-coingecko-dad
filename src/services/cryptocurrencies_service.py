from src.repositories.coingecko_repository import (
    fetch_cryptocurrencies_from_api,
)
from src.schemas import CryptocurrencyResponseDTO, CryptocurrencyItemDTO


async def get_cryptocurrencies(
    currency: str, page: int, per_page: int
) -> CryptocurrencyResponseDTO:

    raw_data = await fetch_cryptocurrencies_from_api(currency, page, per_page)

    cryptocurrencies = [
        CryptocurrencyItemDTO(
            name=coin['name'],
            symbol=coin['symbol'].upper(),
            price=coin['current_price'],
            market_cap=coin['market_cap'],
        )
        for coin in raw_data
    ]

    return CryptocurrencyResponseDTO(
        current_page=page, cryptocurrencies=cryptocurrencies
    )
