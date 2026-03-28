from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from db import get_db
from models import UserModel
from schemas import UserSchema, UserResponse

router = APIRouter()


@router.post("/users", response_model=UserResponse)
async def create_user(user: UserSchema, db: AsyncSession = Depends(get_db)):
    db_user = UserModel(name=user.name, age=user.age, email=user.email)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)

    return {
        "id": db_user.id,
        "name": db_user.name,
        "age": db_user.age,
        "email": db_user.email
    }


@router.get("/users", response_model=list[UserResponse])
async def get_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(UserModel))
    users = result.scalars().all()

    return [
        {
            "id": user.id,
            "name": user.name,
            "age": user.age,
            "email": user.email
        }
        for user in users
    ]


@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(UserModel).where(UserModel.id == user_id))
    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "id": user.id,
        "name": user.name,
        "age": user.age,
        "email": user.email
    }


@router.delete("/users/{user_id}")
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(UserModel).where(UserModel.id == user_id))
    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    await db.delete(user)
    await db.commit()

    return {"message": f"User {user_id} deleted"}


@router.put("/users/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, user_data: UserSchema, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(UserModel).where(UserModel.id == user_id))
    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    user.name = user_data.name
    user.age = user_data.age
    user.email = user_data.email

    await db.commit()
    await db.refresh(user)

    return {
        "id": user.id,
        "name": user.name,
        "age": user.age,
        "email": user.email
    }