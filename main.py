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
    x = center[0] + (radius * np.cos(angle))
    y = center[1] + (radius * np.sin(angle))
    return x, y


def get_point_symmetry(p, center):
    # `center`を中心とした`p`の点対象を返す
    d = abs(center - p)
    return center - d if p > center else center + d


def is_point_in_triangle_2(x1, y1, x2, y2, x3, y3, xp, yp):
    c1 = (x2-x1)*(yp-y1)-(y2-y1)*(xp-x1)
    c2 = (x3-x2)*(yp-y2)-(y3-y2)*(xp-x2)
    c3 = (x1-x3)*(yp-y3)-(y1-y3)*(xp-x3)
    return (c1<0 and c2<0 and c3<0) or (c1>0 and c2>0 and c3>0)


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
    F_l = (F[0] - F[1])
    f_r = (F[0] - f) / F_l * 2 * np.pi + np.pi / 2
    left = get_circumference_crd(ctx.target_crds, width, f_r+3*np.pi/4)
    right = get_circumference_crd(ctx.target_crds, width, f_r+5*np.pi/4)
    left_2 = left[0], get_point_symmetry(left[1], ctx.target_crds[1])
    right_2 = right[0], get_point_symmetry(right[1], ctx.target_crds[1])
    return is_point_in_triangle_2(
        left_2[0], left_2[1], right_2[0], right_2[1], ctx.target_crds[0], ctx.target_crds[1],
        ctx.source_crds[0], ctx.source_crds[1])
