from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, AsyncSession
from sqlalchemy import text
from src.config.config import settings
from src.models.user_model import Base
import asyncio

engine: AsyncEngine = create_async_engine(settings.DB_URL, echo=True)

Session: AsyncSession = sessionmaker(
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    class_=AsyncSession,
    bind=engine
)

async def create_schema(session: AsyncSession, schema_name: str):
    result = await session.execute(text(f"SELECT schema_name FROM information_schema.schemata WHERE schema_name = '{schema_name}'"))
    schema_exists = result.scalar() is not None
    
    if not schema_exists:
        await session.execute(text(f"CREATE SCHEMA IF NOT EXISTS {schema_name};"))
        await session.commit()

async def create_tables():
    async with engine.begin() as conn:
        await create_schema(conn, settings.DB_SCHEMA)
        await conn.run_sync(Base.metadata.create_all)
        print("criou")

if __name__ == "__main__":
    asyncio.run(create_tables())