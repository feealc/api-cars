# import argparse
# import sys
from src.database.car_db import CarDb
# from src.model.car import Car
from src.model.car_basemodel import CarPost


def prepare_for_test():
    db = CarDb()
    db.prepare()

    db.delete_all_cars()
    db.insert_car(CarPost(make='Volks', model='T-Cross', color='Cinza',
                          year_manufactured=2019, year_model=2020,
                          fuel='Flex', horsepower=150, doors=4, seats=5, fipe='brum')
                  )


if __name__ == '__main__':
    # parser = argparse.ArgumentParser()
    # parser.add_argument('-e', '--email', action='store_true', help='Não realizar envio do e-mail com os resultados')
    # parser.add_argument('-t', '--test', action='store_true', help='Executar apenas função de teste')
    # args = parser.parse_args()

    # logger.setLevel(logging.DEBUG)

    # if args.test:
    #     test_func()
    #     sys.exit(0)

    # logger.info('### Início')

    # obj = HandlerJsonProject()
    db = CarDb()
    db.prepare()

    # db.list_all_tables(debug=True)
    # db.list_columns_from_table(table_name='tb_cars', debug=True)

    # cars
    db.delete_all_cars()
    db.insert_car(CarPost(make='Volks',
                          model='T-Cross',
                          color='Cinza',
                          year_manufactured=2019,
                          year_model=2020,
                          fuel='Flex',
                          horsepower=150,
                          doors=5,
                          seats=5,
                          fipe='brum'))
    db.insert_car(CarPost(make='Volks', model='Taos'))
    db.insert_car(CarPost(make='Mercedes', model='Sprinter'))
    db.insert_car(CarPost(make='Hyundai', model='HB20'))
    ret = db.select_all_cars(debug=True)
    # print(ret)
