import json
import unittest
from main import *


class TestCase(unittest.TestCase):
    def setUp(self):
        self.facing_rng = (-158, -786)

    def read_event(self, fname):
        with open(fname) as f:
            return json.loads(f.read())

    def test_back_success(self):
        # 開幕3GCD目の方向指定成功してる月光
        self.assertTrue(is_back(self.read_event('fixtures/success.json'), facing_rng=self.facing_rng))

    def test_back_failure_short_width(self):
        # 上の`width`を少し縮めてプレイヤーがはみ出るようにする
        self.assertFalse(is_back(self.read_event('fixtures/success.json'), facing_rng=self.facing_rng, width=5))

    def test_back_failure_312(self):
        # 5:12頃の影潜りの方向指定失敗してるイベント
        self.assertFalse(is_back(self.read_event('fixtures/failure.json'), facing_rng=self.facing_rng))


if __name__ == '__main__':
    unittest.main()
