import json
import unittest
from main import *


class TestCase(unittest.TestCase):
    def test_back_success(self):
        # 開幕3GCD目の方向指定成功してる月光
        with open('fixtures/success.json') as f:
            event = json.loads(f.read())
        self.assertTrue(is_back(event, F=(-158, -786)))

    def test_back_failure_short_width(self):
        # 上の`width`を少し縮めてプレイヤーがはみ出るようにする
        with open('fixtures/success.json') as f:
            event = json.loads(f.read())
        self.assertFalse(is_back(event, F=(-158, -786), width=5))

    def test_back_failure_312(self):
        # 5:12頃の影潜りの方向指定失敗してるイベント
        with open('fixtures/failure.json') as f:
            event = json.loads(f.read())
        self.assertFalse(is_back(event, F=(-158, -786)))


if __name__ == '__main__':
    unittest.main()
