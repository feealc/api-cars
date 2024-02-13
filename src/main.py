from fastapi import FastAPI, Response, HTTPException, status
# from fastapi.responses import JSONResponse
from src.database.car_db import CarDb
from src.gen.generic import ReturnMessage
from src.model.car_basemodel import Car, CarPost, CarPut, CarPatch
from pydantic import BaseModel


app = FastAPI()


class Message(BaseModel):
    detail: str


@app.get('/cars')
async def get_all_cars() -> list[Car]:
    db = CarDb()
    items = []
    for car in db.select_all_cars():
        items.append(Car(**car.__dict__))
    return items


@app.get('/car/{car_id}', responses={
    status.HTTP_404_NOT_FOUND: {'model': Message},
})
async def get_car(car_id: int) -> Car:
    db = CarDb()
    c = db.select_car_by_id(car_id=car_id)
    if c is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ReturnMessage.CAR_NOT_FOUND.value)
    return Car(**c.__dict__)


@app.post('/car', responses={
    status.HTTP_400_BAD_REQUEST: {'model': Message},
})
async def create_car(car: CarPost, response: Response) -> Car:
    db = CarDb()
    if db.check_car_exist(make=car.make, model=car.model):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ReturnMessage.CAR_EXIST.value)
    car_id = db.insert_car(new_car=car)
    c = db.select_car_by_id(car_id=car_id)
    response.status_code = status.HTTP_201_CREATED
    return Car(**c.__dict__)


@app.put('/car', responses={
    status.HTTP_400_BAD_REQUEST: {'model': Message},
    status.HTTP_404_NOT_FOUND: {'model': Message},
})
async def update_car(car: CarPut) -> Car:
    db = CarDb()
    c = db.select_car_by_id(car_id=car.id)
    if c is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ReturnMessage.CAR_NOT_FOUND.value)
    if db.check_car_exist(make=car.make, model=car.model):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ReturnMessage.CAR_EXIST.value)
    db.update_car_put(car=car)
    c = db.select_car_by_id(car_id=car.id)
    return Car(**c.__dict__)


@app.patch('/car', responses={
    status.HTTP_404_NOT_FOUND: {'model': Message},
})
async def update_car(car: CarPatch) -> Car:
    db = CarDb()
    _, _, aux = car.get_field_names(ignore_id=True, ignore_value_none=True)
    if len(aux) == 0:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail=ReturnMessage.BODY_MORE_THAN_ID)
    c = db.select_car_by_id(car_id=car.id)
    if c is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ReturnMessage.CAR_NOT_FOUND.value)
    if db.check_car_exist(make=car.make, model=car.model):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ReturnMessage.CAR_EXIST.value)
    db.update_car_patch(car=car)
    c = db.select_car_by_id(car_id=car.id)
    return Car(**c.__dict__)


@app.delete('/car/{car_id}', responses={
    status.HTTP_200_OK: {'model': Message},
    status.HTTP_404_NOT_FOUND: {'model': Message},
})
async def delete_car(car_id: int) -> dict:
    db = CarDb()
    c = db.select_car_by_id(car_id=car_id)
    if c is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ReturnMessage.CAR_NOT_FOUND.value)
    db.delete_car_by_id(car_id=car_id)
    return {'detail': ReturnMessage.CAR_DELETED.value}


@app.post('/reset', include_in_schema=False, responses={
    status.HTTP_200_OK: {'model': Message},
})
async def reset():
    db = CarDb()
    db.delete_all_cars()
    return {'detail': ReturnMessage.RESET_COMPLETED.value}
