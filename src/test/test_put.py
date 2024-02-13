from pathlib import Path
import os
import sys
sys.path.append(os.path.join(Path(__file__).parent.parent.parent))
from fastapi import status
from src.gen.generic import Generic, Detail, ReturnMessage
import requests
import unittest


class TestPut(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.base_url = Generic.get_base_url()

    def setUp(self) -> None:
        pass

    def test_put(self):
        url = f'{self.base_url}/car'
        resp = requests.put(url, json=Generic.car_put())
        resp_json = resp.json()

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        put_car = Generic.car_put()
        for key in Generic.car_post_expected().keys():
            if key not in put_car:
                put_car[key] = None
        put_car.update({
            'date_created': Generic.get_current_date(),
            'date_updated': Generic.get_current_date()
        })
        self.assertIsInstance(resp_json, dict)
        Generic.assert_dict(source=resp_json, expected=put_car)

    def test_put_car_not_found(self):
        url = f'{self.base_url}/car'
        put_car = Generic.car_put()
        put_car.update({'id': 1234})
        resp = requests.put(url, json=put_car)
        resp_json = resp.json()

        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIsInstance(resp_json, dict)
        Generic.assert_dict(source=resp_json, expected={'detail': ReturnMessage.CAR_NOT_FOUND.value})

    def test_put_id_wrong_type(self):
        update_car = {
            'id': 'x',
            'make': 'Ferrari',
            'model': 'Spider',
        }
        url = f'{self.base_url}/car'
        resp = requests.put(url, json=update_car)
        resp_json = resp.json()

        self.assertEqual(resp.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        resp_obj = Generic.get_detail_info(type_field=Detail.INT_PARSING,
                                           field='id',
                                           msg=Detail.INPUT_VALID_INTEGER,
                                           input_data='x')
        self.assertIsInstance(resp_json, dict)
        Generic.assert_dict(source=resp_json, expected=resp_obj)

    def test_put_make_model_equal(self):
        url = f'{self.base_url}/car'
        car_post = Generic.car_put()
        resp = requests.put(url, json=car_post)
        resp_json = resp.json()

        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIsInstance(resp_json, dict)
        Generic.assert_dict(source=resp_json, expected={'detail': ReturnMessage.CAR_EXIST.value})

    def test_put_make_equal(self):
        url = f'{self.base_url}/car'
        car_post = Generic.car_put()
        car_post.update({'model': 'brum'})
        resp = requests.put(url, json=car_post)
        resp_json = resp.json()

        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIsInstance(resp_json, dict)
        Generic.assert_dict(source=resp_json, expected={'detail': ReturnMessage.CAR_EXIST.value})

    def test_put_make_missing(self):
        update_car = {
            'id': 1,
            'model': 'Spider',
        }
        url = f'{self.base_url}/car'
        resp = requests.put(url, json=update_car)
        resp_json = resp.json()

        self.assertEqual(resp.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        resp_obj = Generic.get_detail_info(type_field=Detail.MISSING,
                                           field='make',
                                           msg=Detail.FIELD_REQUIRED,
                                           input_data=update_car)
        self.assertIsInstance(resp_json, dict)
        Generic.assert_dict(source=resp_json, expected=resp_obj)

    def test_put_make_wrong_type(self):
        update_car = {
            'id': 2,
            'make': 412,
            'model': 'a'
        }
        url = f'{self.base_url}/car'
        resp = requests.put(url, json=update_car)
        resp_json = resp.json()

        self.assertEqual(resp.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        resp_obj = Generic.get_detail_info(type_field=Detail.STRING_TYPE,
                                           field='make',
                                           msg=Detail.INPUT_VALID_STRING,
                                           input_data=412)
        self.assertIsInstance(resp_json, dict)
        Generic.assert_dict(source=resp_json, expected=resp_obj)

    def test_put_model_equal(self):
        url = f'{self.base_url}/car'
        car_post = Generic.car_put()
        car_post.update({'make': 'brum'})
        resp = requests.put(url, json=car_post)
        resp_json = resp.json()

        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIsInstance(resp_json, dict)
        Generic.assert_dict(source=resp_json, expected={'detail': ReturnMessage.CAR_EXIST.value})

    def test_put_model_missing(self):
        update_car = {
            'id': 2,
            'make': 'Spider',
        }
        url = f'{self.base_url}/car'
        resp = requests.put(url, json=update_car)
        resp_json = resp.json()

        self.assertEqual(resp.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        resp_obj = Generic.get_detail_info(type_field=Detail.MISSING,
                                           field='model',
                                           msg=Detail.FIELD_REQUIRED,
                                           input_data=update_car)
        self.assertIsInstance(resp_json, dict)
        Generic.assert_dict(source=resp_json, expected=resp_obj)

    def test_put_model_wrong_type(self):
        update_car = {
            'id': 2,
            'make': 'Ferrari',
            'model': 9
        }
        url = f'{self.base_url}/car'
        resp = requests.put(url, json=update_car)
        resp_json = resp.json()

        self.assertEqual(resp.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        resp_obj = Generic.get_detail_info(type_field=Detail.STRING_TYPE,
                                           field='model',
                                           msg=Detail.INPUT_VALID_STRING,
                                           input_data=9)
        self.assertIsInstance(resp_json, dict)
        Generic.assert_dict(source=resp_json, expected=resp_obj)

    def test_put_color_wrong_type(self):
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
        resp_obj = Generic.get_detail_info(type_field=Detail.STRING_TYPE,
                                           field='color',
                                           msg=Detail.INPUT_VALID_STRING,
                                           input_data=1234)
        self.assertIsInstance(resp_json, dict)
        Generic.assert_dict(source=resp_json, expected=resp_obj)

    def test_put_year_manufactured_wrong_type(self):
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
        resp_obj = Generic.get_detail_info(type_field=Detail.INT_PARSING,
                                           field='year_manufactured',
                                           msg=Detail.INPUT_VALID_INTEGER,
                                           input_data='b')
        self.assertIsInstance(resp_json, dict)
        Generic.assert_dict(source=resp_json, expected=resp_obj)

    def test_put_year_model_wrong_type(self):
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
        resp_obj = Generic.get_detail_info(type_field=Detail.INT_PARSING,
                                           field='year_model',
                                           msg=Detail.INPUT_VALID_INTEGER,
                                           input_data='c')
        self.assertIsInstance(resp_json, dict)
        Generic.assert_dict(source=resp_json, expected=resp_obj)

    def test_put_fuel_wrong_type(self):
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
        resp_obj = Generic.get_detail_info(type_field=Detail.STRING_TYPE,
                                           field='fuel',
                                           msg=Detail.INPUT_VALID_STRING,
                                           input_data=4879)
        self.assertIsInstance(resp_json, dict)
        Generic.assert_dict(source=resp_json, expected=resp_obj)

    def test_put_horsepower_wrong_type(self):
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
        resp_obj = Generic.get_detail_info(type_field=Detail.INT_PARSING,
                                           field='horsepower',
                                           msg=Detail.INPUT_VALID_INTEGER,
                                           input_data='d')
        self.assertIsInstance(resp_json, dict)
        Generic.assert_dict(source=resp_json, expected=resp_obj)

    def test_put_doors_wrong_type(self):
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
        resp_obj = Generic.get_detail_info(type_field=Detail.INT_PARSING,
                                           field='doors',
                                           msg=Detail.INPUT_VALID_INTEGER,
                                           input_data='e')
        self.assertIsInstance(resp_json, dict)
        Generic.assert_dict(source=resp_json, expected=resp_obj)

    def test_put_seats_wrong_type(self):
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
        resp_obj = Generic.get_detail_info(type_field=Detail.INT_PARSING,
                                           field='seats',
                                           msg=Detail.INPUT_VALID_INTEGER,
                                           input_data='f')
        self.assertIsInstance(resp_json, dict)
        Generic.assert_dict(source=resp_json, expected=resp_obj)

    def test_put_fipe_wrong_type(self):
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
        resp_obj = Generic.get_detail_info(type_field=Detail.STRING_TYPE,
                                           field='fipe',
                                           msg=Detail.INPUT_VALID_STRING,
                                           input_data=9876)
        self.assertIsInstance(resp_json, dict)
        Generic.assert_dict(source=resp_json, expected=resp_obj)
