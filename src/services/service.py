from src.repositories.repository import fetch_cryptocurrencies_from_api, fetch_cryptocurrency_history_from_api
from datetime import datetime
from src.DTOs import CryptocurrencyResponse, CryptocurrencyItem, MarketSummary, CryptocurrencySummaryItem, CryptocurrencyHistory, PriceHistoryItem

async def get_cryptocurrencies(currency: str, page: int, per_page: int) -> CryptocurrencyResponse:

    raw_data = await fetch_cryptocurrencies_from_api(currency, page, per_page)
    
    cryptocurrencies = [
        CryptocurrencyItem(
            name=coin["name"],
            symbol=coin["symbol"],
            price=coin["current_price"],
            market_cap=coin["market_cap"]
        )
        for coin in raw_data
    ]
    
    return CryptocurrencyResponse(
        current_page=page,
        cryptocurrencies=cryptocurrencies
    )

async def get_market_summary(currency: str) -> MarketSummary:
    """
    Obtém o resumo do mercado de criptomoedas (top 3, maior valorização, maior desvalorização).
    """

    raw_data = await fetch_cryptocurrencies_from_api(currency, page=1, per_page=10)

    top_market_cap = [
        CryptocurrencySummaryItem(
            name=coin["name"],
            symbol=coin["symbol"],
            market_cap=coin["market_cap"]
        )
        for coin in raw_data[:3]
    ]
    
    top_gainer = max(raw_data, key=lambda coin: coin["price_change_percentage_24h"])
    top_loser = min(raw_data, key=lambda coin: coin["price_change_percentage_24h"])

    return MarketSummary(
        top_market_cap=top_market_cap,
        top_gainer=CryptocurrencySummaryItem(
            name=top_gainer["name"],
            symbol=top_gainer["symbol"],
            market_cap=top_gainer["market_cap"]
        ),
        top_loser=CryptocurrencySummaryItem(
            name=top_loser["name"],
            symbol=top_loser["symbol"],
            market_cap=top_loser["market_cap"]
        )
    )

async def get_cryptocurrency_history(
    crypto_id: str, 
    currency: str, 
    start_date: str, 
    end_date: str
) -> CryptocurrencyHistory:
    """
    Obtém o histórico de preços de uma criptomoeda específica no intervalo de tempo fornecido.
    """
    # Converter as datas para o formato necessário (ex: "2023-11-20")
    # A API do CoinGecko usa timestamps (Unix timestamp), então precisamos converter as datas.
    start_timestamp = int(datetime.strptime(start_date, "%Y-%m-%d").timestamp())
    end_timestamp = int(datetime.strptime(end_date, "%Y-%m-%d").timestamp())

    # Chamada para o repositório para obter os dados históricos da API
    raw_data = await fetch_cryptocurrency_history_from_api(crypto_id, currency, start_timestamp, end_timestamp)
    
    # Organize the data into the  format
    history = [
        PriceHistoryItem(
            date=datetime.utcfromtimestamp(coin["date"]).strftime("%Y-%m-%d"),
            price=coin["price"]
        )
        for coin in raw_data
    ]

    # Build the response 
    return CryptocurrencyHistory(
        id=crypto_id,
        symbol=raw_data[0]["symbol"] if raw_data else "",
        currency=currency,
        history=history
    )