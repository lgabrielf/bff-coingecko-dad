from pydantic import BaseModel, ConfigDict

class FavoriteCreateDTO(BaseModel):
    coin_id: str

    class ConfigDict:
        json_schema_extra = {
            "example": {
                "coin_id": "bitcoin"
            }
        }

class FavoriteResponseDTO(BaseModel):
    id: int
    user_id: int
    coin_id: str

    class ConfigDict:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "user_id": 1,
                "coin_id": "bitcoin"
            }
        }
