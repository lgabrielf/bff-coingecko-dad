from datetime import datetime, timedelta
from typing import Optional

from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pytz import timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.config.security import check_password
from src.config.config import settings
from src.models.user_model import UserModel

oauth2_schema = OAuth2PasswordBearer(tokenUrl='/bff/login')


async def authenticate(
    name: str, password: str, db: AsyncSession
) -> Optional[UserModel]:
    async with db as session:
        query = select(UserModel).filter(UserModel.name == name)
        result = await session.execute(query)
        user: UserModel = result.scalars().unique().one_or_none()

        if not user:
            return None

        if not check_password(password, user.password):
            return None

        return user


def _criar_token(tipo_token: str, tempo_vida: timedelta, sub: str) -> str:
    # https://datatracker.ietf.org/doc/html/rfc7519#section-4.1.3
    payload = {}
    rn = timezone('America/Fortaleza')

    # tempo de expiração do token
    expira = datetime.now(tz=rn) + tempo_vida

    payload['type'] = tipo_token

    payload['exp'] = expira
    # iat: gerado em
    payload['iat'] = datetime.now(tz=rn)
    # sub: pode ser id, email, nome, qualquer coisa que identifique o usuário
    payload['sub'] = str(sub)

    return jwt.encode(
        payload, settings.JWT_SECRET, algorithm=settings.ALGORITHM
    )


def criar_token_acesso(sub: str) -> str:
    """
    http://jwt.io
    """

    return _criar_token(
        tipo_token='access_token',
        tempo_vida=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        sub=sub,
    )
