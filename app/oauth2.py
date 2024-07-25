import jwt
from jwt.exceptions import InvalidTokenError
from fastapi.security import OAuth2PasswordBearer
from .config import settings
from datetime import datetime, timezone, timedelta
from .schemas import TokenData
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from .database import get_db
from .models import User


oauth2_schema = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


def create_access_token(data: dict):
    payload = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload.update({'exp': expire})

    access_token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    return access_token


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get('user_id')
        if not user_id:
            raise credentials_exception
        token_data = TokenData(id=user_id)

    except InvalidTokenError:
        raise credentials_exception

    return token_data


def get_current_user(token: str = Depends(oauth2_schema), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials", headers={'WWW-Authenticate': "Bearer"})
    token_data = verify_access_token(token, credentials_exception)
    user = db.query(User).filter(User.id == token_data.id).first()

    return user

