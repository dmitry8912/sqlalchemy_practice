import time
import uuid
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud_models import UserCreate, UserResponse
from app.session import get_session
from models import User

user_router = APIRouter()

@user_router.post("/users/", response_model=UserResponse)
async def create_user(user: UserCreate, session: AsyncSession = Depends(get_session)):
    new_user = User(name=user.name, balance=user.balance)
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return new_user

@user_router.get("/users/", response_model=List[UserResponse])
async def get_users(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(User))
    users = result.scalars().all()
    return users

@user_router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: uuid.UUID, session: AsyncSession = Depends(get_session)):
    t1 = time.time()
    user = await session.get(User, user_id)
    print(f"Get user {time.time() - t1} seconds")
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@user_router.put("/users/{user_id}", response_model=UserResponse)
async def update_user(user_id: uuid.UUID, updated_user: UserCreate, session: AsyncSession = Depends(get_session)):
    user = await session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.name = updated_user.name
    user.balance = updated_user.balance
    await session.commit()
    await session.refresh(user)
    return user

@user_router.delete("/users/{user_id}", status_code=204)
async def delete_user(user_id: uuid.UUID, session: AsyncSession = Depends(get_session)):
    user = await session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    await session.delete(user)
    await session.commit()