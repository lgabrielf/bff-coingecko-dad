from fastapi import APIRouter, Query, HTTPException
from src.services.service import get_cryptocurrencies
from src.DTOs import CryptocurrencyResponse

router = APIRouter()

@router.get("/cryptocurrencies", response_model=CryptocurrencyResponse)
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
