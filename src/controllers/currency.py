from fastapi import APIRouter, Query, HTTPException
from src.services.service import get_cryptocurrencies, get_market_summary, get_cryptocurrency_history
from src.DTOs import CryptocurrencyResponse, MarketSummary, CryptocurrencyHistory

router = APIRouter()

@router.get("/bff/cryptocurrencies", response_model=CryptocurrencyResponse)
async def list_cryptocurrencies(
    currency: str = Query("usd", description="Moeda de cotação: usd ou eur"),
    page: int = Query(1, description="Número da página"),
    per_page: int = Query(10, description="Itens por página (máximo: 250)")
):
    """
    Endpoint para listar criptomoedas paginadas e filtradas por moeda de cotação.
    """
    if currency not in ["usd", "eur"]:
        raise HTTPException(status_code=400, detail="Moeda de cotação inválida. Use 'usd' ou 'eur'.")

    return await get_cryptocurrencies(currency, page, per_page)

@router.get("/bff/market/summary", response_model=MarketSummary)
async def market_summary(currency: str = "usd"):
    """
    Endpoint para obter o resumo do mercado de criptomoedas.
    """
    try:
        return await get_market_summary(currency)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter dados do mercado: {str(e)}")
    
@router.get("/bff/cryptocurrencies/{id}/history", response_model=CryptocurrencyHistory)
async def cryptocurrency_history(
    id: str,
    currency: str = Query("usd", description="Moeda de cotação: usd ou eur"),
    start_date: str = Query(..., description="Data de início no formato yyyy-mm-dd"),
    end_date: str = Query(..., description="Data de fim no formato yyyy-mm-dd")
):
    """
    Endpoint para obter o histórico de preços de uma criptomoeda específica.
    """
    try:
        return await get_cryptocurrency_history(id, currency, start_date, end_date)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter dados do histórico: {str(e)}")