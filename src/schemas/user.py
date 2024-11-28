from pydantic import BaseModel
from typing import Optional

class UserDTO(BaseModel):

    id: Optional[int] = None
    name: str
    password: str

    class Config:
        from_attributes = True
        schema_extra = {
            "example": {
                "id": 1,
                "name": "John Doe",
                "password": "securepassword",
                "email": "john.doe@example.com"
            }
        }

class UserCreateDTO(UserDTO):
    password: str

    class Config:
        from_attributes = True

class UserSchemaUp(UserDTO):
    name: Optional[str]
    password: Optional[str]

    class Config:
        from_attributes = True
