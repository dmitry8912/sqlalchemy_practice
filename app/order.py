import uuid
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud_models import UserCreate, UserResponse
from app.session import get_session

from app.crud_models import OrderCreate, OrderResponse
from models import User, Order

order_router = APIRouter()


@order_router.post("/orders/", response_model=OrderResponse)
async def create_order(order: OrderCreate, session: AsyncSession = Depends(get_session)):
    new_order = Order(amount=order.amount, user_id=order.user_id)
    session.add(new_order)
    await session.commit()
    await session.refresh(new_order)
    return new_order

@order_router.get("/orders/", response_model=List[OrderResponse])
async def get_orders(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Order))
    orders = result.scalars().all()
    return orders

@order_router.get("/orders/{order_id}", response_model=OrderResponse)
async def get_order(order_id: uuid.UUID, session: AsyncSession = Depends(get_session)):
    order = await session.get(Order, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@order_router.put("/orders/{order_id}", response_model=OrderResponse)
async def update_order(order_id: uuid.UUID, updated_order: OrderCreate, session: AsyncSession = Depends(get_session)):
    order = await session.get(Order, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    order.amount = updated_order.amount
    order.user_id = updated_order.user_id
    await session.commit()
    await session.refresh(order)
    return order

@order_router.delete("/orders/{order_id}", status_code=204)
async def delete_order(order_id: uuid.UUID, session: AsyncSession = Depends(get_session)):
    order = await session.get(Order, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    await session.delete(order)
    await session.commit()