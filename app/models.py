from pydantic import BaseModel


class User(BaseModel):
    email: str
    full_name: str
    password: str
    id: int


class Flower(BaseModel):
    name: str
    count: int
    cost: int
    id: int = 0
