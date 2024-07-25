from fastapi import APIRouter, Depends, status, HTTPException
from ..oauth2 import get_current_user
from ..schemas import UserOut, CreateOrder, OrderOut, UpdateOrder, UpdateOrderStatus
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Order


order_router = APIRouter(prefix='/orders', tags=['order'])


@order_router.post('/', status_code=status.HTTP_201_CREATED, response_model=OrderOut)
async def create_order(order: CreateOrder, current_user: UserOut = Depends(get_current_user), db: Session = Depends(get_db)):
    new_order = Order(**order.model_dump(), user_id=current_user.id)
    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    return new_order


@order_router.get("/", status_code=status.HTTP_200_OK, response_model=list[OrderOut])
async def get_all_orders(current_user: UserOut = Depends(get_current_user), db: Session = Depends(get_db)):
    orders = db.query(Order)

    if not current_user.is_staff:
        return current_user.order

    return orders.all()


@order_router.get("/{order_id}", status_code=status.HTTP_200_OK, response_model=OrderOut)
async def get_one_order(order_id: int, current_user: UserOut = Depends(get_current_user), db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()

    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="There is no order with this specific id.")

    if not current_user.is_staff and order.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You do not have permission to perform this action.")

    return order


@order_router.put("/{order_id}", status_code=status.HTTP_200_OK, response_model=OrderOut)
async def update_order(order_id: int,
                       updated_order: UpdateOrder,
                       current_user: UserOut = Depends(get_current_user),
                       db: Session = Depends(get_db)):

    order = db.query(Order).filter(Order.id == order_id)

    if not order.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="There is no order with this specific id.")

    if order.first().user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You do not have permission to perform this action.")

    order.update(updated_order.model_dump(), synchronize_session=False)

    db.commit()

    return order.first()


@order_router.patch("/{order_id}/status", status_code=status.HTTP_200_OK, response_model=OrderOut)
async def update_order_status(order_id: int,
                              updated_order_status: UpdateOrderStatus,
                              current_user: UserOut = Depends(get_current_user),
                              db: Session = Depends(get_db)):

    order = db.query(Order).filter(Order.id == order_id)

    if not order.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="There is no order with this specific id.")

    if not current_user.is_staff:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You do not have permission to perform this action.")


    order.update(updated_order_status.model_dump(), synchronize_session=False)

    db.commit()

    return order.first()


@order_router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_order(order_id: int, current_user: UserOut = Depends(get_current_user), db: Session = Depends(get_db)):
    order_query = db.query(Order).filter(Order.id == order_id)

    order = order_query.first()

    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="There is no order with this specific id.")

    if not current_user.is_staff and current_user.id != order.user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You do not have permission to perform this action")


    order_query.delete(synchronize_session=False)
    db.commit()








