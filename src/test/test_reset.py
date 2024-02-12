from pathlib import Path
import os
import sys
sys.path.append(os.path.join(Path(__file__).parent.parent.parent))
from fastapi import status
from src.gen.generic import Generic, ReturnMessage
import requests
import unittest


class TestReset(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.base_url = Generic.get_base_url()

    def setUp(self) -> None:
        pass

    def test_reset(self):
        url = f'{self.base_url}/reset'
        resp = requests.post(url)
        resp_json = resp.json()

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIsInstance(resp_json, dict)

        Generic.assert_dict(source=resp_json, expected={'detail': ReturnMessage.RESET_COMPLETED.value})
