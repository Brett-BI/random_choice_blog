from pydantic import BaseModel

from typing import Optional

class CreateUserRequestModel(BaseModel):
    id: Optional[str]
    full_name: Optional[str]
    email: str
    about: Optional[str]
    password: str
    created_date: Optional[str]
    active: Optional[bool]

class UserResponseModel(BaseModel):
    id: str
    full_name: str
    email: str
    about: str
    created_date: str