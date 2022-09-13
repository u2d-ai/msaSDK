# -*- coding: utf-8 -*-
from typing import Optional
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta
from sqlmodel import SQLModel

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')


class MSATokenData(SQLModel):
    """TokenData schema"""
    id: Optional[str]
    """User ID"""


class MSAToken:

    def __init__(self, secret_key: str, algorithm: str = "HS256"):
        """MSAToken

        Args:
            secret_key: The secret key to produce a Token
            algorithm: Algo to use, default ``HS256``
        """
        super().__init__()
        self.secret_key: str = secret_key
        self.algorithm: str = algorithm
        self.credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                                   detail="Could not validate credentials",
                                                   headers={"WWW-Authenticate": "Bearer"})

    async def create_token(self, data: dict, expire_minutes: int = 100) -> str:
        """Create a Token

            Args:
                data: the data and content used to build the token
                expire_minutes: the time the token is valid, expires

            Returns:
                encoded_jwt: jwt encoded token
        """
        to_encode = data.copy()
        # Use utcnow, not now
        expire = datetime.utcnow() + timedelta(minutes=expire_minutes)
        to_encode.update({"exp": expire})

        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    async def verify_token(self, token: str) -> MSATokenData:
        """Verify Token

            Args:
                token: the token as str

            Raises:
                JWTError: credentials_exception

            Returns:
                token_data: the jwt decoded data
        """
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            id: str = payload.get("user_id")
            if id is None:
                raise self.credentials_exception
            # Validate
            token_data = MSATokenData(id=id)
        except JWTError:
            raise self.credentials_exception

        return token_data

    async def get_current_user(self, token: str = Depends(oauth2_scheme)):

        token = await self.verify_token(token)
        return token
