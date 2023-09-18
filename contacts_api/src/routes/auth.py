from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session


from src.db.db import get_db
from src.schemas.users_schema import UserModel, UserResponse
from src.schemas.tokens_schema import TokenModel
from src.repository.users import create_user, get_user_by_email, update_token
from src.services.auth import auth_service

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def signup(body: UserModel, db: Session = Depends(get_db)):
    exist_user = await get_user_by_email(body.email, db)
    if exist_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Account with email {exist_user.email} already exist!")

    body.password = auth_service.get_password_hash(body.password)
    new_user = await create_user(body, db)
    return new_user

@router.post('/login', response_model=TokenModel)
async def login(body: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    unauthorizedExc = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password!")
    user = await get_user_by_email(body.username, db)
    if user is None:
        raise unauthorizedExc
    if not auth_service.verify_password(body.password, user.password):
        raise unauthorizedExc
    
    access_token = await auth_service.create_access_token(data={"sub": user.email})
    refresh_token = await auth_service.create_refresh_token(data={"sub": user.email})
    await update_token(user, refresh_token, db)
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

    

# Refresh token update