
from fastapi import APIRouter, HTTPException
from src.services.service import get_market_summary
from src.DTOs import MarketSummary

router = APIRouter()

@router.get("/market/summary", response_model=MarketSummary)
async def market_summary(currency: str = "usd"):
    """
    Endpoint para obter o resumo do mercado de criptomoedas.
    """
    try:
        return await get_market_summary(currency)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter dados do mercado: {str(e)}")