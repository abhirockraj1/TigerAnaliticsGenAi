# app/api/models/user.py
from sqlalchemy import Column, Integer, String, Enum
from api.utils.database import Base
from api.schemas.user import UserRole as RoleEnum

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(Enum(RoleEnum), default=RoleEnum.collaborator)