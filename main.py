from fastapi import FastAPI

from db import engine, Base
from routes.users import router as users_router

app = FastAPI()


@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.get("/")
async def root():
    return {"message": "Hello, FastAPI!"}


app.include_router(users_router)