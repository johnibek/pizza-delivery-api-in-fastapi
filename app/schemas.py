from pydantic import BaseModel, EmailStr
from enum import Enum

class UserBase(BaseModel):
    username: str
    email: EmailStr
    is_active: bool = True
    is_staff: bool = False


class SignUpModel(UserBase):
    password: str

    class Config:
        json_schema_extra={
            "examples": [
                {
                    "username": "johndoe",
                    "email": "johndoe@gmail.com",
                    "password": "john123",
                    "is_active": True,
                    "is_staff": False
                }
            ]
        }

class UpdateUser(UserBase):
    password: str

    class Config:
        json_schema_extra={
            "examples": [
                {
                    "username": "johndoe",
                    "email": "johndoe@gmail.com",
                    "password": "john123",
                    "is_active": True,
                    "is_staff": False
                }
            ]
        }


class UserOut(UserBase):
    id: int

    class Config:
        orm_mode = True


class TokenData(BaseModel):
    id: int | None = None


# Order model
class OrderStatus(str, Enum):
    pending='PENDING'
    in_progress = 'IN-PROGRESS'
    delivered = 'DELIVERED'

class PizzaSize(str, Enum):
    small = 'SMALL'
    medium = 'MEDIUM'
    large = 'LARGE'
    extra_large = 'EXTRA-LARGE'


class BaseOrder(BaseModel):
    quantity: int
    pizza_size: PizzaSize = PizzaSize.small

class CreateOrder(BaseOrder):
    class Config:
        json_schema_extra={
            "examples": [
                {
                    "quantity": 3,
                    "pizza_size": "LARGE"
                }
            ]
        }

class UpdateOrder(BaseOrder):
    class Config:
        json_schema_extra={
            "examples": [
                {
                    "quantity": 3,
                    "pizza_size": "LARGE"
                }
            ]
        }


class UpdateOrderStatus(BaseModel):
    order_status: OrderStatus = OrderStatus.pending

    class Config:
        json_schema_extra={
            "examples": [
                {
                    'order_status': "PENDING"
                }
            ]
        }

class ChoiceModel(BaseModel):
    code: str
    value: str

class OrderOut(BaseModel):
    id: int
    quantity: int
    order_status: ChoiceModel
    pizza_size: ChoiceModel
    user_id: int
    user: UserOut

    class Config:
        orm_model = True
