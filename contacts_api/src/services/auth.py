import asyncio
from typing import Optional
from datetime import datetime, timedelta

from sqlalchemy.orm import Session
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt

from src.db.db import get_db
from src.repository.users import get_user_by_email


class Authorization:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    SECRET_KEY = "main_key"
    ALGORITHM = "HS256"
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

    def verify_password(self, plain_password, password: str):
        return self.pwd_context.verify(plain_password, password)

    def get_password_hash(self, password: str):
        return self.pwd_context.hash(password)

    # Define function for new access token
    async def create_access_token(self, data: dict, expires_delta: Optional[float] = None):
        to_encode = data.copy()
        
        if expires_delta:
            expire = datetime.utcnow() + timedelta(seconds=expires_delta)
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)

        to_encode.update({"iat": datetime.utcnow(), "exp": expire, "scope": "access_token"})
        encoded_access_token = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        
        return encoded_access_token
    
    # Define function for new refresh token
    async def create_refresh_token(self, data: dict, expires_delta: Optional[float] = None):
        to_encode = data.copy()
        
        if expires_delta:
            expire = datetime.utcnow() + timedelta(seconds=expires_delta)
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)

        to_encode.update({"iat": datetime.utcnow(), "exp": expire, "scope": "refresh_token"})
        encoded_refresh_token = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_refresh_token

    # Get current user
    async def get_current_user(self, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
        credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Couldn't validate credentials!", headers={"WWW-Authenticate": "Bearer"})

        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])

            if payload.get("scope") == "access_token":
                email = payload.get("sub")
                if email is None:
                    raise credentials_exception
            else:
                raise credentials_exception
        except JWTError:
            raise credentials_exception
        
        user = await get_user_by_email(email, db)
        if user is None:
            raise credentials_exception
        return user
    # Get email by refresh_token
    async def decode_refresh_token(self, refresh_token: str):
        try:
            payload = jwt.decode(refresh_token, self.SECRET_KEY, algorithms=[self.ALGORITHM])

            if payload['scope'] == 'refresh_token':
                email = payload['sub']
                return email
            
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid scope for token")
        except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

auth_service = Authorization()



# async def get_access_token():
#     access_token = await auth_service.create_access_token(data=data, expires_delta=None)
#     return "Access token:", access_token

# async def get_refresh_token():
#     refresh_token = await auth_service.create_access_token(data=data, expires_delta=None)
#     return "Refresh token:", refresh_token


# async def main():
   
#     access_token = await get_access_token()
#     refresh_token = await get_refresh_token()

#     return access_token, refresh_token




# if __name__ == '__main__':
    
    
#     data = {
#         "username": 'artem',
#         "password": 'qwerty'
#     }

#     result = asyncio.run(main())
#     print(result)

    # decoded_token = jwt.decode(token, "main_key", algorithms=["HS256"])
    # print(decoded_token)