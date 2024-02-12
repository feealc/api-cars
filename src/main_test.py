from datetime import datetime
from fastapi import status
from src.main_db import prepare_for_test
# from model.car import Car
# from typing import Any
import requests
import unittest


# RUN - python -m unittest -v main_test


class MyTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        prepare_for_test()
        cls.base_url = 'http://127.0.0.1:8000'
        # cls.base_url = 'http://0.0.0.0:8080'
        cls.car_expected = {
            'id': 1,
            'make': 'Volks',
            'model': 'T-Cross',
            'color': 'Cinza',
            'year_manufactured': 2019,
            'year_model': 2020,
            'fuel': 'Flex',
            'horsepower': 150,
            'doors': 4,
            'seats': 5,
            'fipe': 'brum',
            'date_created': cls.get_current_date_int(),
            'date_updated': None,
        }
        cls.car_new = {
            'make': 'Porsche',
            'model': 'Cayenne',
            'color': 'Branco',
            'year_manufactured': 2023,
            'year_model': 2024,
            'fuel': 'Gasolina',
            'horsepower': 739,
            'doors': 4,
            'seats': 5,
            'fipe': 'hybrid'
        }
        cls.car_new_id = 2
        cls.car_put = {
            'id': cls.car_new_id,
            'make': 'BMW',
            'model': 'X6'
        }

    def setUp(self) -> None:
        pass

    @staticmethod
    def get_current_date_int():
        return int(datetime.now().strftime('%Y%m%d'))

    def assert_dict(self, source: dict, expected: dict):
        self.assertEqual(len(source.keys()), len(expected.keys()))
        for key in expected.keys():
            self.assertTrue(key in source, f'{key} not found in source')
            if expected[key] is None:
                self.assertIsNone(source[key], f'value {source[key]} for key {key} is not none')
            else:
                self.assertIsInstance(source[key], type(expected[key]))
                self.assertIsNotNone(source[key])
                self.assertEqual(source[key], expected[key])

    def test_1_get_all(self):
        url = f'{self.base_url}/cars'
        resp = requests.get(url)
        resp_json = resp.json()

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp_json), 1)
        self.assertIsInstance(resp_json, list)
        # del resp_json[0]['color']

        for resp_car in resp_json:
            self.assert_dict(source=resp_car, expected=self.car_expected)

    def test_2_get_car(self):
        url = f'{self.base_url}/car/1'
        resp = requests.get(url)
        resp_json = resp.json()

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIsInstance(resp_json, dict)
        self.assert_dict(source=resp_json, expected=self.car_expected)

    def test_2_get_car_not_found(self):
        url = f'{self.base_url}/car/122'
        resp = requests.get(url)
        resp_json = resp.json()

        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
        obj = {
            'detail': 'Car not found',
        }
        self.assertIsInstance(resp_json, dict)
        self.assert_dict(source=resp_json, expected=obj)

    def test_3_post(self):
        url = f'{self.base_url}/car'
        resp = requests.post(url, json=self.car_new)
        resp_json = resp.json()

        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        new_car = self.car_new
        new_car.update({
            'id': self.car_new_id,
            'date_created': self.get_current_date_int(),
            'date_updated': None
        })
        self.assertIsInstance(resp_json, dict)
        self.assert_dict(source=resp_json, expected=new_car)

    def test_3_post_make_missing(self):
        new_car = {
            'model': 'Cayenne',
        }
        url = f'{self.base_url}/car'
        resp = requests.post(url, json=new_car)
        resp_json = resp.json()

        self.assertEqual(resp.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        resp_obj = {
            'detail': [
                {
                    'type': 'missing',
                    'loc': [
                        'body',
                        'make'
                    ],
                    'msg': 'Field required',
                    'input': new_car,
                    'url': 'https://errors.pydantic.dev/2.6/v/missing'
                }
            ]
        }
        self.assertIsInstance(resp_json, dict)
        self.assert_dict(source=resp_json, expected=resp_obj)

    def test_3_post_make_wrong_type(self):
        new_car = {
            'make': 412,
            'model': 'a'
        }
        url = f'{self.base_url}/car'
        resp = requests.post(url, json=new_car)
        resp_json = resp.json()

        self.assertEqual(resp.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        resp_obj = {
            'detail': [
                {
                    'type': 'string_type',
                    'loc': [
                        'body',
                        'make'
                    ],
                    'msg': 'Input should be a valid string',
                    'input': 412,
                    'url': 'https://errors.pydantic.dev/2.6/v/string_type'
                }
            ]
        }
        self.assertIsInstance(resp_json, dict)
        self.assert_dict(source=resp_json, expected=resp_obj)

    def test_3_post_model_missing(self):
        new_car = {
            'make': 'Porsche',
        }
        url = f'{self.base_url}/car'
        resp = requests.post(url, json=new_car)
        resp_json = resp.json()

        self.assertEqual(resp.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        resp_obj = {
            'detail': [
                {
                    'type': 'missing',
                    'loc': [
                        'body',
                        'model'
                    ],
                    'msg': 'Field required',
                    'input': new_car,
                    'url': 'https://errors.pydantic.dev/2.6/v/missing'
                }
            ]
        }
        self.assertIsInstance(resp_json, dict)
        self.assert_dict(source=resp_json, expected=resp_obj)

    def test_3_post_model_wrong_type(self):
        new_car = {
            'make': 'Mercedes',
            'model': 9
        }
        url = f'{self.base_url}/car'
        resp = requests.post(url, json=new_car)
        resp_json = resp.json()

        self.assertEqual(resp.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        resp_obj = {
            'detail': [
                {
                    'type': 'string_type',
                    'loc': [
                        'body',
                        'model'
                    ],
                    'msg': 'Input should be a valid string',
                    'input': 9,
                    'url': 'https://errors.pydantic.dev/2.6/v/string_type'
                }
            ]
        }
        self.assertIsInstance(resp_json, dict)
        self.assert_dict(source=resp_json, expected=resp_obj)

    def test_3_post_color_wrong_type(self):
        new_car = {
            'make': 'Mercedes',
            'model': 'Sprinter',
            'color': 1234
        }
        url = f'{self.base_url}/car'
        resp = requests.post(url, json=new_car)
        resp_json = resp.json()

        self.assertEqual(resp.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        resp_obj = {
            'detail': [
                {
                    'type': 'string_type',
                    'loc': [
                        'body',
                        'color'
                    ],
                    'msg': 'Input should be a valid string',
                    'input': 1234,
                    'url': 'https://errors.pydantic.dev/2.6/v/string_type'
                }
            ]
        }
        self.assertIsInstance(resp_json, dict)
        self.assert_dict(source=resp_json, expected=resp_obj)

    def test_3_post_year_manufactured_wrong_type(self):
        new_car = {
            'make': 'Mercedes',
            'model': 'Sprinter',
            'year_manufactured': 'b'
        }
        url = f'{self.base_url}/car'
        resp = requests.post(url, json=new_car)
        resp_json = resp.json()

        self.assertEqual(resp.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        resp_obj = {
            'detail': [
                {
                    'type': 'int_parsing',
                    'loc': [
                        'body',
                        'year_manufactured'
                    ],
                    'msg': 'Input should be a valid integer, unable to parse string as an integer',
                    'input': 'b',
                    'url': 'https://errors.pydantic.dev/2.6/v/int_parsing'
                }
            ]
        }
        self.assertIsInstance(resp_json, dict)
        self.assert_dict(source=resp_json, expected=resp_obj)

    def test_3_post_year_model_wrong_type(self):
        new_car = {
            'make': 'Mercedes',
            'model': 'Sprinter',
            'year_model': 'c'
        }
        url = f'{self.base_url}/car'
        resp = requests.post(url, json=new_car)
        resp_json = resp.json()

        self.assertEqual(resp.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        resp_obj = {
            'detail': [
                {
                    'type': 'int_parsing',
                    'loc': [
                        'body',
                        'year_model'
                    ],
                    'msg': 'Input should be a valid integer, unable to parse string as an integer',
                    'input': 'c',
                    'url': 'https://errors.pydantic.dev/2.6/v/int_parsing'
                }
            ]
        }
        self.assertIsInstance(resp_json, dict)
        self.assert_dict(source=resp_json, expected=resp_obj)

    def test_3_post_fuel_wrong_type(self):
        new_car = {
            'make': 'Mercedes',
            'model': 'Sprinter',
            'fuel': 4879
        }
        url = f'{self.base_url}/car'
        resp = requests.post(url, json=new_car)
        resp_json = resp.json()

        self.assertEqual(resp.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        resp_obj = {
            'detail': [
                {
                    'type': 'string_type',
                    'loc': [
                        'body',
                        'fuel'
                    ],
                    'msg': 'Input should be a valid string',
                    'input': 4879,
                    'url': 'https://errors.pydantic.dev/2.6/v/string_type'
                }
            ]
        }
        self.assertIsInstance(resp_json, dict)
        self.assert_dict(source=resp_json, expected=resp_obj)

    def test_3_post_horsepower_wrong_type(self):
        new_car = {
            'make': 'Mercedes',
            'model': 'Sprinter',
            'horsepower': 'd'
        }
        url = f'{self.base_url}/car'
        resp = requests.post(url, json=new_car)
        resp_json = resp.json()

        self.assertEqual(resp.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        resp_obj = {
            'detail': [
                {
                    'type': 'int_parsing',
                    'loc': [
                        'body',
                        'horsepower'
                    ],
                    'msg': 'Input should be a valid integer, unable to parse string as an integer',
                    'input': 'd',
                    'url': 'https://errors.pydantic.dev/2.6/v/int_parsing'
                }
            ]
        }
        self.assertIsInstance(resp_json, dict)
        self.assert_dict(source=resp_json, expected=resp_obj)

    def test_3_post_doors_wrong_type(self):
        new_car = {
            'make': 'Mercedes',
            'model': 'Sprinter',
            'doors': 'e'
        }
        url = f'{self.base_url}/car'
        resp = requests.post(url, json=new_car)
        resp_json = resp.json()

        self.assertEqual(resp.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        resp_obj = {
            'detail': [
                {
                    'type': 'int_parsing',
                    'loc': [
                        'body',
                        'doors'
                    ],
                    'msg': 'Input should be a valid integer, unable to parse string as an integer',
                    'input': 'e',
                    'url': 'https://errors.pydantic.dev/2.6/v/int_parsing'
                }
            ]
        }
        self.assertIsInstance(resp_json, dict)
        self.assert_dict(source=resp_json, expected=resp_obj)

    def test_3_post_seats_wrong_type(self):
        new_car = {
            'make': 'Mercedes',
            'model': 'Sprinter',
            'seats': 'f'
        }
        url = f'{self.base_url}/car'
        resp = requests.post(url, json=new_car)
        resp_json = resp.json()

        self.assertEqual(resp.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        resp_obj = {
            'detail': [
                {
                    'type': 'int_parsing',
                    'loc': [
                        'body',
                        'seats'
                    ],
                    'msg': 'Input should be a valid integer, unable to parse string as an integer',
                    'input': 'f',
                    'url': 'https://errors.pydantic.dev/2.6/v/int_parsing'
                }
            ]
        }
        self.assertIsInstance(resp_json, dict)
        self.assert_dict(source=resp_json, expected=resp_obj)

    def test_3_post_fipe_wrong_type(self):
        new_car = {
            'make': 'Mercedes',
            'model': 'Sprinter',
            'fipe': 9876
        }
        url = f'{self.base_url}/car'
        resp = requests.post(url, json=new_car)
        resp_json = resp.json()

        self.assertEqual(resp.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        resp_obj = {
            'detail': [
                {
                    'type': 'string_type',
                    'loc': [
                        'body',
                        'fipe'
                    ],
                    'msg': 'Input should be a valid string',
                    'input': 9876,
                    'url': 'https://errors.pydantic.dev/2.6/v/string_type'
                }
            ]
        }
        self.assertIsInstance(resp_json, dict)
        self.assert_dict(source=resp_json, expected=resp_obj)

    def test_4_put(self):
        url = f'{self.base_url}/car'
        resp = requests.put(url, json=self.car_put)
        resp_json = resp.json()

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        put_car = self.car_put
        put_car.update({
            'color': None,
            'year_manufactured': None,
            'year_model': None,
            'fuel': None,
            'horsepower': None,
            'doors': None,
            'seats': None,
            'fipe': None,
            'date_created': self.get_current_date_int(),
            'date_updated': self.get_current_date_int()
        })
        self.assertIsInstance(resp_json, dict)
        self.assert_dict(source=resp_json, expected=put_car)

    def test_4_put_id_wrong_type(self):
        update_car = {
            'id': 'x',
            'make': 'Ferrari',
            'model': 'Spider',
        }
        url = f'{self.base_url}/car'
        resp = requests.put(url, json=update_car)
        resp_json = resp.json()

        self.assertEqual(resp.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        resp_obj = {
            'detail': [
                {
                    'type': 'int_parsing',
                    'loc': [
                        'body',
                        'id'
                    ],
                    'msg': 'Input should be a valid integer, unable to parse string as an integer',
                    'input': 'x',
                    'url': 'https://errors.pydantic.dev/2.6/v/int_parsing'
                }
            ]
        }
        self.assertIsInstance(resp_json, dict)
        self.assert_dict(source=resp_json, expected=resp_obj)

    def test_4_put_make_missing(self):
        update_car = {
            'id': 2,
            'model': 'Spider',
        }
        url = f'{self.base_url}/car'
        resp = requests.put(url, json=update_car)
        resp_json = resp.json()

        self.assertEqual(resp.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        resp_obj = {
            'detail': [
                {
                    'type': 'missing',
                    'loc': [
                        'body',
                        'make'
                    ],
                    'msg': 'Field required',
                    'input': update_car,
                    'url': 'https://errors.pydantic.dev/2.6/v/missing'
                }
            ]
        }
        self.assertIsInstance(resp_json, dict)
        self.assert_dict(source=resp_json, expected=resp_obj)

    def test_4_put_make_wrong_type(self):
        update_car = {
            'id': 2,
            'make': 412,
            'model': 'a'
        }
        url = f'{self.base_url}/car'
        resp = requests.put(url, json=update_car)
        resp_json = resp.json()

        self.assertEqual(resp.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        resp_obj = {
            'detail': [
                {
                    'type': 'string_type',
                    'loc': [
                        'body',
                        'make'
                    ],
                    'msg': 'Input should be a valid string',
                    'input': 412,
                    'url': 'https://errors.pydantic.dev/2.6/v/string_type'
                }
            ]
        }
        self.assertIsInstance(resp_json, dict)
        self.assert_dict(source=resp_json, expected=resp_obj)

    def test_4_put_model_missing(self):
        update_car = {
            'id': 2,
            'make': 'Spider',
        }
        url = f'{self.base_url}/car'
        resp = requests.put(url, json=update_car)
        resp_json = resp.json()

        self.assertEqual(resp.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        resp_obj = {
            'detail': [
                {
                    'type': 'missing',
                    'loc': [
                        'body',
                        'model'
                    ],
                    'msg': 'Field required',
                    'input': update_car,
                    'url': 'https://errors.pydantic.dev/2.6/v/missing'
                }
            ]
        }
        self.assertIsInstance(resp_json, dict)
        self.assert_dict(source=resp_json, expected=resp_obj)

    def test_4_put_model_wrong_type(self):
        update_car = {
            'id': 2,
            'make': 'Ferrari',
            'model': 9
        }
        url = f'{self.base_url}/car'
        resp = requests.put(url, json=update_car)
        resp_json = resp.json()

        self.assertEqual(resp.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        resp_obj = {
            'detail': [
                {
                    'type': 'string_type',
                    'loc': [
                        'body',
                        'model'
                    ],
                    'msg': 'Input should be a valid string',
                    'input': 9,
                    'url': 'https://errors.pydantic.dev/2.6/v/string_type'
                }
            ]
        }
        self.assertIsInstance(resp_json, dict)
        self.assert_dict(source=resp_json, expected=resp_obj)

    def test_4_put_color_wrong_type(self):
        update_car = {
            'id': 2,
            'make': 'Ferrari',
            'model': 'Spider',
            'color': 1234
        }
        url = f'{self.base_url}/car'
        resp = requests.put(url, json=update_car)
        resp_json = resp.json()

        self.assertEqual(resp.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        resp_obj = {
            'detail': [
                {
                    'type': 'string_type',
                    'loc': [
                        'body',
                        'color'
                    ],
                    'msg': 'Input should be a valid string',
                    'input': 1234,
                    'url': 'https://errors.pydantic.dev/2.6/v/string_type'
                }
            ]
        }
        self.assertIsInstance(resp_json, dict)
        self.assert_dict(source=resp_json, expected=resp_obj)

    def test_4_put_year_manufactured_wrong_type(self):
        update_car = {
            'id': 2,
            'make': 'Ferrari',
            'model': 'Spider',
            'year_manufactured': 'b'
        }
        url = f'{self.base_url}/car'
        resp = requests.put(url, json=update_car)
        resp_json = resp.json()

        self.assertEqual(resp.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        resp_obj = {
            'detail': [
                {
                    'type': 'int_parsing',
                    'loc': [
                        'body',
                        'year_manufactured'
                    ],
                    'msg': 'Input should be a valid integer, unable to parse string as an integer',
                    'input': 'b',
                    'url': 'https://errors.pydantic.dev/2.6/v/int_parsing'
                }
            ]
        }
        self.assertIsInstance(resp_json, dict)
        self.assert_dict(source=resp_json, expected=resp_obj)

    def test_4_put_year_model_wrong_type(self):
        update_car = {
            'id': 2,
            'make': 'Ferrari',
            'model': 'Spider',
            'year_model': 'c'
        }
        url = f'{self.base_url}/car'
        resp = requests.put(url, json=update_car)
        resp_json = resp.json()

        self.assertEqual(resp.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        resp_obj = {
            'detail': [
                {
                    'type': 'int_parsing',
                    'loc': [
                        'body',
                        'year_model'
                    ],
                    'msg': 'Input should be a valid integer, unable to parse string as an integer',
                    'input': 'c',
                    'url': 'https://errors.pydantic.dev/2.6/v/int_parsing'
                }
            ]
        }
        self.assertIsInstance(resp_json, dict)
        self.assert_dict(source=resp_json, expected=resp_obj)

    def test_4_put_fuel_wrong_type(self):
        update_car = {
            'id': 2,
            'make': 'Ferrari',
            'model': 'Spider',
            'fuel': 4879
        }
        url = f'{self.base_url}/car'
        resp = requests.put(url, json=update_car)
        resp_json = resp.json()

        self.assertEqual(resp.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        resp_obj = {
            'detail': [
                {
                    'type': 'string_type',
                    'loc': [
                        'body',
                        'fuel'
                    ],
                    'msg': 'Input should be a valid string',
                    'input': 4879,
                    'url': 'https://errors.pydantic.dev/2.6/v/string_type'
                }
            ]
        }
        self.assertIsInstance(resp_json, dict)
        self.assert_dict(source=resp_json, expected=resp_obj)

    def test_4_put_horsepower_wrong_type(self):
        update_car = {
            'id': 2,
            'make': 'Ferrari',
            'model': 'Spider',
            'horsepower': 'd'
        }
        url = f'{self.base_url}/car'
        resp = requests.put(url, json=update_car)
        resp_json = resp.json()

        self.assertEqual(resp.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        resp_obj = {
            'detail': [
                {
                    'type': 'int_parsing',
                    'loc': [
                        'body',
                        'horsepower'
                    ],
                    'msg': 'Input should be a valid integer, unable to parse string as an integer',
                    'input': 'd',
                    'url': 'https://errors.pydantic.dev/2.6/v/int_parsing'
                }
            ]
        }
        self.assertIsInstance(resp_json, dict)
        self.assert_dict(source=resp_json, expected=resp_obj)

    def test_4_put_doors_wrong_type(self):
        update_car = {
            'id': 2,
            'make': 'Ferrari',
            'model': 'Spider',
            'doors': 'e'
        }
        url = f'{self.base_url}/car'
        resp = requests.put(url, json=update_car)
        resp_json = resp.json()

        self.assertEqual(resp.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        resp_obj = {
            'detail': [
                {
                    'type': 'int_parsing',
                    'loc': [
                        'body',
                        'doors'
                    ],
                    'msg': 'Input should be a valid integer, unable to parse string as an integer',
                    'input': 'e',
                    'url': 'https://errors.pydantic.dev/2.6/v/int_parsing'
                }
            ]
        }
        self.assertIsInstance(resp_json, dict)
        self.assert_dict(source=resp_json, expected=resp_obj)

    def test_4_put_seats_wrong_type(self):
        update_car = {
            'id': 2,
            'make': 'Ferrari',
            'model': 'Spider',
            'seats': 'f'
        }
        url = f'{self.base_url}/car'
        resp = requests.put(url, json=update_car)
        resp_json = resp.json()

        self.assertEqual(resp.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        resp_obj = {
            'detail': [
                {
                    'type': 'int_parsing',
                    'loc': [
                        'body',
                        'seats'
                    ],
                    'msg': 'Input should be a valid integer, unable to parse string as an integer',
                    'input': 'f',
                    'url': 'https://errors.pydantic.dev/2.6/v/int_parsing'
                }
            ]
        }
        self.assertIsInstance(resp_json, dict)
        self.assert_dict(source=resp_json, expected=resp_obj)

    def test_4_put_fipe_wrong_type(self):
        update_car = {
            'id': 2,
            'make': 'Ferrari',
            'model': 'Spider',
            'fipe': 9876
        }
        url = f'{self.base_url}/car'
        resp = requests.put(url, json=update_car)
        resp_json = resp.json()

        self.assertEqual(resp.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        resp_obj = {
            'detail': [
                {
                    'type': 'string_type',
                    'loc': [
                        'body',
                        'fipe'
                    ],
                    'msg': 'Input should be a valid string',
                    'input': 9876,
                    'url': 'https://errors.pydantic.dev/2.6/v/string_type'
                }
            ]
        }
        self.assertIsInstance(resp_json, dict)
        self.assert_dict(source=resp_json, expected=resp_obj)

    def test_5_patch(self):
        update_car = {
            'id': 1,
            'fipe': 'Zombicide'
        }
        url = f'{self.base_url}/car'
        resp = requests.patch(url, json=update_car)
        resp_json = resp.json()

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        new_car = self.car_expected
        new_car.update(update_car)
        new_car.update({
            'date_updated': self.get_current_date_int()
        })
        self.assertIsInstance(resp_json, dict)
        self.assert_dict(source=resp_json, expected=new_car)

    def test_5_patch_id_only(self):
        update_car = {
            'id': 1
        }
        url = f'{self.base_url}/car'
        resp = requests.patch(url, json=update_car)
        resp_json = resp.json()

        self.assertEqual(resp.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.assertIsInstance(resp_json, dict)
        self.assert_dict(source=resp_json, expected={'detail': 'Body must have at least one field other than id'})

    def test_5_patch_id_missing(self):
        url = f'{self.base_url}/car'
        resp = requests.patch(url, json={})
        resp_json = resp.json()

        self.assertEqual(resp.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        resp_obj = {
            'detail': [
                {
                    'type': 'missing',
                    'loc': [
                        'body',
                        'id'
                    ],
                    'msg': 'Field required',
                    'input': {},
                    'url': 'https://errors.pydantic.dev/2.6/v/missing'
                }
            ]
        }
        self.assertIsInstance(resp_json, dict)
        self.assert_dict(source=resp_json, expected=resp_obj)

    def test_5_patch_id_wrong_type(self):
        update_car = {
            'id': 'x',
        }
        url = f'{self.base_url}/car'
        resp = requests.patch(url, json=update_car)
        resp_json = resp.json()

        self.assertEqual(resp.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        resp_obj = {
            'detail': [
                {
                    'type': 'int_parsing',
                    'loc': [
                        'body',
                        'id'
                    ],
                    'msg': 'Input should be a valid integer, unable to parse string as an integer',
                    'input': 'x',
                    'url': 'https://errors.pydantic.dev/2.6/v/int_parsing'
                }
            ]
        }
        self.assertIsInstance(resp_json, dict)
        self.assert_dict(source=resp_json, expected=resp_obj)

    def test_5_patch_make_wrong_type(self):
        update_car = {
            'id': 2,
            'make': 412,
        }
        url = f'{self.base_url}/car'
        resp = requests.patch(url, json=update_car)
        resp_json = resp.json()

        self.assertEqual(resp.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        resp_obj = {
            'detail': [
                {
                    'type': 'string_type',
                    'loc': [
                        'body',
                        'make'
                    ],
                    'msg': 'Input should be a valid string',
                    'input': 412,
                    'url': 'https://errors.pydantic.dev/2.6/v/string_type'
                }
            ]
        }
        self.assertIsInstance(resp_json, dict)
        self.assert_dict(source=resp_json, expected=resp_obj)

    def test_5_patch_model_wrong_type(self):
        update_car = {
            'id': 2,
            'model': 9
        }
        url = f'{self.base_url}/car'
        resp = requests.patch(url, json=update_car)
        resp_json = resp.json()

        self.assertEqual(resp.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        resp_obj = {
            'detail': [
                {
                    'type': 'string_type',
                    'loc': [
                        'body',
                        'model'
                    ],
                    'msg': 'Input should be a valid string',
                    'input': 9,
                    'url': 'https://errors.pydantic.dev/2.6/v/string_type'
                }
            ]
        }
        self.assertIsInstance(resp_json, dict)
        self.assert_dict(source=resp_json, expected=resp_obj)

    def test_5_patch_color_wrong_type(self):
        update_car = {
            'id': 2,
            'color': 1234
        }
        url = f'{self.base_url}/car'
        resp = requests.patch(url, json=update_car)
        resp_json = resp.json()

        self.assertEqual(resp.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        resp_obj = {
            'detail': [
                {
                    'type': 'string_type',
                    'loc': [
                        'body',
                        'color'
                    ],
                    'msg': 'Input should be a valid string',
                    'input': 1234,
                    'url': 'https://errors.pydantic.dev/2.6/v/string_type'
                }
            ]
        }
        self.assertIsInstance(resp_json, dict)
        self.assert_dict(source=resp_json, expected=resp_obj)

    def test_5_patch_year_manufactured_wrong_type(self):
        update_car = {
            'id': 2,
            'year_manufactured': 'b'
        }
        url = f'{self.base_url}/car'
        resp = requests.patch(url, json=update_car)
        resp_json = resp.json()

        self.assertEqual(resp.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        resp_obj = {
            'detail': [
                {
                    'type': 'int_parsing',
                    'loc': [
                        'body',
                        'year_manufactured'
                    ],
                    'msg': 'Input should be a valid integer, unable to parse string as an integer',
                    'input': 'b',
                    'url': 'https://errors.pydantic.dev/2.6/v/int_parsing'
                }
            ]
        }
        self.assertIsInstance(resp_json, dict)
        self.assert_dict(source=resp_json, expected=resp_obj)

    def test_5_patch_year_model_wrong_type(self):
        update_car = {
            'id': 2,
            'year_model': 'c'
        }
        url = f'{self.base_url}/car'
        resp = requests.patch(url, json=update_car)
        resp_json = resp.json()

        self.assertEqual(resp.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        resp_obj = {
            'detail': [
                {
                    'type': 'int_parsing',
                    'loc': [
                        'body',
                        'year_model'
                    ],
                    'msg': 'Input should be a valid integer, unable to parse string as an integer',
                    'input': 'c',
                    'url': 'https://errors.pydantic.dev/2.6/v/int_parsing'
                }
            ]
        }
        self.assertIsInstance(resp_json, dict)
        self.assert_dict(source=resp_json, expected=resp_obj)

    def test_5_patch_fuel_wrong_type(self):
        update_car = {
            'id': 2,
            'fuel': 4879
        }
        url = f'{self.base_url}/car'
        resp = requests.patch(url, json=update_car)
        resp_json = resp.json()

        self.assertEqual(resp.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        resp_obj = {
            'detail': [
                {
                    'type': 'string_type',
                    'loc': [
                        'body',
                        'fuel'
                    ],
                    'msg': 'Input should be a valid string',
                    'input': 4879,
                    'url': 'https://errors.pydantic.dev/2.6/v/string_type'
                }
            ]
        }
        self.assertIsInstance(resp_json, dict)
        self.assert_dict(source=resp_json, expected=resp_obj)

    def test_5_patch_horsepower_wrong_type(self):
        update_car = {
            'id': 2,
            'horsepower': 'd'
        }
        url = f'{self.base_url}/car'
        resp = requests.patch(url, json=update_car)
        resp_json = resp.json()

        self.assertEqual(resp.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        resp_obj = {
            'detail': [
                {
                    'type': 'int_parsing',
                    'loc': [
                        'body',
                        'horsepower'
                    ],
                    'msg': 'Input should be a valid integer, unable to parse string as an integer',
                    'input': 'd',
                    'url': 'https://errors.pydantic.dev/2.6/v/int_parsing'
                }
            ]
        }
        self.assertIsInstance(resp_json, dict)
        self.assert_dict(source=resp_json, expected=resp_obj)

    def test_5_patch_doors_wrong_type(self):
        update_car = {
            'id': 2,
            'doors': 'e'
        }
        url = f'{self.base_url}/car'
        resp = requests.patch(url, json=update_car)
        resp_json = resp.json()

        self.assertEqual(resp.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        resp_obj = {
            'detail': [
                {
                    'type': 'int_parsing',
                    'loc': [
                        'body',
                        'doors'
                    ],
                    'msg': 'Input should be a valid integer, unable to parse string as an integer',
                    'input': 'e',
                    'url': 'https://errors.pydantic.dev/2.6/v/int_parsing'
                }
            ]
        }
        self.assertIsInstance(resp_json, dict)
        self.assert_dict(source=resp_json, expected=resp_obj)

    def test_5_patch_seats_wrong_type(self):
        update_car = {
            'id': 2,
            'seats': 'f'
        }
        url = f'{self.base_url}/car'
        resp = requests.patch(url, json=update_car)
        resp_json = resp.json()

        self.assertEqual(resp.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        resp_obj = {
            'detail': [
                {
                    'type': 'int_parsing',
                    'loc': [
                        'body',
                        'seats'
                    ],
                    'msg': 'Input should be a valid integer, unable to parse string as an integer',
                    'input': 'f',
                    'url': 'https://errors.pydantic.dev/2.6/v/int_parsing'
                }
            ]
        }
        self.assertIsInstance(resp_json, dict)
        self.assert_dict(source=resp_json, expected=resp_obj)

    def test_5_patch_fipe_wrong_type(self):
        update_car = {
            'id': 2,
            'fipe': 9876
        }
        url = f'{self.base_url}/car'
        resp = requests.patch(url, json=update_car)
        resp_json = resp.json()

        self.assertEqual(resp.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        resp_obj = {
            'detail': [
                {
                    'type': 'string_type',
                    'loc': [
                        'body',
                        'fipe'
                    ],
                    'msg': 'Input should be a valid string',
                    'input': 9876,
                    'url': 'https://errors.pydantic.dev/2.6/v/string_type'
                }
            ]
        }
        self.assertIsInstance(resp_json, dict)
        self.assert_dict(source=resp_json, expected=resp_obj)

    def test_6_delete_car(self):
        url = f'{self.base_url}/car/2'
        resp = requests.delete(url)
        resp_json = resp.json()

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIsInstance(resp_json, dict)
        self.assert_dict(source=resp_json, expected={'detail': 'Car deleted'})

    def test_6_delete_car_not_found(self):
        url = f'{self.base_url}/car/2345'
        resp = requests.delete(url)
        resp_json = resp.json()

        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIsInstance(resp_json, dict)
        self.assert_dict(source=resp_json, expected={'detail': 'Car not found'})


if __name__ == '__main__':
    # unittest.main(failfast=True, exit=True)
    unittest.main()
