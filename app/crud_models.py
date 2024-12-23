import datetime
from typing import List, Optional

from pydantic import BaseModel
import uuid

class UserBase(BaseModel):
    name: str
    balance: int

class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    id: uuid.UUID
    timestamp: datetime.datetime

    class Config:
        orm_mode = True

class OrderBase(BaseModel):
    amount: int
    user_id: Optional[uuid.UUID] = None

class OrderCreate(OrderBase):
    pass

class OrderResponse(OrderBase):
    id: uuid.UUID
    timestamp: datetime.datetime

    class Config:
        orm_mode = True


class OrderPlacementRequest(BaseModel):
    user_id: uuid.UUID
    orders: List[OrderBase]


class OrderPlacementResponse(BaseModel):
    total_orders: int
    available_balance: int