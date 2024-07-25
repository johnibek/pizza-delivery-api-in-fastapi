from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy_utils.types import ChoiceType
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    is_active = Column(Boolean, server_default="FALSE")
    is_staff = Column(Boolean, server_default="FALSE")

    order = relationship('Order', back_populates='user')

    def __str__(self):
        return {self.username}


class Order(Base):
    __tablename__ = "orders"

    ORDER_STATUS = (
        ('PENDING', 'pending'),
        ('IN-PROGRESS', 'in-progress'),
        ('DELIVERED', 'delivered')
    )

    PIZZA_SIZES = (
        ('SMALL', 'small'),
        ('MEDIUM', 'medium'),
        ('LARGE', 'large'),
        ('EXTRA-LARGE', 'extra-large')
    )

    id = Column(Integer, primary_key=True, nullable=False)
    quantity = Column(Integer, nullable=False)
    order_status = Column(ChoiceType(choices=ORDER_STATUS), server_default="PENDING")
    pizza_size = Column(ChoiceType(choices=PIZZA_SIZES), server_default='SMALL')
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)

    user = relationship('User', back_populates='order')

