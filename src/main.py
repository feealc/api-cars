from fastapi import FastAPI, Response, HTTPException, status
# from fastapi.responses import JSONResponse
from database.car_db import CarDb
from model.car_basemodel import Car, CarPost, CarPut


app = FastAPI()


@app.get('/cars')
async def get_all_cars() -> list[Car]:
    db = CarDb()
    items = []
    for car in db.select_all_cars():
        items.append(Car(**car.__dict__))
    return items


@app.get('/car/{car_id}')
async def get_car(car_id: int) -> Car:
    db = CarDb()
    c = db.select_car_by_id(car_id=car_id)
    if c is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Car not found")
    return Car(**c.__dict__)


@app.post('/car')
async def create_car(car: CarPost, response: Response) -> Car:
    db = CarDb()
    car_id = db.insert_car(new_car=car)
    c = db.select_car_by_id(car_id=car_id)
    response.status_code = status.HTTP_201_CREATED
    return Car(**c.__dict__)


@app.put('/car')
async def update_car(car: CarPut) -> Car:
    db = CarDb()
    c = db.select_car_by_id(car_id=car.id)
    if c is None:
        raise HTTPException(status_code=404, detail="Car not found")
    db.update_car_put(car=car)
    c = db.select_car_by_id(car_id=car.id)
    return Car(**c.__dict__)

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
