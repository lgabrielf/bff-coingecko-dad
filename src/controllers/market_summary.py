from fastapi import APIRouter, HTTPException, Depends
from src.services.market_service import get_market_summary
from src.services.user_service import  get_current_user
from src.schemas import MarketSummaryResponseDTO, UserDTO

router = APIRouter()

@router.get('/market/summary', response_model=MarketSummaryResponseDTO)
async def market_summary(currency: str = 'usd', usuario_logado: UserDTO = Depends(get_current_user)):
    """
    Endpoint para obter o resumo do mercado de criptomoedas.
    """
    if currency not in ['usd', 'eur']:
        raise HTTPException(
            status_code=400,
            detail="Moeda de cotação inválida. Use 'usd' ou 'eur'."
    )

    try:
        return await get_market_summary(currency)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f'Erro ao obter dados do mercado: {str(e)}'
        )
