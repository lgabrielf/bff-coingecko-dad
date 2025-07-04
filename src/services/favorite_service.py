from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete, and_
from src.models.favorite_model import FavoriteModel
from src.models.user_model import UserModel
from src.schemas.favorite import FavoriteCreateDTO
from fastapi import HTTPException, status

async def create_favorite(db: AsyncSession, favorite: FavoriteCreateDTO, user: UserModel) -> FavoriteModel:
    existing_favorite_query = select(FavoriteModel).where(
        and_(
            FavoriteModel.user_id == user.id,
            FavoriteModel.coin_id == favorite.coin_id
        )
    )
    existing_favorite = await db.execute(existing_favorite_query)
    if existing_favorite.scalars().first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Coin already favorited")

    db_favorite = FavoriteModel(coin_id=favorite.coin_id, user_id=user.id)
    db.add(db_favorite)
    await db.commit()
    await db.refresh(db_favorite)
    return db_favorite

async def get_user_favorites(db: AsyncSession, user: UserModel):
    query = select(FavoriteModel).where(FavoriteModel.user_id == user.id)
    result = await db.execute(query)
    return result.scalars().all()

async def delete_favorite(db: AsyncSession, favorite_id: int, user: UserModel):
    favorite_to_delete_query = select(FavoriteModel).where(
        and_(
            FavoriteModel.id == favorite_id,
            FavoriteModel.user_id == user.id
        )
    )
    favorite_to_delete = await db.execute(favorite_to_delete_query)
    db_favorite = favorite_to_delete.scalars().first()

    if not db_favorite:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Favorite not found")

    await db.delete(db_favorite)
    await db.commit()
    return {"message": "Favorite deleted successfully"}
