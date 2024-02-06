from fastapi import FastAPI, HTTPException
# from fastapi.responses import JSONResponse
from pydantic import BaseModel
from database.car_db import CarDb


class Car(BaseModel):
    id: int
    make: str
    model: str
    color: str | None = None
    year_manufactured: int | None = None
    year_model: int | None = None
    fuel: str | None = None
    horsepower: int | None = None
    doors: int | None = None
    seats: int | None = None
    fipe: str | None = None
    date_created: int
    date_updated: int | None = None


class CarPost(BaseModel):
    make: str
    model: str
    color: str | None = None
    year_manufactured: int | None = None
    year_model: int | None = None
    fuel: str | None = None
    horsepower: int | None = None
    doors: int | None = None
    seats: int | None = None
    fipe: str | None = None


app = FastAPI()


@app.get('/cars')
async def get_cars() -> list[Car]:
    db = CarDb()
    items = []
    for car in db.select_all_cars():
        items.append(Car(**car.__dict__))
    return items


@app.get('/car/{car_id}')
async def get_cars(car_id: int) -> Car:
    db = CarDb()
    c = db.select_car_by_id(car_id=car_id)
    if c is None:
        raise HTTPException(status_code=404, detail="Car not found")
    return Car(**c.__dict__)


@app.post("/car")
async def create_car(car: CarPost):
    return car

# put

# patch

# delete

# @app.put("/items/{item_id}")
# async def create_item(item_id: int, item: Item):
#     return {"item_id": item_id, **item.dict()}


# Because path operations are evaluated in order,
# you need to make sure that the path for /users/me is declared before the one for /users/{user_id}:
# @app.get('/users/me')
# async def read_user_me():
#     return {'user_id': 'the current user'}


# @app.get('/users/{user_id}')
# async def read_user(user_id: str):
#     return {'user_id': user_id}
