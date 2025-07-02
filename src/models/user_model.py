from sqlalchemy.orm import declarative_base
from sqlalchemy import Integer, String, Column, MetaData
from src.config.config import settings

metadata = MetaData(schema=settings.DB_SCHEMA)
Base = declarative_base(metadata=metadata)

class UserModel(Base):
    __tablename__ = 'user'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(256), nullable=True)
    password = Column(String(256), nullable=True)
    role = Column(String(50), nullable=True)