from src.repositories.coingecko_repository import (
    fetch_cryptocurrency_history_from_api,
)
from datetime import datetime, timezone
from src.schemas import CryptocurrencyHistoryResponseDTO, PriceHistoryItemDTO


async def get_cryptocurrency_history(
    crypto_id: str, currency: str, start_date: str, end_date: str
) -> CryptocurrencyHistoryResponseDTO:
    """
    Obtém o histórico de preços de uma criptomoeda específica no intervalo de tempo fornecido.
    """
    start_timestamp = int(
        datetime.strptime(start_date, '%Y-%m-%d').timestamp()
    )
    end_timestamp = int(datetime.strptime(end_date, '%Y-%m-%d').timestamp())

    raw_data = await fetch_cryptocurrency_history_from_api(
        crypto_id, currency, start_timestamp, end_timestamp
    )

    history = [
        PriceHistoryItemDTO(
            date=datetime.fromtimestamp(coin['date'], timezone.utc).strftime('%Y-%m-%d'),
            price=coin['price'],
        )
        for coin in raw_data
    ]

    return CryptocurrencyHistoryResponseDTO(
        id=crypto_id,
        symbol=crypto_id.upper(),
        currency=currency,
        history=history,
    )
