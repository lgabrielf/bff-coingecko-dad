import pytest
from unittest.mock import AsyncMock, MagicMock
from fastapi import HTTPException
from src.services import favorite_service
from src.schemas.favorite import FavoriteCreateDTO
from src.models.user_model import UserModel
from src.models.favorite_model import FavoriteModel

@pytest.mark.asyncio
async def test_create_favorite_success():
    mock_db = AsyncMock()
    mock_user = UserModel(id=1, name="testuser")
    favorite_data = FavoriteCreateDTO(coin_id="bitcoin")

    # Mock the database to return None, indicating the favorite doesn't exist
    mock_result = MagicMock()
    mock_result.scalars.return_value.first.return_value = None
    mock_db.execute.return_value = mock_result

    # The service creates and returns a FavoriteModel instance.
    # We assume the db.refresh call populates it correctly.
    result = await favorite_service.create_favorite(db=mock_db, favorite=favorite_data, user=mock_user)

    # In a real scenario, db.refresh would populate the ID. We assert the parts we know.
    assert getattr(result, 'coin_id') == "bitcoin"
    assert getattr(result, 'user_id') == 1
    mock_db.add.assert_called_once()
    mock_db.commit.assert_awaited_once()
    mock_db.refresh.assert_awaited_once()

@pytest.mark.asyncio
async def test_create_favorite_conflict():
    mock_db = AsyncMock()
    mock_user = UserModel(id=1, name="testuser")
    favorite_data = FavoriteCreateDTO(coin_id="bitcoin")
    existing_favorite = FavoriteModel(id=1, user_id=mock_user.id, coin_id=favorite_data.coin_id)

    # Mock the database to return an existing favorite
    mock_result = MagicMock()
    mock_result.scalars.return_value.first.return_value = existing_favorite
    mock_db.execute.return_value = mock_result

    with pytest.raises(HTTPException) as exc_info:
        await favorite_service.create_favorite(db=mock_db, favorite=favorite_data, user=mock_user)

    assert exc_info.value.status_code == 409
    assert exc_info.value.detail == "Coin already favorited"

@pytest.mark.asyncio
async def test_get_user_favorites():
    mock_db = AsyncMock()
    mock_user = UserModel(id=1, name="testuser")
    expected_favorites = [FavoriteModel(id=1, user_id=mock_user.id, coin_id="bitcoin")]

    # Mock the database to return a list of favorites
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = expected_favorites
    mock_db.execute.return_value = mock_result

    result = await favorite_service.get_user_favorites(db=mock_db, user=mock_user)

    assert len(result) == 1
    assert getattr(result[0], 'coin_id') == "bitcoin"

@pytest.mark.asyncio
async def test_delete_favorite_success():
    mock_db = AsyncMock()
    mock_user = UserModel(id=1, name="testuser")
    favorite_to_delete = FavoriteModel(id=1, user_id=mock_user.id, coin_id="bitcoin")

    
    mock_result = MagicMock()
    mock_result.scalars.return_value.first.return_value = favorite_to_delete
    mock_db.execute.return_value = mock_result

    result = await favorite_service.delete_favorite(db=mock_db, favorite_id=1, user=mock_user)

    assert result == {"message": "Favorite deleted successfully"}
    mock_db.delete.assert_called_once_with(favorite_to_delete)
    mock_db.commit.assert_awaited_once()

@pytest.mark.asyncio
async def test_delete_favorite_not_found():
    mock_db = AsyncMock()
    mock_user = UserModel(id=1, name="testuser")

    mock_result = MagicMock()
    mock_result.scalars.return_value.first.return_value = None
    mock_db.execute.return_value = mock_result

    with pytest.raises(HTTPException) as exc_info:
        await favorite_service.delete_favorite(db=mock_db, favorite_id=999, user=mock_user)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Favorite not found"
