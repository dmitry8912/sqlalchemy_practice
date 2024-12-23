import time
import uuid
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import noload
from sqlalchemy.sql.functions import count

from app.crud_models import UserCreate, UserResponse, OrderPlacementRequest, OrderPlacementResponse
from app.session import get_session
from models import User, Order

marketplace_router = APIRouter()

@marketplace_router.post("/marketplace/v1/", response_model=OrderPlacementResponse)
async def place_order_v1(order_placement: OrderPlacementRequest, session: AsyncSession = Depends(get_session)):
    """First approach."""
    user = (await session.execute(select(User).where(User.id == order_placement.user_id))).scalars().first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    for order in order_placement.orders:
        if order.amount <= 0:
            raise HTTPException(detail="Amount can not be negative", status_code=400)
        placed_order = Order(amount=order.amount, user_id=order_placement.user_id)
        session.add(placed_order)
        user.balance -= order.amount
        await session.commit()

    await session.refresh(user)
    return OrderPlacementResponse(total_orders=len(user.user_orders), available_balance=user.balance)

@marketplace_router.post("/marketplace/v2/", response_model=OrderPlacementResponse)
async def place_order_v2(order_placement: OrderPlacementRequest, session: AsyncSession = Depends(get_session)):
    """Commit after all objects saved."""
    user = (await session.execute(select(User).where(User.id == order_placement.user_id))).scalars().first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    for order in order_placement.orders:
        if order.amount <= 0:
            raise HTTPException(detail="Amount can not be negative", status_code=400)
        placed_order = Order(amount=order.amount, user_id=order_placement.user_id)
        session.add(placed_order)
        user.balance -= order.amount
        await session.flush()

    await session.commit()
    await session.refresh(user)
    return OrderPlacementResponse(total_orders=len(user.user_orders), available_balance=user.balance)

@marketplace_router.post("/marketplace/v3/", response_model=OrderPlacementResponse)
async def place_order_v3(order_placement: OrderPlacementRequest, session: AsyncSession = Depends(get_session)):
    """Count user orders and balance by query."""
    user = (await session.execute(select(User).options(noload(User.user_orders)).where(User.id == order_placement.user_id))).scalars().first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    for order in order_placement.orders:
        if order.amount <= 0:
            raise HTTPException(detail="Amount can not be negative", status_code=400)
        placed_order = Order(amount=order.amount, user_id=order_placement.user_id)
        session.add(placed_order)
        user.balance -= order.amount
        await session.flush()

    await session.commit()
    orders_count_query = select(count(Order.id)).filter(Order.user_id == user.id).subquery("user_orders")
    query = select(User.balance, orders_count_query).filter(User.id == order_placement.user_id)
    result = (await session.execute(query)).first()
    return OrderPlacementResponse(total_orders=result[0], available_balance=result[1])

@marketplace_router.post("/marketplace/v4/", response_model=OrderPlacementResponse)
async def place_order_v4(order_placement: OrderPlacementRequest, session: AsyncSession = Depends(get_session)):
    """Block user."""
    user_query = select(User).filter(User.id == order_placement.user_id).with_for_update()
    user = (await session.execute(user_query)).scalars().first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    for order in order_placement.orders:
        if order.amount <= 0:
            raise HTTPException(detail="Amount can not be negative", status_code=400)
        placed_order = Order(amount=order.amount, user_id=order_placement.user_id)
        session.add(placed_order)
        user.balance -= order.amount
        await session.flush()

    await session.commit()
    orders_count_query = select(count(Order.id)).filter(Order.user_id == user.id).subquery("user_orders")
    query = select(User.balance, orders_count_query).filter(User.id == order_placement.user_id)
    result = (await session.execute(query)).first()
    return OrderPlacementResponse(total_orders=result[0], available_balance=result[1])

@marketplace_router.post("/marketplace/v5/", response_model=OrderPlacementResponse)
async def place_order_v5(order_placement: OrderPlacementRequest, session: AsyncSession = Depends(get_session)):
    """Block user and reload from database."""
    user_query = select(User).filter(User.id == order_placement.user_id)

    user = (await session.execute(user_query)).scalars().first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user_query = select(User).filter(User.id == order_placement.user_id).filter(User.balance > 0)

    # Produces reload from db
    user_query = user_query.execution_options(populate_existing=True)

    user = (await session.execute(user_query)).scalars().first()

    for order in order_placement.orders:
        if order.amount <= 0:
            raise HTTPException(detail="Amount can not be negative", status_code=400)
        placed_order = Order(amount=order.amount, user_id=order_placement.user_id)
        session.add(placed_order)
        user.balance -= order.amount
        await session.flush()

    await session.commit()
    orders_count_query = select(count(Order.id)).filter(Order.user_id == user.id).subquery("user_orders")
    query = select(User.balance, orders_count_query).filter(User.id == order_placement.user_id)
    result = (await session.execute(query)).first()
    return OrderPlacementResponse(total_orders=result[0], available_balance=result[1])
