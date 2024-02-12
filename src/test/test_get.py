from pathlib import Path
import os
import sys
sys.path.append(os.path.join(Path(__file__).parent.parent.parent))
from fastapi import status
from src.gen.generic import Generic, ReturnMessage
import requests
import unittest


class TestGet(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.base_url = Generic.get_base_url()

    def setUp(self) -> None:
        pass

    def test_get_all(self):
        url = f'{self.base_url}/cars'
        resp = requests.get(url)
        resp_json = resp.json()

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp_json), 1)
        self.assertIsInstance(resp_json, list)

        for resp_car in resp_json:
            Generic.assert_dict(source=resp_car, expected=Generic.car_post_expected())

    def test_get_car(self):
        url = f'{self.base_url}/car/1'
        resp = requests.get(url)
        resp_json = resp.json()

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIsInstance(resp_json, dict)
        Generic.assert_dict(source=resp_json, expected=Generic.car_post_expected())

    def test_get_car_not_found(self):
        url = f'{self.base_url}/car/122'
        resp = requests.get(url)
        resp_json = resp.json()

        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIsInstance(resp_json, dict)
        Generic.assert_dict(source=resp_json, expected={'detail': ReturnMessage.CAR_NOT_FOUND.value})
