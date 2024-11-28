from src.repositories.coingecko_repository import (
    fetch_cryptocurrencies_from_api,
)
from src.schemas import MarketSummaryResponseDTO, CryptocurrencySummaryItemDTO


async def get_market_summary(currency: str) -> MarketSummaryResponseDTO:
    """
    Obtém o resumo do mercado de criptomoedas (top 3, maior valorização, maior desvalorização).
    """

    raw_data = await fetch_cryptocurrencies_from_api(
        currency, page=1, per_page=10
    )

    top_market_cap = [
        CryptocurrencySummaryItemDTO(
            name=coin['name'],
            symbol=coin['symbol'].upper(),
            market_cap=coin['market_cap'],
            percentage_change_24h=coin.get(
                'price_change_percentage_24h', None
            ),
        )
        for coin in raw_data[:3]
    ]

    top_gainer = max(
        raw_data, key=lambda coin: coin['price_change_percentage_24h']
    )
    top_loser = min(
        raw_data, key=lambda coin: coin['price_change_percentage_24h']
    )

    return MarketSummaryResponseDTO(
        top_market_cap=top_market_cap,
        top_gainer=CryptocurrencySummaryItemDTO(
            name=top_gainer['name'],
            symbol=top_gainer['symbol'].upper(),
            market_cap=top_gainer.get('market_cap', None),
            percentage_change_24h=top_gainer['price_change_percentage_24h'],
        ),
        top_loser=CryptocurrencySummaryItemDTO(
            name=top_loser['name'],
            symbol=top_loser['symbol'].upper(),
            market_cap=top_gainer.get('market_cap', None),
            percentage_change_24h=top_loser['price_change_percentage_24h'],
        ),
    )
