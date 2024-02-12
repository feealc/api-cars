from pathlib import Path
import os
import sys
sys.path.append(os.path.join(Path(__file__).parent.parent.parent))
from fastapi import status
from src.gen.generic import Generic, ReturnMessage
import requests
import unittest


class TestDelete(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.base_url = Generic.get_base_url()

    def setUp(self) -> None:
        pass

    def test_delete(self):
        url = f'{self.base_url}/car/1'
        resp = requests.delete(url)
        resp_json = resp.json()

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIsInstance(resp_json, dict)
        Generic.assert_dict(source=resp_json, expected={'detail': ReturnMessage.CAR_DELETED.value})

    def test_delete_car_not_found(self):
        url = f'{self.base_url}/car/2345'
        resp = requests.delete(url)
        resp_json = resp.json()

        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIsInstance(resp_json, dict)
        Generic.assert_dict(source=resp_json, expected={'detail': ReturnMessage.CAR_NOT_FOUND.value})
