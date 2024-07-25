from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from ..schemas import SignUpModel, UserOut
from sqlalchemy.orm import Session
from ..database import get_db
from ..utils import hash_password, verify_password
from ..models import User
from fastapi.security import OAuth2PasswordRequestForm
from ..oauth2 import create_access_token

auth_router = APIRouter(prefix="/auth", tags=['auth'])


@auth_router.post("/signup", status_code=status.HTTP_201_CREATED, response_model=UserOut)
async def register_user(user:SignUpModel, db: Session = Depends(get_db)):
    user_email = db.query(User).filter(User.email == user.email).first()
    user_username = db.query(User).filter(User.username == user.username).first()

    if user_email is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The user with this email already exists")

    if user_username is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The user with this username already exists")

    hashed_password = hash_password(user.password)
    user.password = hashed_password

    new_user = User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@auth_router.post("/login")
async def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user_credentials.username).first()

    if not db_user or not verify_password(user_credentials.password, db_user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")

    access_token = create_access_token({'user_id': db_user.id})

    return {'access_token': access_token, "token_type": "Bearer"}
