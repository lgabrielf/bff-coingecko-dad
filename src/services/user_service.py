from typing import Generator, Optional
import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.config.database import Session
from src.config.auth import oauth2_schema
from src.config.config import settings
from src.models.user_model import UserModel

from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError

from pydantic import BaseModel

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TokenData(BaseModel):
    username: Optional[str] = None

async def get_session() -> Generator:
    session: AsyncSession = Session()

    try:
        logger.info("Conexão com o banco de dados estabelecida com sucesso.")
        yield session  #abre conexão com o db
    finally:
        logger.info("Conexão com o banco de dados encerrada com sucesso.")
        await session.close() #depois de fazer uso, eh encerrada a conexão


async def get_current_user(db: Session = Depends(get_session), token: str = Depends(oauth2_schema)) -> UserModel:
   # caso o usuário não autentique, retorne essa variável a seguir
    credential_exception: HTTPException = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, 
        detail='Não foi possível authenticate a credencial', 
        headers={"WWWW-Authenticate": "Bearer"}
    )

    try:
        payload = jwt.decode(
            token, 
            settings.JWT_SECRET, 
            algorithms=[settings.ALGORITHM], 
            options={"verify_aud": False}
        )
        user_id = payload.get("sub")
        if user_id is None:
            raise credential_exception

        # (opcional) imprimir role para debug
        print(f"[DEBUG] role no token: {payload.get('role')}")
    except JWTError: 
        #se não conseguir decodificar
        raise credential_exception
    async with db as session:
        query = select(UserModel).filter(UserModel.id == int(user_id))
        result = await session.execute(query)
        user: UserModel = result.scalars().unique().one_or_none()

        if user is None:
            raise credential_exception
        return user