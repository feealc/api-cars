from enum import StrEnum
import datetime
import os
import unittest


class Detail(StrEnum):
    MISSING = 'missing'
    STRING_TYPE = 'string_type'
    INT_PARSING = 'int_parsing'
    FIELD_REQUIRED = 'Field required'
    INPUT_VALID_STRING = 'Input should be a valid string'
    INPUT_VALID_INTEGER = 'Input should be a valid integer, unable to parse string as an integer'


class ReturnMessage(StrEnum):
    CAR_NOT_FOUND = 'Car not found'
    BODY_MORE_THAN_ID = 'Body must have at least one field other than id'
    CAR_DELETED = 'Car deleted'
    RESET_COMPLETED = 'Reset completed'


class Generic:

    @staticmethod
    def get_current_date() -> int:
        return int(datetime.datetime.now().strftime('%Y%m%d'))

    @staticmethod
    def get_base_url() -> str:
        return os.environ.get('BASE_URL', 'http://127.0.0.1:8000')

    @staticmethod
    def assert_dict(source: dict, expected: dict) -> None:
        unittest.TestCase().assertEqual(len(source.keys()), len(expected.keys()))
        for key in expected.keys():
            unittest.TestCase().assertTrue(key in source, f'{key} not found in source')
            if expected[key] is None:
                unittest.TestCase().assertIsNone(source[key], f'value {source[key]} for key {key} is not none')
            else:
                unittest.TestCase().assertIsInstance(source[key], type(expected[key]))
                unittest.TestCase().assertIsNotNone(source[key])
                unittest.TestCase().assertEqual(source[key], expected[key])

    @staticmethod
    def car_post() -> dict:
        return {
            'make': 'Porsche',
            'model': 'Cayenne',
            'color': 'Branco',
            'year_manufactured': 2023,
            'year_model': 2024,
            'fuel': 'Gasolina',
            'horsepower': 739,
            'doors': 4,
            'seats': 5,
            'fipe': 'hybrid',
        }

    @staticmethod
    def car_post_expected() -> dict:
        obj = Generic.car_post()
        obj.update({
            'id': 1,
            'date_created': Generic.get_current_date(),
            'date_updated': None,
        })
        return obj

    @staticmethod
    def car_put() -> dict:
        return {
            'id': 1,
            'make': 'Volks',
            'model': 'T-Cross',
            'color': 'Cinza',
            'horsepower': 150,
        }

    @staticmethod
    def car_patch() -> dict:
        return {
            'id': 1,
            'fipe': 'rookie',
        }

    @staticmethod
    def get_detail_info(type_field: Detail,
                        field: str,
                        msg: Detail,
                        input_data: dict | str | int) -> dict:
        return {
            'detail': [
                {
                    'type': type_field.value,
                    'loc': [
                        'body',
                        field
                    ],
                    'msg': msg.value,
                    'input': input_data,
                    'url': f'https://errors.pydantic.dev/2.6/v/{type_field.value}'
                }
            ]
        }
