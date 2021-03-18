import numpy as np
from collections import namedtuple


DEFAULT_WIDTH = 100


def get_circumference_crd(center, radius, angle):
    # 与えられた情報を元に円周上の座標を返す
    # `angle`はラジアン
    return center[0] + (radius * np.cos(angle)), center[1] + (radius * np.sin(angle))


def get_point_symmetry(p, center):
    # `center`を中心とした`p`の点対象を返す
    d = abs(center - p)
    return center - d if p > center else center + d


def get_point_symmetry_y(p, center_y):
    # `center`を中心として`y`座標を反転させる
    return p[0], get_point_symmetry(p[1], center_y)


def is_point_in_triangle(p, t1, t2, t3):
    c1 = (t2[0]-t1[0])*(p[1]-t1[1])-(t2[1]-t1[1])*(p[0]-t1[0])
    c2 = (t3[0]-t2[0])*(p[1]-t2[1])-(t3[1]-t2[1])*(p[0]-t2[0])
    c3 = (t1[0]-t3[0])*(p[1]-t3[1])-(t1[1]-t3[1])*(p[0]-t3[0])
    return (c1 < 0 and c2 < 0 and c3 < 0) or (c1 > 0 and c2 > 0 and c3 > 0)


def facing_to_radians(f, F):
    # `facing`をラジアンに変換する
    return (F[0] - f) / (F[0] - F[1]) * 2 * np.pi + np.pi / 2


def get_quadrant_corners(center, front, width, idx):
    # タゲサークルを罰印で4つに分けた時の第n象限の円周座標を返す
    # `idx`は[0,1,2,3]の値を取り、北から反時計回りに増加
    p_1 = -1/8 + (1/4) * idx
    p_2 = p_1 + 1/4
    return get_circumference_crd(center, width, front + p_1 * 2 * np.pi), \
        get_circumference_crd(center, width, front + p_2 * 2 * np.pi)


TargetCircle = namedtuple('TargetCircle', 'center width tilt')


def is_point_in_quadrant(p, idx, circle):
    left_corner, right_corner = get_quadrant_corners(circle.center, circle.tilt, circle.width, idx)
    return is_point_in_triangle(
        p,
        get_point_symmetry_y(left_corner, circle.center[1]),  # y座標を反転させてffの座標システム(左上が0,0)準拠にする
        get_point_symmetry_y(right_corner, circle.center[1]),
        circle.center)


def _is_back(f, target_loc, source_loc, F, width):
    f_r = facing_to_radians(f, F)  # ボスが向いてる向きのラジアン値
    return is_point_in_quadrant(source_loc, 2, TargetCircle(center=target_loc, width=width, tilt=f_r))


def _is_flack(f, target_loc, source_loc, F, width):
    f_r = facing_to_radians(f, F)
    if is_point_in_quadrant(source_loc, 1, TargetCircle(center=target_loc, width=width, tilt=f_r)):
        return True
    return is_point_in_quadrant(source_loc, 3, TargetCircle(center=target_loc, width=width, tilt=f_r))


class PositionalEvent(dict):
    @property
    def tr(self):
        return self['targetResources']

    @property
    def target_loc(self):
        return self.tr['x'] / 100, self.tr['y'] / 100

    @property
    def target_facing(self):
        return self.tr['facing']

    @property
    def sr(self):
        return self['sourceResources']

    @property
    def source_loc(self):
        return self.sr['x'] / 100, self.sr['y'] / 100


def is_back(event, facing_rng, width=DEFAULT_WIDTH):
    """
    ボスの座標を中心とした円から背面の三角形を計算して、
    プレイヤーがその中にいれば`True`を返す
    event: FFLogsのダメージイベント
    facing_rng: `facing`の値の範囲(他のイベントより推定)
    width: 円の幅
    計算の結果が狂う(背面にいるのに三角形の外に出る)事があるので、
    可視化しないなら広めに取る
    """
    pe = PositionalEvent(event)
    return _is_back(pe.target_facing, pe.target_loc, pe.source_loc, facing_rng, width)


def is_flack(event, facing_rng, width=DEFAULT_WIDTH):
    # 側面
    pe = PositionalEvent(event)
    return _is_flack(pe.target_facing, pe.target_loc, pe.source_loc, facing_rng, width)
