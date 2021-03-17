import numpy as np


class PositionalContext(dict):
    @property
    def tr(self):
        return self['targetResources']

    @property
    def target_crds(self):
        return self.tr['x'] / 100, self.tr['y'] / 100

    @property
    def target_facing(self):
        return self.tr['facing']

    @property
    def sr(self):
        return self['sourceResources']

    @property
    def source_crds(self):
        return self.sr['x'] / 100, self.sr['y'] / 100


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


def is_point_in_triangle(t1, t2, t3, p):
    c1 = (t2[0]-t1[0])*(p[1]-t1[1])-(t2[1]-t1[1])*(p[0]-t1[0])
    c2 = (t3[0]-t2[0])*(p[1]-t2[1])-(t3[1]-t2[1])*(p[0]-t2[0])
    c3 = (t1[0]-t3[0])*(p[1]-t3[1])-(t1[1]-t3[1])*(p[0]-t3[0])
    return (c1 < 0 and c2 < 0 and c3 < 0) or (c1 > 0 and c2 > 0 and c3 > 0)


def is_back(e, F, width=30):
    """
    ボスの座標を中心とした円から背面の三角形を計算して、
    プレイヤーがその中にいれば`True`を返す
    e: FFLogsのダメージイベント
    F: `facing`の値の範囲(他のイベントより推定)
    width: 円の幅(可視化しないなら大きくすればいい)
    """
    ctx = PositionalContext(e)
    f = ctx.target_facing
    f_r = (F[0] - f) / (F[0] - F[1]) * 2 * np.pi + np.pi / 2  # ボスが向いてる向きのラジアン値
    left = get_circumference_crd(ctx.target_crds, width, f_r+3*np.pi/4)
    right = get_circumference_crd(ctx.target_crds, width, f_r+5*np.pi/4)
    return is_point_in_triangle(
        get_point_symmetry_y(left, ctx.target_crds[1]),
        get_point_symmetry_y(right, ctx.target_crds[1]),
        ctx.target_crds, ctx.source_crds)
