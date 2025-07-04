from fastapi import APIRouter, Depends, status
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from src.services.user_service import get_current_user, get_session
from src.models.user_model import UserModel
from src.schemas.favorite import FavoriteResponseDTO, FavoriteCreateDTO
from src.services import favorite_service

router = APIRouter()

@router.post("/favorites", response_model=FavoriteResponseDTO, status_code=status.HTTP_201_CREATED)
async def add_favorite(
    favorite: FavoriteCreateDTO,
    db: AsyncSession = Depends(get_session),
    current_user: UserModel = Depends(get_current_user)
):
    return await favorite_service.create_favorite(db=db, favorite=favorite, user=current_user)

@router.get("/favorites/all", response_model=List[FavoriteResponseDTO])
async def list_favorites(
    db: AsyncSession = Depends(get_session),
    current_user: UserModel = Depends(get_current_user)
):
    return await favorite_service.get_user_favorites(db=db, user=current_user)

@router.delete("/favorites/{favorite_id}", status_code=status.HTTP_200_OK)
async def remove_favorite(
    favorite_id: int,
    db: AsyncSession = Depends(get_session),
    current_user: UserModel = Depends(get_current_user)
):
    return await favorite_service.delete_favorite(db=db, favorite_id=favorite_id, user=current_user)
