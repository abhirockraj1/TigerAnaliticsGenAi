# app/api/schemas/user.py
from pydantic import BaseModel
from enum import Enum

class UserRole(str, Enum):
    owner = "owner"
    collaborator = "collaborator"

class UserCreate(BaseModel):
    username: str
    password: str
    role: UserRole = UserRole.collaborator

class UserResponse(BaseModel):
    id: int
    username: str
    role: UserRole

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str
    role: UserRole

class UserCredentials(BaseModel):
    username: str
    password: str