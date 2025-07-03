from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, AsyncSession
from sqlalchemy import text, insert
from passlib.hash import bcrypt
from src.config.config import settings
from src.models.user_model import Base, UserModel
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
    result = await session.execute(
        text(f"SELECT schema_name FROM information_schema.schemata WHERE schema_name = :schema_name"),
        {"schema_name": schema_name}
    )
    schema_exists = result.scalar() is not None

    if not schema_exists:
        await session.execute(text(f"CREATE SCHEMA IF NOT EXISTS {schema_name};"))
        await session.commit()
        print(f"Schema '{schema_name}' created.")
    else:
        print(f"Schema '{schema_name}' already exists.")

async def create_first_admin(conn: AsyncSession):
    # Verifica se admin já existe
    result = await conn.execute(
        text(f"SELECT id FROM {settings.DB_SCHEMA}.user WHERE name = :name"),
        {"name": settings.ADMIN_USERNAME}
    )
    user_exists = result.scalar() is not None

    if not user_exists:
        hashed_password = bcrypt.hash(settings.ADMIN_PASSWORD)
        await conn.execute(
            insert(UserModel).values(
                name=settings.ADMIN_USERNAME,
                password=hashed_password,
                role="admin"
            )
        )
        await conn.commit()
        print(f"Admin user '{settings.ADMIN_USERNAME}' criado com sucesso.")
    else:
        print(f"Admin user '{settings.ADMIN_USERNAME}' já existe.")

async def create_tables():
    async with engine.begin() as conn:
        await create_schema(conn, settings.DB_SCHEMA)
        await conn.run_sync(Base.metadata.create_all)
        await create_first_admin(conn)
        print("Tabelas criadas com sucesso.")

if __name__ == "__main__":
    asyncio.run(create_tables())