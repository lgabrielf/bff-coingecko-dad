from pydantic import BaseModel
from typing import Optional

class UserDTO(BaseModel):

    id: Optional[int] = None
    name: str
    password: str

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "name": "John Doe",
                "password": "securepassword",
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
