import sqlite3
import os
from pathlib import Path
from gen.generic import Generic
from model.car import Car


class CarDb:
    def __init__(self):
        self.db_name = os.path.join(Path(__file__).parent.parent.parent, 'cars.db')
        self.__conn = None
        self.__cursor = None
        self.__tb_cars = 'tb_cars'

    def __connect(self) -> None:
        self.__conn = sqlite3.connect(self.db_name)
        self.__cursor = self.__conn.cursor()

    def __commit(self) -> None:
        if self.__conn:
            self.__conn.commit()

    def __close_conn(self) -> None:
        if self.__conn:
            self.__conn.close()

    def __table_exist(self, table_name: str) -> bool:
        self.__connect()
        self.__cursor.execute(f"""
        SELECT name FROM sqlite_master WHERE type='table' and name='{table_name}'
        """)
        return False if self.__cursor.fetchone() is None else True

    def __create_table_cars(self) -> None:
        print(f'Criando tabela {self.__tb_cars}')
        self.__connect()
        self.__cursor.execute(f"""
        CREATE TABLE {self.__tb_cars} (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            make TEXT NOT NULL,
            model TEXT NOT NULL,
            color TEXT,
            year_manufactured INTEGER,
            year_model INTEGER,
            fuel TEXT,
            horsepower INTEGER,
            doors INTEGER,
            seats INTEGER,
            fipe TEXT,
            date_created INTEGER NOT NULL,
            date_updated INTEGER
        );
        """)
        self.__commit()
        self.__close_conn()
        self.reset_auto_increment_cars()

    def prepare(self):
        self.__connect()
        self.__close_conn()

        if not self.__table_exist(table_name=self.__tb_cars):
            self.__create_table_cars()

    def list_all_tables(self, debug: bool = False):
        self.__connect()
        self.__cursor.execute("""
        SELECT name FROM sqlite_master WHERE type='table' ORDER BY name
        """)
        all_tables = self.__cursor.fetchall()
        if debug:
            print('Tabelas:')
            for tabela in all_tables:
                print('> [%s]' % tabela)
        self.__close_conn()
        return all_tables

    def list_columns_from_table(self, table_name: str, debug: bool = False):
        self.__connect()
        self.__cursor.execute('PRAGMA table_info({})'.format(table_name))
        cols = [tupla[1] for tupla in self.__cursor.fetchall()]
        if debug:
            print(f'Colunas tabela {table_name}: {cols}')
        self.__close_conn()
        return cols

    """
    ===============================================================================================
    INSERT
    ===============================================================================================
    """
    # def insert_car(self, marca: str, modelo: str, data_criacao: int = None):
    #     if data_criacao is None:
    #         data_criacao = Generic.get_current_date()
    #
    #     self.__connect()
    #     self.__cursor.execute(f"""
    #     INSERT INTO {self.__tb_cars}
    #     (marca, modelo, data_criacao)
    #     VALUES (?,?,?)
    #     """, (marca, modelo, data_criacao))
    #     self.__commit()
    #     self.__close_conn()

    def insert_car(self, new_car: Car):
        self.__connect()
        self.__cursor.execute(f"""
        INSERT INTO {self.__tb_cars}
        (make, model, date_created)
        VALUES (?,?,?)
        """, (new_car.make, new_car.model, new_car.date_created))
        self.__commit()
        self.__close_conn()

    """
    ===============================================================================================
    SELECT
    ===============================================================================================
    """
    def select_all_cars(self, debug: bool = False, order_by: str = 'id') -> [Car]:
        self.__connect()
        self.__cursor.execute(f"""
        SELECT * FROM {self.__tb_cars} ORDER BY {order_by};
        """)
        lines = self.__cursor.fetchall()
        lines_ret = []
        for line in lines:
            if debug:
                print(line)
            c = Car(make='', model='')
            c.load_from_tuple(line)
            # print(c)
            lines_ret.append(c)
        self.__close_conn()
        return lines_ret

    def select_car_by_id(self, car_id: int, debug: bool = False) -> Car:
        self.__connect()
        self.__cursor.execute(f"""
        SELECT * FROM {self.__tb_cars} WHERE id = {car_id};
        """)
        line = self.__cursor.fetchone()
        if debug:
            print(line)
        if line is None:
            return
        c = Car(make='', model='')
        c.load_from_tuple(line)
        self.__close_conn()
        return c

    """
    ===============================================================================================
    UPDATE
    ===============================================================================================
    """

    """
    ===============================================================================================
    DELETE
    ===============================================================================================
    """
    def delete_all_cars(self):
        self.__connect()
        self.__cursor.execute(f"""
        DELETE FROM {self.__tb_cars};
        """)
        self.__commit()
        self.__close_conn()
        self.reset_auto_increment_cars()

    """
    ===============================================================================================
    RESET
    ===============================================================================================
    """
    def __reset_auto_increment(self, table_name: str):
        self.__connect()
        self.__cursor.execute(f"""
        UPDATE SQLITE_SEQUENCE SET SEQ = 0 WHERE NAME = '{table_name}';
        """)
        self.__commit()
        self.__close_conn()

    def reset_auto_increment_cars(self):
        self.__reset_auto_increment(table_name=self.__tb_cars)
