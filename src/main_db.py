import argparse
import sys
from database.car_db import CarDb
from model.car import Car


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
    # db.delete_all_cars()
    # db.insert_car(Car(make='Volks', model='T-Cross'))
    # db.insert_car(Car(make='Volks', model='Taos'))
    # db.insert_car(Car(make='Volks', model='Nivus'))
    ret = db.select_all_cars(debug=True)
    # print(ret)