from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from db import engine, Base, get_db
from models import UserModel
from schemas import UserSchema

app = FastAPI()


@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.get("/")
async def root():
    return {"message": "Hello, FastAPI!"}


@app.post("/users")
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


@app.get("/users")
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


@app.get("/users/{user_id}")
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(UserModel).where(UserModel.id == user_id))
    user = result.scalar_one_or_none()

    if user is None:
        return {"error": "User not found"}

    return {
        "id": user.id,
        "name": user.name,
        "age": user.age,
        "email": user.email
    }


@app.delete("/users/{user_id}")
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(UserModel).where(UserModel.id == user_id))
    user = result.scalar_one_or_none()

    if user is None:
        return {"error": "User not found"}

    await db.delete(user)
    await db.commit()

    return {"message": f"User {user_id} deleted"}


@app.put("/users/{user_id}")
async def update_user(user_id: int, user_data: UserSchema, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(UserModel).where(UserModel.id == user_id))
    user = result.scalar_one_or_none()

    if user is None:
        return {"error": "User not found"}

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