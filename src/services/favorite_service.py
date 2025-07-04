
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.user_model import UserModel
from src.schemas.favorite import FavoriteCreateDTO
from fastapi import HTTPException, status
from src.repositories.favorite_repository import FavoriteRepository

async def create_favorite(db: AsyncSession, favorite: FavoriteCreateDTO, user: UserModel):
    existing_favorite = await FavoriteRepository.get_by_user_and_coin(db, user.id, favorite.coin_id)
    if existing_favorite:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Coin already favorited")
    return await FavoriteRepository.create(db, favorite.coin_id, user.id)

async def get_user_favorites(db: AsyncSession, user: UserModel):
    return await FavoriteRepository.get_all_by_user(db, user.id)

async def delete_favorite(db: AsyncSession, favorite_id: int, user: UserModel):
    db_favorite = await FavoriteRepository.get_by_id_and_user(db, favorite_id, user.id)
    if not db_favorite:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Favorite not found")
    await FavoriteRepository.delete(db, db_favorite)
    return {"message": "Favorite deleted successfully"}
