from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.models.user_model import Base
from src.config.config import settings

class FavoriteModel(Base):
    __tablename__ = 'favorites'

    id = Column(Integer, primary_key=True, index=True)
    coin_id = Column(String, nullable=False, index=True)
    user_id = Column(Integer, ForeignKey(f"{settings.DB_SCHEMA}.user.id"), nullable=False)

    user = relationship("UserModel", back_populates="favorites")
