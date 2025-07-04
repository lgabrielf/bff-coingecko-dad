from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import and_
from src.models.favorite_model import FavoriteModel

class FavoriteRepository:
    @staticmethod
    async def get_by_user_and_coin(db: AsyncSession, user_id: int, coin_id: str):
        query = select(FavoriteModel).where(
            and_(
                FavoriteModel.user_id == user_id,
                FavoriteModel.coin_id == coin_id
            )
        )
        result = await db.execute(query)
        return result.scalars().first()

    @staticmethod
    async def create(db: AsyncSession, coin_id: str, user_id: int):
        db_favorite = FavoriteModel(coin_id=coin_id, user_id=user_id)
        db.add(db_favorite)
        await db.commit()
        await db.refresh(db_favorite)
        return db_favorite

    @staticmethod
    async def get_all_by_user(db: AsyncSession, user_id: int):
        query = select(FavoriteModel).where(FavoriteModel.user_id == user_id)
        result = await db.execute(query)
        return result.scalars().all()

    @staticmethod
    async def get_by_id_and_user(db: AsyncSession, favorite_id: int, user_id: int):
        query = select(FavoriteModel).where(
            and_(
                FavoriteModel.id == favorite_id,
                FavoriteModel.user_id == user_id
            )
        )
        result = await db.execute(query)
        return result.scalars().first()

    @staticmethod
    async def delete(db: AsyncSession, favorite):
        await db.delete(favorite)
        await db.commit()
