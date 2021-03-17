import json
import unittest
from main import *


class TestCase(unittest.TestCase):
    def setUp(self):
        self.facing_rng = (-158, -786)

    @staticmethod
    def read_event(fname):
        with open(fname) as f:
            return json.loads(f.read())

    def test_back_success(self):
        # 開幕3GCD目の方向指定成功してる月光
        self.assertTrue(is_back(self.read_event('fixtures/back.json'), facing_rng=self.facing_rng))

    def test_back_failure_short_width(self):
        # 上の`width`を少し縮めてプレイヤーがはみ出るようにする
        self.assertFalse(is_back(self.read_event('fixtures/back.json'), facing_rng=self.facing_rng, width=5))

    def test_back_failure_312(self):
        # 5:12頃の影潜りの方向指定失敗してるイベント
        self.assertFalse(is_back(self.read_event('fixtures/upper_left.json'), facing_rng=self.facing_rng))

    def test_flack_success(self):
        # 開幕3GCD目の方向指定成功してる月光
        self.assertTrue(is_flack(self.read_event('fixtures/flack.json'), facing_rng=self.facing_rng))

    def test_flack_failure_short_width(self):
        # 開幕3GCD目の方向指定成功してる月光
        self.assertFalse(is_flack(self.read_event('fixtures/flack.json'), facing_rng=self.facing_rng, width=3))

    def test_flack_failure_behind(self):
        # 開幕3GCD目の方向指定成功してる月光
        self.assertFalse(is_flack(self.read_event('fixtures/back.json'), facing_rng=self.facing_rng))


if __name__ == '__main__':
    unittest.main()
