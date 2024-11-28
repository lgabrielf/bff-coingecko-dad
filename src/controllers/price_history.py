from fastapi import APIRouter, Query, HTTPException
from src.services.price_service import get_cryptocurrency_history
from src.schemas import CryptocurrencyHistoryResponseDTO

router = APIRouter()


@router.get(
    '/cryptocurrencies/{id}/history',
    response_model=CryptocurrencyHistoryResponseDTO,
)
async def cryptocurrency_history(
    id: str,
    currency: str = Query('usd', description='Moeda de cotação: usd ou eur'),
    start_date: str = Query(
        ..., description='Data de início no formato yyyy-mm-dd'
    ),
    end_date: str = Query(
        ..., description='Data de fim no formato yyyy-mm-dd'
    ),
):
    """
    Endpoint para obter o histórico de preços de uma criptomoeda específica.
    """
    # try:
    return await get_cryptocurrency_history(id, currency, start_date, end_date)
    # except Exception as e:
    #     raise HTTPException(status_code=500, detail=f"Erro ao obter dados do histórico: {str(e)}")
