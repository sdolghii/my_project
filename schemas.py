from pydantic import BaseModel


class UserSchema(BaseModel):
    name: str
    age: int
    email: str | None = None


class UserResponse(BaseModel):
    id: int
    name: str
    age: int
    email: str | None = None