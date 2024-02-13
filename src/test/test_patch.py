from pathlib import Path
import os
import sys
sys.path.append(os.path.join(Path(__file__).parent.parent.parent))
from fastapi import status
from src.gen.generic import Generic, Detail, ReturnMessage
import requests
import unittest


class TestPatch(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.base_url = Generic.get_base_url()

    def setUp(self) -> None:
        pass

    def test_patch(self):
        url = f'{self.base_url}/car'
        update_car = Generic.car_patch()
        update_car['fipe'] = update_car['fipe'] + '         '
        resp = requests.patch(url, json=update_car)
        resp_json = resp.json()

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        updated_car = Generic.car_put()
        for key in Generic.car_post_expected().keys():
            if key not in updated_car:
                updated_car[key] = None
        updated_car.update({
            'date_created': Generic.get_current_date(),
            'date_updated': Generic.get_current_date()
        })
        update_car = {
            # clear values with spaces
            key: value.strip() if isinstance(value, str) else value for key, value in update_car.items()
        }
        updated_car.update(update_car)
        self.assertIsInstance(resp_json, dict)
        Generic.assert_dict(source=resp_json, expected=updated_car)

    def test_patch_car_not_found(self):
        url = f'{self.base_url}/car'
        put_car = Generic.car_patch()
        put_car.update({'id': 1946})
        resp = requests.patch(url, json=put_car)
        resp_json = resp.json()

        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIsInstance(resp_json, dict)
        Generic.assert_dict(source=resp_json, expected={'detail': ReturnMessage.CAR_NOT_FOUND.value})

    def test_patch_id_only(self):
        url = f'{self.base_url}/car'
        resp = requests.patch(url, json={'id': 1})
        resp_json = resp.json()

        self.assertEqual(resp.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.assertIsInstance(resp_json, dict)
        Generic.assert_dict(source=resp_json, expected={'detail': ReturnMessage.BODY_MORE_THAN_ID.value})

    def test_patch_id_missing(self):
        url = f'{self.base_url}/car'
        resp = requests.patch(url, json={})
        resp_json = resp.json()

        self.assertEqual(resp.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        resp_obj = Generic.get_detail_info(type_field=Detail.MISSING,
                                           field='id',
                                           msg=Detail.FIELD_REQUIRED,
                                           input_data={})
        self.assertIsInstance(resp_json, dict)
        Generic.assert_dict(source=resp_json, expected=resp_obj)

    def test_patch_id_wrong_type(self):
        update_car = {
            'id': 'x',
        }
        url = f'{self.base_url}/car'
        resp = requests.patch(url, json=update_car)
        resp_json = resp.json()

        self.assertEqual(resp.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        resp_obj = Generic.get_detail_info(type_field=Detail.INT_PARSING,
                                           field='id',
                                           msg=Detail.INPUT_VALID_INTEGER,
                                           input_data='x')
        self.assertIsInstance(resp_json, dict)
        Generic.assert_dict(source=resp_json, expected=resp_obj)

    def test_patch_id_zero(self):
        new_car = {
            'id': 0,
            'make': 'b',
            'model': 'a'
        }
        url = f'{self.base_url}/car'
        resp = requests.patch(url, json=new_car)
        resp_json = resp.json()

        self.assertEqual(resp.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        resp_obj = Generic.get_detail_info(type_field=Detail.GREATER_THAN,
                                           field='id',
                                           msg=Detail.INPUT_VALID_INTEGER_GREATER_THAN,
                                           input_data=0,
                                           gt=0)
        self.assertIsInstance(resp_json, dict)
        Generic.assert_dict(source=resp_json, expected=resp_obj)

    def test_patch_make_model_equal(self):
        url = f'{self.base_url}/car'
        car_post = Generic.car_put()
        resp = requests.patch(url, json=car_post)
        resp_json = resp.json()

        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIsInstance(resp_json, dict)
        Generic.assert_dict(source=resp_json, expected={'detail': ReturnMessage.CAR_EXIST.value})

    def test_patch_make_equal(self):
        url = f'{self.base_url}/car'
        car_post = Generic.car_put()
        car_post.update({'model': 'brum'})
        resp = requests.patch(url, json=car_post)
        resp_json = resp.json()

        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIsInstance(resp_json, dict)
        Generic.assert_dict(source=resp_json, expected={'detail': ReturnMessage.CAR_EXIST.value})

    def test_patch_make_wrong_type(self):
        update_car = {
            'id': 2,
            'make': 412,
        }
        url = f'{self.base_url}/car'
        resp = requests.patch(url, json=update_car)
        resp_json = resp.json()

        self.assertEqual(resp.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        resp_obj = Generic.get_detail_info(type_field=Detail.STRING_TYPE,
                                           field='make',
                                           msg=Detail.INPUT_VALID_STRING,
                                           input_data=412)
        self.assertIsInstance(resp_json, dict)
        Generic.assert_dict(source=resp_json, expected=resp_obj)

    def test_patch_make_empty(self):
        new_car = {
            'id': 2,
            'make': ''
        }
        url = f'{self.base_url}/car'
        resp = requests.patch(url, json=new_car)
        resp_json = resp.json()

        self.assertEqual(resp.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        resp_obj = Generic.get_detail_info(type_field=Detail.STRING_TOO_SHORT,
                                           field='make',
                                           msg=Detail.INPUT_VALID_STRING_MIN_LENGTH,
                                           input_data='',
                                           min_length=1)
        self.assertIsInstance(resp_json, dict)
        Generic.assert_dict(source=resp_json, expected=resp_obj)

    def test_patch_make_spaces(self):
        new_car = {
            'id': 2,
            'make': '    '
        }
        url = f'{self.base_url}/car'
        resp = requests.patch(url, json=new_car)
        resp_json = resp.json()

        self.assertEqual(resp.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        resp_obj = Generic.get_detail_info(type_field=Detail.STRING_TOO_SHORT,
                                           field='make',
                                           msg=Detail.INPUT_VALID_STRING_MIN_LENGTH,
                                           input_data='    ',
                                           min_length=1)
        self.assertIsInstance(resp_json, dict)
        Generic.assert_dict(source=resp_json, expected=resp_obj)

    def test_patch_model_equal(self):
        url = f'{self.base_url}/car'
        car_post = Generic.car_put()
        car_post.update({'make': 'brum'})
        resp = requests.patch(url, json=car_post)
        resp_json = resp.json()

        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIsInstance(resp_json, dict)
        Generic.assert_dict(source=resp_json, expected={'detail': ReturnMessage.CAR_EXIST.value})

    def test_patch_model_wrong_type(self):
        update_car = {
            'id': 2,
            'model': 9
        }
        url = f'{self.base_url}/car'
        resp = requests.patch(url, json=update_car)
        resp_json = resp.json()

        self.assertEqual(resp.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        resp_obj = Generic.get_detail_info(type_field=Detail.STRING_TYPE,
                                           field='model',
                                           msg=Detail.INPUT_VALID_STRING,
                                           input_data=9)
        self.assertIsInstance(resp_json, dict)
        Generic.assert_dict(source=resp_json, expected=resp_obj)

    def test_patch_model_empty(self):
        new_car = {
            'id': 2,
            'model': ''
        }
        url = f'{self.base_url}/car'
        resp = requests.patch(url, json=new_car)
        resp_json = resp.json()

        self.assertEqual(resp.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        resp_obj = Generic.get_detail_info(type_field=Detail.STRING_TOO_SHORT,
                                           field='model',
                                           msg=Detail.INPUT_VALID_STRING_MIN_LENGTH,
                                           input_data='',
                                           min_length=1)
        self.assertIsInstance(resp_json, dict)
        Generic.assert_dict(source=resp_json, expected=resp_obj)

    def test_patch_model_spaces(self):
        new_car = {
            'id': 2,
            'model': '   '
        }
        url = f'{self.base_url}/car'
        resp = requests.patch(url, json=new_car)
        resp_json = resp.json()

        self.assertEqual(resp.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        resp_obj = Generic.get_detail_info(type_field=Detail.STRING_TOO_SHORT,
                                           field='model',
                                           msg=Detail.INPUT_VALID_STRING_MIN_LENGTH,
                                           input_data='   ',
                                           min_length=1)
        self.assertIsInstance(resp_json, dict)
        Generic.assert_dict(source=resp_json, expected=resp_obj)

    def test_patch_color_wrong_type(self):
        update_car = {
            'id': 2,
            'color': 1234
        }
        url = f'{self.base_url}/car'
        resp = requests.patch(url, json=update_car)
        resp_json = resp.json()

        self.assertEqual(resp.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        resp_obj = Generic.get_detail_info(type_field=Detail.STRING_TYPE,
                                           field='color',
                                           msg=Detail.INPUT_VALID_STRING,
                                           input_data=1234)
        self.assertIsInstance(resp_json, dict)
        Generic.assert_dict(source=resp_json, expected=resp_obj)

    def test_patch_color_empty(self):
        new_car = {
            'id': 2,
            'color': ''
        }
        url = f'{self.base_url}/car'
        resp = requests.patch(url, json=new_car)
        resp_json = resp.json()

        self.assertEqual(resp.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        resp_obj = Generic.get_detail_info(type_field=Detail.STRING_TOO_SHORT,
                                           field='color',
                                           msg=Detail.INPUT_VALID_STRING_MIN_LENGTH,
                                           input_data='',
                                           min_length=1)
        self.assertIsInstance(resp_json, dict)
        Generic.assert_dict(source=resp_json, expected=resp_obj)

    def test_patch_color_spaces(self):
        new_car = {
            'id': 2,
            'color': '  '
        }
        url = f'{self.base_url}/car'
        resp = requests.patch(url, json=new_car)
        resp_json = resp.json()

        self.assertEqual(resp.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        resp_obj = Generic.get_detail_info(type_field=Detail.STRING_TOO_SHORT,
                                           field='color',
                                           msg=Detail.INPUT_VALID_STRING_MIN_LENGTH,
                                           input_data='  ',
                                           min_length=1)
        self.assertIsInstance(resp_json, dict)
        Generic.assert_dict(source=resp_json, expected=resp_obj)

    def test_patch_year_manufactured_wrong_type(self):
        update_car = {
            'id': 2,
            'year_manufactured': 'b'
        }
        url = f'{self.base_url}/car'
        resp = requests.patch(url, json=update_car)
        resp_json = resp.json()

        self.assertEqual(resp.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        resp_obj = Generic.get_detail_info(type_field=Detail.INT_PARSING,
                                           field='year_manufactured',
                                           msg=Detail.INPUT_VALID_INTEGER,
                                           input_data='b')
        self.assertIsInstance(resp_json, dict)
        Generic.assert_dict(source=resp_json, expected=resp_obj)

    def test_patch_year_manufactured_zero(self):
        new_car = {
            'id': 2,
            'year_manufactured': 0
        }
        url = f'{self.base_url}/car'
        resp = requests.patch(url, json=new_car)
        resp_json = resp.json()

        self.assertEqual(resp.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        resp_obj = Generic.get_detail_info(type_field=Detail.GREATER_THAN,
                                           field='year_manufactured',
                                           msg=Detail.INPUT_VALID_INTEGER_GREATER_THAN,
                                           input_data=0,
                                           gt=0)
        self.assertIsInstance(resp_json, dict)
        Generic.assert_dict(source=resp_json, expected=resp_obj)

    def test_patch_year_model_wrong_type(self):
        update_car = {
            'id': 2,
            'year_model': 'c'
        }
        url = f'{self.base_url}/car'
        resp = requests.patch(url, json=update_car)
        resp_json = resp.json()

        self.assertEqual(resp.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        resp_obj = Generic.get_detail_info(type_field=Detail.INT_PARSING,
                                           field='year_model',
                                           msg=Detail.INPUT_VALID_INTEGER,
                                           input_data='c')
        self.assertIsInstance(resp_json, dict)
        Generic.assert_dict(source=resp_json, expected=resp_obj)

    def test_patch_year_model_zero(self):
        new_car = {
            'id': 2,
            'year_model': 0
        }
        url = f'{self.base_url}/car'
        resp = requests.patch(url, json=new_car)
        resp_json = resp.json()

        self.assertEqual(resp.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        resp_obj = Generic.get_detail_info(type_field=Detail.GREATER_THAN,
                                           field='year_model',
                                           msg=Detail.INPUT_VALID_INTEGER_GREATER_THAN,
                                           input_data=0,
                                           gt=0)
        self.assertIsInstance(resp_json, dict)
        Generic.assert_dict(source=resp_json, expected=resp_obj)

    def test_patch_fuel_wrong_type(self):
        update_car = {
            'id': 2,
            'fuel': 4879
        }
        url = f'{self.base_url}/car'
        resp = requests.patch(url, json=update_car)
        resp_json = resp.json()

        self.assertEqual(resp.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        resp_obj = Generic.get_detail_info(type_field=Detail.STRING_TYPE,
                                           field='fuel',
                                           msg=Detail.INPUT_VALID_STRING,
                                           input_data=4879)
        self.assertIsInstance(resp_json, dict)
        Generic.assert_dict(source=resp_json, expected=resp_obj)

    def test_patch_fuel_empty(self):
        new_car = {
            'id': 2,
            'fuel': ''
        }
        url = f'{self.base_url}/car'
        resp = requests.patch(url, json=new_car)
        resp_json = resp.json()

        self.assertEqual(resp.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        resp_obj = Generic.get_detail_info(type_field=Detail.STRING_TOO_SHORT,
                                           field='fuel',
                                           msg=Detail.INPUT_VALID_STRING_MIN_LENGTH,
                                           input_data='',
                                           min_length=1)
        self.assertIsInstance(resp_json, dict)
        Generic.assert_dict(source=resp_json, expected=resp_obj)

    def test_patch_fuel_spaces(self):
        new_car = {
            'id': 2,
            'fuel': '  '
        }
        url = f'{self.base_url}/car'
        resp = requests.patch(url, json=new_car)
        resp_json = resp.json()

        self.assertEqual(resp.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        resp_obj = Generic.get_detail_info(type_field=Detail.STRING_TOO_SHORT,
                                           field='fuel',
                                           msg=Detail.INPUT_VALID_STRING_MIN_LENGTH,
                                           input_data='  ',
                                           min_length=1)
        self.assertIsInstance(resp_json, dict)
        Generic.assert_dict(source=resp_json, expected=resp_obj)

    def test_patch_horsepower_wrong_type(self):
        update_car = {
            'id': 2,
            'horsepower': 'd'
        }
        url = f'{self.base_url}/car'
        resp = requests.patch(url, json=update_car)
        resp_json = resp.json()

        self.assertEqual(resp.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        resp_obj = Generic.get_detail_info(type_field=Detail.INT_PARSING,
                                           field='horsepower',
                                           msg=Detail.INPUT_VALID_INTEGER,
                                           input_data='d')
        self.assertIsInstance(resp_json, dict)
        Generic.assert_dict(source=resp_json, expected=resp_obj)

    def test_patch_horsepower_zero(self):
        new_car = {
            'id': 2,
            'horsepower': 0
        }
        url = f'{self.base_url}/car'
        resp = requests.patch(url, json=new_car)
        resp_json = resp.json()

        self.assertEqual(resp.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        resp_obj = Generic.get_detail_info(type_field=Detail.GREATER_THAN,
                                           field='horsepower',
                                           msg=Detail.INPUT_VALID_INTEGER_GREATER_THAN,
                                           input_data=0,
                                           gt=0)
        self.assertIsInstance(resp_json, dict)
        Generic.assert_dict(source=resp_json, expected=resp_obj)

    def test_patch_doors_wrong_type(self):
        update_car = {
            'id': 2,
            'doors': 'e'
        }
        url = f'{self.base_url}/car'
        resp = requests.patch(url, json=update_car)
        resp_json = resp.json()

        self.assertEqual(resp.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        resp_obj = Generic.get_detail_info(type_field=Detail.INT_PARSING,
                                           field='doors',
                                           msg=Detail.INPUT_VALID_INTEGER,
                                           input_data='e')
        self.assertIsInstance(resp_json, dict)
        Generic.assert_dict(source=resp_json, expected=resp_obj)

    def test_patch_doors_zero(self):
        new_car = {
            'id': 2,
            'doors': 0
        }
        url = f'{self.base_url}/car'
        resp = requests.patch(url, json=new_car)
        resp_json = resp.json()

        self.assertEqual(resp.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        resp_obj = Generic.get_detail_info(type_field=Detail.GREATER_THAN,
                                           field='doors',
                                           msg=Detail.INPUT_VALID_INTEGER_GREATER_THAN,
                                           input_data=0,
                                           gt=0)
        self.assertIsInstance(resp_json, dict)
        Generic.assert_dict(source=resp_json, expected=resp_obj)

    def test_patch_seats_wrong_type(self):
        update_car = {
            'id': 2,
            'seats': 'f'
        }
        url = f'{self.base_url}/car'
        resp = requests.patch(url, json=update_car)
        resp_json = resp.json()

        self.assertEqual(resp.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        resp_obj = Generic.get_detail_info(type_field=Detail.INT_PARSING,
                                           field='seats',
                                           msg=Detail.INPUT_VALID_INTEGER,
                                           input_data='f')
        self.assertIsInstance(resp_json, dict)
        Generic.assert_dict(source=resp_json, expected=resp_obj)

    def test_patch_seats_zero(self):
        new_car = {
            'id': 2,
            'seats': 0
        }
        url = f'{self.base_url}/car'
        resp = requests.patch(url, json=new_car)
        resp_json = resp.json()

        self.assertEqual(resp.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        resp_obj = Generic.get_detail_info(type_field=Detail.GREATER_THAN,
                                           field='seats',
                                           msg=Detail.INPUT_VALID_INTEGER_GREATER_THAN,
                                           input_data=0,
                                           gt=0)
        self.assertIsInstance(resp_json, dict)
        Generic.assert_dict(source=resp_json, expected=resp_obj)

    def test_patch_fipe_wrong_type(self):
        update_car = {
            'id': 2,
            'fipe': 9876
        }
        url = f'{self.base_url}/car'
        resp = requests.patch(url, json=update_car)
        resp_json = resp.json()

        self.assertEqual(resp.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        resp_obj = Generic.get_detail_info(type_field=Detail.STRING_TYPE,
                                           field='fipe',
                                           msg=Detail.INPUT_VALID_STRING,
                                           input_data=9876)
        self.assertIsInstance(resp_json, dict)
        Generic.assert_dict(source=resp_json, expected=resp_obj)

    def test_patch_fipe_empty(self):
        new_car = {
            'id': 2,
            'fipe': ''
        }
        url = f'{self.base_url}/car'
        resp = requests.patch(url, json=new_car)
        resp_json = resp.json()

        self.assertEqual(resp.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        resp_obj = Generic.get_detail_info(type_field=Detail.STRING_TOO_SHORT,
                                           field='fipe',
                                           msg=Detail.INPUT_VALID_STRING_MIN_LENGTH,
                                           input_data='',
                                           min_length=1)
        self.assertIsInstance(resp_json, dict)
        Generic.assert_dict(source=resp_json, expected=resp_obj)

    def test_patch_fipe_spaces(self):
        new_car = {
            'id': 2,
            'fipe': '   '
        }
        url = f'{self.base_url}/car'
        resp = requests.patch(url, json=new_car)
        resp_json = resp.json()

        self.assertEqual(resp.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        resp_obj = Generic.get_detail_info(type_field=Detail.STRING_TOO_SHORT,
                                           field='fipe',
                                           msg=Detail.INPUT_VALID_STRING_MIN_LENGTH,
                                           input_data='   ',
                                           min_length=1)
        self.assertIsInstance(resp_json, dict)
        Generic.assert_dict(source=resp_json, expected=resp_obj)
