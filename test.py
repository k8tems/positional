import json
import unittest
from main import *


class TestCase(unittest.TestCase):
    def test_back_success(self):
        with open('fixtures/success.json') as f:
            event = json.loads(f.read())
        self.assertTrue(is_back(event, F=(-158, -786)))

    def test_back_failure(self):
        with open('fixtures/failure.json') as f:
            event = json.loads(f.read())
        self.assertFalse(is_back(event, F=(-158, -786)))


if __name__ == '__main__':
    unittest.main()
