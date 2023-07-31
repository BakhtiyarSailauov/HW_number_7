from typing import Dict, List

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt
from fastapi import FastAPI, HTTPException, Form, Depends, Request
from starlette.responses import JSONResponse

from flowers_repository import FlowersRepository
from users_repository import UsersRepository
from models import User, Flower

app = FastAPI()

flowers_repository = FlowersRepository()
users_repository = UsersRepository()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
shopping_cart = []


def create_jwt(id: int) -> str:
    body = {"id": id}
    token = jwt.encode(body, "BadBreacking", "HS256")
    return token


def decode_jwt(token: str) -> int:
    data = jwt.decode(token, "BadBreacking", "HS256")
    return data["id"]


@app.post("/signup", status_code=200)
def post_signup(user: User):
    try:
        users_repository.save(user)
    except KeyError:
        raise HTTPException(status_code=400, detail="User already exists")

    return {"message": "User registered successfully"}


@app.post("/login", status_code=200, response_model=Dict[str, str])
def post_login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = users_repository.get_by_email(form_data.username)
    if user is None or user.password != form_data.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_jwt(user.id)
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/profile", status_code=200, response_model=User)
def get_profile(token: str = Depends(oauth2_scheme)):
    user_id = decode_jwt(token)
    user = users_repository.get_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    user.password = None
    return user


@app.get("/flowers", status_code=200, response_model=List[Flower])
def get_flowers(token: str = Depends(oauth2_scheme)):
    user_id = decode_jwt(token)
    user = users_repository.get_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    flowers = flowers_repository.get_all()
    return flowers


@app.post("/flowers")
def post_flowers(flower: Flower):
    try:
        flowers_repository.save(flower)
    except KeyError:
        raise HTTPException(status_code=400, detail="Flower already exists")

    return {"message": "Flower registered successfully",
            "flower_id": flower.id
            }


@app.post("/cart/items", status_code=200)
def add_to_cart(flower_id: int = Form()):
    shopping_cart.append(flower_id)
    response = JSONResponse(content={"message": "Item added to cart successfully"}, status_code=200)
    response.set_cookie(key="cart_items", value=",".join(map(str, shopping_cart)))
    return response


@app.get("/cart/items")
def get_to_cart(request: Request):
    cart_items = request.cookies.get("cart_items")
    cart_flowers = []
    total_price = 0.0

    if cart_items:
        cart_items_list = list(map(int, cart_items.split(",")))
        for flower_id in cart_items_list:
            flower = flowers_repository.get_by_id(flower_id)
            if flower:
                cart_flowers.append(flower)
                total_price += flower.cost

    return {
        "cart_flowers": cart_flowers,
        "total_price": total_price
    }
