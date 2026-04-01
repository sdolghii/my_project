from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from db import engine, Base, get_db
from models import UserModel
from routes.users import router as users_router
from pydantic import BaseModel
from auth import hash_password, verify_password, create_access_token, get_current_user
from fastapi.security import HTTPBearer

from fastapi.openapi.utils import get_openapi

app = FastAPI()

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="My API",
        version="0.1.0",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
        }
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.get("/")
async def root():
    return {"message": "Hello, FastAPI!"}


app.include_router(users_router)

class RegisterSchema(BaseModel):
    name: str
    age: int
    email: str
    password: str

@app.post("/register")
async def register(user: RegisterSchema, db: AsyncSession = Depends(get_db)):
    db_user = UserModel(
        name=user.name,
        age=user.age,
        email=user.email,
        hashed_password=hash_password(user.password)
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return {"message": "User created", "id": db_user.id}

@app.post("/login")
async def login(email: str, password: str, db: AsyncSession = Depends(get_db)):
    from sqlalchemy import select
    result = await db.execute(select(UserModel).where(UserModel.email == email))
    user = result.scalar_one_or_none()
    if not user or not verify_password(password, user.hashed_password):
        from fastapi import HTTPException
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}