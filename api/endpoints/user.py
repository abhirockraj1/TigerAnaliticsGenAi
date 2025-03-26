
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from api.utils import database, security
from api.schemas import user as user_schema
from api.services import user_service
from api.schemas.user import UserRole
from datetime import timedelta

router = APIRouter()

@router.post("/token", response_model=user_schema.Token)
async def login_for_access_token(form_data: security.OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = user_service.get_user_by_username(db, form_data.username)
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": user.username, "role": user.role.value}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/collaborators/validate", response_model=user_schema.UserResponse)
def validate_collaborator(
    creds: user_schema.UserCredentials,
    db: Session = Depends(database.get_db),
):
    user = user_service.get_user_by_username(db, creds.username)
    if not user or user.role != UserRole.collaborator or not security.verify_password(creds.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid collaborator credentials")
    return user

@router.post("/users/", response_model=user_schema.UserResponse)
def create_user(user: user_schema.UserCreate, db: Session = Depends(database.get_db), current_user: user_schema.UserResponse = Depends(security.owner_access)):
    db_user = user_service.create_user(db, user)
    return db_user
@router.post("/owners/", response_model=user_schema.UserResponse)
def create_owner(
    owner_in: user_schema.UserCreate,
    db: Session = Depends(database.get_db),
):
    if(owner_in.role == UserRole.collaborator):
        raise HTTPException(status_code=400, detail="Owner role must be 'owner'")
    elif(user_service.get_user_by_username(db, owner_in.username) != None):
        raise HTTPException(status_code=409, detail="Username already exists")
    db_user = user_service.create_user(db, owner_in)
    return db_user

@router.get("/users/me/", response_model=user_schema.UserResponse)
async def read_users_me(current_user: user_schema.UserResponse = Depends(security.get_current_user)):
    return current_user

@router.get("/users/", response_model=list[user_schema.UserResponse])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db), current_user: user_schema.UserResponse = Depends(security.owner_access)):
    users = user_service.get_users(db, skip=skip, limit=limit)
    return users