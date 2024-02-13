from pathlib import Path
import os
import sys
sys.path.append(os.path.join(Path(__file__).parent.parent.parent))
from fastapi import status
from src.gen.generic import Generic, Detail, ReturnMessage
import requests
import unittest


class TestPost(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.base_url = Generic.get_base_url()

    def setUp(self) -> None:
        pass

    def test_post(self):
        url = f'{self.base_url}/car'
        car_post = Generic.car_post()
        car_post['color'] = car_post['color'] + '    '
        resp = requests.post(url, json=car_post)
        resp_json = resp.json()

        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        car_post = Generic.car_post_expected()
        self.assertIsInstance(resp_json, dict)
        Generic.assert_dict(source=resp_json, expected=car_post)

    def test_post_make_model_equal(self):
        url = f'{self.base_url}/car'
        car_post = Generic.car_post()
        resp = requests.post(url, json=car_post)
        resp_json = resp.json()

        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIsInstance(resp_json, dict)
        Generic.assert_dict(source=resp_json, expected={'detail': ReturnMessage.CAR_EXIST.value})

    def test_post_make_equal(self):
        url = f'{self.base_url}/car'
        car_post = Generic.car_post()
        car_post.update({'model': 'brum'})
        resp = requests.post(url, json=car_post)
        resp_json = resp.json()

        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIsInstance(resp_json, dict)
        Generic.assert_dict(source=resp_json, expected={'detail': ReturnMessage.CAR_EXIST.value})

    def test_post_make_missing(self):
        new_car = {
            'model': 'Cayenne',
        }
        url = f'{self.base_url}/car'
        resp = requests.post(url, json=new_car)
        resp_json = resp.json()

        self.assertEqual(resp.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        resp_obj = Generic.get_detail_info(type_field=Detail.MISSING,
                                           field='make',
                                           msg=Detail.FIELD_REQUIRED,
                                           input_data=new_car)
        self.assertIsInstance(resp_json, dict)
        Generic.assert_dict(source=resp_json, expected=resp_obj)

    def test_post_make_wrong_type(self):
        new_car = {
            'make': 412,
            'model': 'a'
        }
        url = f'{self.base_url}/car'
        resp = requests.post(url, json=new_car)
        resp_json = resp.json()

        self.assertEqual(resp.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        resp_obj = Generic.get_detail_info(type_field=Detail.STRING_TYPE,
                                           field='make',
                                           msg=Detail.INPUT_VALID_STRING,
                                           input_data=412)
        self.assertIsInstance(resp_json, dict)
        Generic.assert_dict(source=resp_json, expected=resp_obj)

    def test_post_make_empty(self):
        new_car = {
            'make': '',
            'model': 'a'
        }
        url = f'{self.base_url}/car'
        resp = requests.post(url, json=new_car)
        resp_json = resp.json()

        self.assertEqual(resp.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        resp_obj = Generic.get_detail_info(type_field=Detail.STRING_TOO_SHORT,
                                           field='make',
                                           msg=Detail.INPUT_VALID_STRING_MIN_LENGTH,
                                           input_data='',
                                           min_length=1)
        self.assertIsInstance(resp_json, dict)
        Generic.assert_dict(source=resp_json, expected=resp_obj)

    def test_post_make_spaces(self):
        new_car = {
            'make': '   ',
            'model': 'a'
        }
        url = f'{self.base_url}/car'
        resp = requests.post(url, json=new_car)
        resp_json = resp.json()

        self.assertEqual(resp.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        resp_obj = Generic.get_detail_info(type_field=Detail.STRING_TOO_SHORT,
                                           field='make',
                                           msg=Detail.INPUT_VALID_STRING_MIN_LENGTH,
                                           input_data='   ',
                                           min_length=1)
        self.assertIsInstance(resp_json, dict)
        Generic.assert_dict(source=resp_json, expected=resp_obj)

    def test_post_model_equal(self):
        url = f'{self.base_url}/car'
        car_post = Generic.car_post()
        car_post.update({'make': 'brum'})
        resp = requests.post(url, json=car_post)
        resp_json = resp.json()

        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIsInstance(resp_json, dict)
        Generic.assert_dict(source=resp_json, expected={'detail': ReturnMessage.CAR_EXIST.value})

    def test_post_model_missing(self):
        new_car = {
            'make': 'Porsche',
        }
        url = f'{self.base_url}/car'
        resp = requests.post(url, json=new_car)
        resp_json = resp.json()

        self.assertEqual(resp.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        resp_obj = Generic.get_detail_info(type_field=Detail.MISSING,
                                           field='model',
                                           msg=Detail.FIELD_REQUIRED,
                                           input_data=new_car)
        self.assertIsInstance(resp_json, dict)
        Generic.assert_dict(source=resp_json, expected=resp_obj)

    def test_post_model_wrong_type(self):
        new_car = {
            'make': 'Mercedes',
            'model': 9
        }
        url = f'{self.base_url}/car'
        resp = requests.post(url, json=new_car)
        resp_json = resp.json()

        self.assertEqual(resp.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        resp_obj = Generic.get_detail_info(type_field=Detail.STRING_TYPE,
                                           field='model',
                                           msg=Detail.INPUT_VALID_STRING,
                                           input_data=9)
        self.assertIsInstance(resp_json, dict)
        Generic.assert_dict(source=resp_json, expected=resp_obj)

    def test_post_model_empty(self):
        new_car = {
            'make': 'a',
            'model': ''
        }
        url = f'{self.base_url}/car'
        resp = requests.post(url, json=new_car)
        resp_json = resp.json()

        self.assertEqual(resp.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        resp_obj = Generic.get_detail_info(type_field=Detail.STRING_TOO_SHORT,
                                           field='model',
                                           msg=Detail.INPUT_VALID_STRING_MIN_LENGTH,
                                           input_data='',
                                           min_length=1)
        self.assertIsInstance(resp_json, dict)
        Generic.assert_dict(source=resp_json, expected=resp_obj)

    def test_post_model_spaces(self):
        new_car = {
            'make': 'a',
            'model': ' '
        }
        url = f'{self.base_url}/car'
        resp = requests.post(url, json=new_car)
        resp_json = resp.json()

        self.assertEqual(resp.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        resp_obj = Generic.get_detail_info(type_field=Detail.STRING_TOO_SHORT,
                                           field='model',
                                           msg=Detail.INPUT_VALID_STRING_MIN_LENGTH,
                                           input_data=' ',
                                           min_length=1)
        self.assertIsInstance(resp_json, dict)
        Generic.assert_dict(source=resp_json, expected=resp_obj)

    def test_post_color_wrong_type(self):
        new_car = {
            'make': 'Mercedes',
            'model': 'Sprinter',
            'color': 1234
        }
        url = f'{self.base_url}/car'
        resp = requests.post(url, json=new_car)
        resp_json = resp.json()

        self.assertEqual(resp.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        resp_obj = Generic.get_detail_info(type_field=Detail.STRING_TYPE,
                                           field='color',
                                           msg=Detail.INPUT_VALID_STRING,
                                           input_data=1234)
        self.assertIsInstance(resp_json, dict)
        Generic.assert_dict(source=resp_json, expected=resp_obj)

    def test_post_color_empty(self):
        new_car = {
            'make': 'b',
            'model': 'a',
            'color': ''
        }
        url = f'{self.base_url}/car'
        resp = requests.post(url, json=new_car)
        resp_json = resp.json()

        self.assertEqual(resp.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        resp_obj = Generic.get_detail_info(type_field=Detail.STRING_TOO_SHORT,
                                           field='color',
                                           msg=Detail.INPUT_VALID_STRING_MIN_LENGTH,
                                           input_data='',
                                           min_length=1)
        self.assertIsInstance(resp_json, dict)
        Generic.assert_dict(source=resp_json, expected=resp_obj)

    def test_post_color_spaces(self):
        new_car = {
            'make': 'b',
            'model': 'a',
            'color': '     '
        }
        url = f'{self.base_url}/car'
        resp = requests.post(url, json=new_car)
        resp_json = resp.json()

        self.assertEqual(resp.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        resp_obj = Generic.get_detail_info(type_field=Detail.STRING_TOO_SHORT,
                                           field='color',
                                           msg=Detail.INPUT_VALID_STRING_MIN_LENGTH,
                                           input_data='     ',
                                           min_length=1)
        self.assertIsInstance(resp_json, dict)
        Generic.assert_dict(source=resp_json, expected=resp_obj)

    def test_post_year_manufactured_wrong_type(self):
        new_car = {
            'make': 'Mercedes',
            'model': 'Sprinter',
            'year_manufactured': 'b'
        }
        url = f'{self.base_url}/car'
        resp = requests.post(url, json=new_car)
        resp_json = resp.json()

        self.assertEqual(resp.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        resp_obj = Generic.get_detail_info(type_field=Detail.INT_PARSING,
                                           field='year_manufactured',
                                           msg=Detail.INPUT_VALID_INTEGER,
                                           input_data='b')
        self.assertIsInstance(resp_json, dict)
        Generic.assert_dict(source=resp_json, expected=resp_obj)

    def test_post_year_manufactured_zero(self):
        new_car = {
            'make': 'b',
            'model': 'a',
            'year_manufactured': 0
        }
        url = f'{self.base_url}/car'
        resp = requests.post(url, json=new_car)
        resp_json = resp.json()

        self.assertEqual(resp.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        resp_obj = Generic.get_detail_info(type_field=Detail.GREATER_THAN,
                                           field='year_manufactured',
                                           msg=Detail.INPUT_VALID_INTEGER_GREATER_THAN,
                                           input_data=0,
                                           gt=0)
        self.assertIsInstance(resp_json, dict)
        Generic.assert_dict(source=resp_json, expected=resp_obj)

    def test_post_year_model_wrong_type(self):
        new_car = {
            'make': 'Mercedes',
            'model': 'Sprinter',
            'year_model': 'c'
        }
        url = f'{self.base_url}/car'
        resp = requests.post(url, json=new_car)
        resp_json = resp.json()

        self.assertEqual(resp.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        resp_obj = Generic.get_detail_info(type_field=Detail.INT_PARSING,
                                           field='year_model',
                                           msg=Detail.INPUT_VALID_INTEGER,
                                           input_data='c')
        self.assertIsInstance(resp_json, dict)
        Generic.assert_dict(source=resp_json, expected=resp_obj)

    def test_post_year_model_zero(self):
        new_car = {
            'make': 'b',
            'model': 'a',
            'year_model': 0
        }
        url = f'{self.base_url}/car'
        resp = requests.post(url, json=new_car)
        resp_json = resp.json()

        self.assertEqual(resp.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        resp_obj = Generic.get_detail_info(type_field=Detail.GREATER_THAN,
                                           field='year_model',
                                           msg=Detail.INPUT_VALID_INTEGER_GREATER_THAN,
                                           input_data=0,
                                           gt=0)
        self.assertIsInstance(resp_json, dict)
        Generic.assert_dict(source=resp_json, expected=resp_obj)

    def test_post_fuel_wrong_type(self):
        new_car = {
            'make': 'Mercedes',
            'model': 'Sprinter',
            'fuel': 4879
        }
        url = f'{self.base_url}/car'
        resp = requests.post(url, json=new_car)
        resp_json = resp.json()

        self.assertEqual(resp.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        resp_obj = Generic.get_detail_info(type_field=Detail.STRING_TYPE,
                                           field='fuel',
                                           msg=Detail.INPUT_VALID_STRING,
                                           input_data=4879)
        self.assertIsInstance(resp_json, dict)
        Generic.assert_dict(source=resp_json, expected=resp_obj)

    def test_post_fuel_empty(self):
        new_car = {
            'make': 'b',
            'model': 'a',
            'fuel': ''
        }
        url = f'{self.base_url}/car'
        resp = requests.post(url, json=new_car)
        resp_json = resp.json()

        self.assertEqual(resp.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        resp_obj = Generic.get_detail_info(type_field=Detail.STRING_TOO_SHORT,
                                           field='fuel',
                                           msg=Detail.INPUT_VALID_STRING_MIN_LENGTH,
                                           input_data='',
                                           min_length=1)
        self.assertIsInstance(resp_json, dict)
        Generic.assert_dict(source=resp_json, expected=resp_obj)

    def test_post_fuel_spaces(self):
        new_car = {
            'make': 'b',
            'model': 'a',
            'fuel': ' '
        }
        url = f'{self.base_url}/car'
        resp = requests.post(url, json=new_car)
        resp_json = resp.json()

        self.assertEqual(resp.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        resp_obj = Generic.get_detail_info(type_field=Detail.STRING_TOO_SHORT,
                                           field='fuel',
                                           msg=Detail.INPUT_VALID_STRING_MIN_LENGTH,
                                           input_data=' ',
                                           min_length=1)
        self.assertIsInstance(resp_json, dict)
        Generic.assert_dict(source=resp_json, expected=resp_obj)

    def test_post_horsepower_wrong_type(self):
        new_car = {
            'make': 'Mercedes',
            'model': 'Sprinter',
            'horsepower': 'd'
        }
        url = f'{self.base_url}/car'
        resp = requests.post(url, json=new_car)
        resp_json = resp.json()

        self.assertEqual(resp.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        resp_obj = Generic.get_detail_info(type_field=Detail.INT_PARSING,
                                           field='horsepower',
                                           msg=Detail.INPUT_VALID_INTEGER,
                                           input_data='d')
        self.assertIsInstance(resp_json, dict)
        Generic.assert_dict(source=resp_json, expected=resp_obj)

    def test_post_horsepower_zero(self):
        new_car = {
            'make': 'b',
            'model': 'a',
            'horsepower': 0
        }
        url = f'{self.base_url}/car'
        resp = requests.post(url, json=new_car)
        resp_json = resp.json()

        self.assertEqual(resp.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        resp_obj = Generic.get_detail_info(type_field=Detail.GREATER_THAN,
                                           field='horsepower',
                                           msg=Detail.INPUT_VALID_INTEGER_GREATER_THAN,
                                           input_data=0,
                                           gt=0)
        self.assertIsInstance(resp_json, dict)
        Generic.assert_dict(source=resp_json, expected=resp_obj)

    def test_post_doors_wrong_type(self):
        new_car = {
            'make': 'Mercedes',
            'model': 'Sprinter',
            'doors': 'e'
        }
        url = f'{self.base_url}/car'
        resp = requests.post(url, json=new_car)
        resp_json = resp.json()

        self.assertEqual(resp.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        resp_obj = Generic.get_detail_info(type_field=Detail.INT_PARSING,
                                           field='doors',
                                           msg=Detail.INPUT_VALID_INTEGER,
                                           input_data='e')
        self.assertIsInstance(resp_json, dict)
        Generic.assert_dict(source=resp_json, expected=resp_obj)

    def test_post_doors_zero(self):
        new_car = {
            'make': 'b',
            'model': 'a',
            'doors': 0
        }
        url = f'{self.base_url}/car'
        resp = requests.post(url, json=new_car)
        resp_json = resp.json()

        self.assertEqual(resp.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        resp_obj = Generic.get_detail_info(type_field=Detail.GREATER_THAN,
                                           field='doors',
                                           msg=Detail.INPUT_VALID_INTEGER_GREATER_THAN,
                                           input_data=0,
                                           gt=0)
        self.assertIsInstance(resp_json, dict)
        Generic.assert_dict(source=resp_json, expected=resp_obj)

    def test_post_seats_wrong_type(self):
        new_car = {
            'make': 'Mercedes',
            'model': 'Sprinter',
            'seats': 'f'
        }
        url = f'{self.base_url}/car'
        resp = requests.post(url, json=new_car)
        resp_json = resp.json()

        self.assertEqual(resp.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        resp_obj = Generic.get_detail_info(type_field=Detail.INT_PARSING,
                                           field='seats',
                                           msg=Detail.INPUT_VALID_INTEGER,
                                           input_data='f')
        self.assertIsInstance(resp_json, dict)
        Generic.assert_dict(source=resp_json, expected=resp_obj)

    def test_post_seats_zero(self):
        new_car = {
            'make': 'b',
            'model': 'a',
            'seats': 0
        }
        url = f'{self.base_url}/car'
        resp = requests.post(url, json=new_car)
        resp_json = resp.json()

        self.assertEqual(resp.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        resp_obj = Generic.get_detail_info(type_field=Detail.GREATER_THAN,
                                           field='seats',
                                           msg=Detail.INPUT_VALID_INTEGER_GREATER_THAN,
                                           input_data=0,
                                           gt=0)
        self.assertIsInstance(resp_json, dict)
        Generic.assert_dict(source=resp_json, expected=resp_obj)

    def test_post_fipe_wrong_type(self):
        new_car = {
            'make': 'Mercedes',
            'model': 'Sprinter',
            'fipe': 9876
        }
        url = f'{self.base_url}/car'
        resp = requests.post(url, json=new_car)
        resp_json = resp.json()

        self.assertEqual(resp.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        resp_obj = Generic.get_detail_info(type_field=Detail.STRING_TYPE,
                                           field='fipe',
                                           msg=Detail.INPUT_VALID_STRING,
                                           input_data=9876)
        self.assertIsInstance(resp_json, dict)
        Generic.assert_dict(source=resp_json, expected=resp_obj)

    def test_post_fipe_empty(self):
        new_car = {
            'make': 'b',
            'model': 'a',
            'fipe': ''
        }
        url = f'{self.base_url}/car'
        resp = requests.post(url, json=new_car)
        resp_json = resp.json()

        self.assertEqual(resp.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        resp_obj = Generic.get_detail_info(type_field=Detail.STRING_TOO_SHORT,
                                           field='fipe',
                                           msg=Detail.INPUT_VALID_STRING_MIN_LENGTH,
                                           input_data='',
                                           min_length=1)
        self.assertIsInstance(resp_json, dict)
        Generic.assert_dict(source=resp_json, expected=resp_obj)

    def test_post_fipe_spaces(self):
        new_car = {
            'make': 'b',
            'model': 'a',
            'fipe': '  '
        }
        url = f'{self.base_url}/car'
        resp = requests.post(url, json=new_car)
        resp_json = resp.json()

        self.assertEqual(resp.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        resp_obj = Generic.get_detail_info(type_field=Detail.STRING_TOO_SHORT,
                                           field='fipe',
                                           msg=Detail.INPUT_VALID_STRING_MIN_LENGTH,
                                           input_data='  ',
                                           min_length=1)
        self.assertIsInstance(resp_json, dict)
        Generic.assert_dict(source=resp_json, expected=resp_obj)
