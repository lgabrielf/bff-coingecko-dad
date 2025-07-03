import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from src.services.user_service import get_current_user, TokenData
from src.models.user_model import UserModel
from fastapi import HTTPException
from jose import jwt, JWTError

@pytest.mark.asyncio
async def test_get_current_user():
    # Simula usuário fake
    fake_user = UserModel(id=1, name="Test User")

    # Mock do token decodificado
    mock_jwt_decode = {
        "sub": "1"
    }

    # Cria um mock para session.execute().scalars().unique().one_or_none()
    mock_result = MagicMock()
    mock_result.scalars.return_value.unique.return_value.one_or_none.return_value = fake_user

    mock_session = AsyncMock()
    mock_session.__aenter__.return_value = mock_session  # para o async with
    mock_session.execute.return_value = mock_result

    with patch("src.services.user_service.jwt.decode", return_value=mock_jwt_decode), \
         patch("src.services.user_service.get_session", return_value=mock_session):

        user = await get_current_user(db=mock_session, token="fake-token")
        assert user == fake_user

@pytest.mark.asyncio
async def test_get_current_user_missing_sub_in_token():
    mock_session = AsyncMock()
    mock_session.__aenter__.return_value = mock_session

    invalid_payload = {}  # não contém "sub"

    with patch("src.services.user_service.jwt.decode", return_value=invalid_payload):
        with pytest.raises(HTTPException) as exc_info:
            await get_current_user(db=mock_session, token="invalid-token")

        assert exc_info.value.status_code == 401
        assert "Não foi possível authenticate a credencial" in str(exc_info.value.detail)

@pytest.mark.asyncio
async def test_get_current_user_invalid_token():
    mock_session = AsyncMock()
    mock_session.__aenter__.return_value = mock_session

    with patch("src.services.user_service.jwt.decode", side_effect=JWTError):
        with pytest.raises(HTTPException) as exc_info:
            await get_current_user(db=mock_session, token="bad-token")

        assert exc_info.value.status_code == 401

# @pytest.mark.asyncio
# async def test_get_current_user_user_not_found():
#     mock_session = AsyncMock()
#     mock_session.__aenter__.return_value = mock_session

#     valid_payload = {"sub": "1"}

#     # Simula ausência de usuário
#     mock_result = AsyncMock()
#     mock_result.scalars.return_value.unique.return_value.one_or_none.return_value = None
#     mock_session.execute.return_value = mock_result

#     with patch("src.services.user_service.jwt.decode", return_value=valid_payload):
#         with patch("src.services.user_service.get_session", return_value=mock_session):
#             with pytest.raises(HTTPException) as exc_info:
#                 await get_current_user(db=mock_session, token="token")

#             assert exc_info.value.status_code == 401

