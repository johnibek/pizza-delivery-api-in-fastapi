from fastapi import APIRouter, status, HTTPException, Depends
from ..oauth2 import get_current_user
from ..schemas import UserOut, UpdateUser
from ..database import get_db
from sqlalchemy.orm import Session
from ..models import User
from ..utils import hash_password

user_router = APIRouter(tags=['users'], prefix="/users")


@user_router.get("/", response_model=list[UserOut])
async def get_users(current_user: UserOut = Depends(get_current_user), db: Session = Depends(get_db)):
    if not current_user.is_staff:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You do not have permission to perform this action.")

    users = db.query(User).all()

    return users


@user_router.get("/{user_id}", response_model=UserOut)
async def get_user(user_id: int, current_user: UserOut = Depends(get_current_user), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"There is no user with this id {user_id}.")

    if not current_user.is_staff and current_user.id != user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You do not have permission to perform this action.")

    return user


@user_router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def get_user(user_id: int, current_user: UserOut = Depends(get_current_user), db: Session = Depends(get_db)):
    user_query = db.query(User).filter(User.id == user_id)

    user = user_query.first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"There is no user with this id {user_id}.")

    if not current_user.is_staff and current_user.id != user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You do not have permission to perform this action.")

    user_query.delete(synchronize_session=False)
    db.commit()


@user_router.put("/{user_id}", response_model=UserOut)
async def get_user(user_id: int, user_detail: UpdateUser, current_user: UserOut = Depends(get_current_user), db: Session = Depends(get_db)):
    user_query = db.query(User).filter(User.id == user_id)

    user = user_query.first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"There is no user with this id {user_id}.")

    if not current_user.is_staff and current_user.id != user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You do not have permission to perform this action.")

    hashed_password = hash_password(user_detail.password)
    user_detail.password = hashed_password

    user_query.update(user_detail.model_dump(), synchronize_session=False)

    db.commit()

    return user_query.first()
