import numpy as np


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


def facing_to_radians(f, F):
    # `facing`をラジアンに変換する
    return (F[0] - f) / (F[0] - F[1]) * 2 * np.pi + np.pi / 2


def get_back_corners(f, target_crds, F, width):
    f_r = facing_to_radians(f, F)  # ボスが向いてる向きのラジアン値
    return get_circumference_crd(target_crds, width, f_r+3*np.pi/4), \
        get_circumference_crd(target_crds, width, f_r+5*np.pi/4)


def _is_back(f, target_crds, source_crds, F, width):
    left_corner, right_corner = get_back_corners(f, target_crds, F, width)
    return is_point_in_triangle(
        get_point_symmetry_y(left_corner, target_crds[1]),  # y座標を反転させてffの座標システム(左上が0,0)準拠にする
        get_point_symmetry_y(right_corner, target_crds[1]),
        target_crds, source_crds)


def parse_loc(res):
    return res['x'] / 100, res['y'] / 100


def is_back(e, F, width=30):
    """
    ボスの座標を中心とした円から背面の三角形を計算して、
    プレイヤーがその中にいれば`True`を返す
    e: FFLogsのダメージイベント
    F: `facing`の値の範囲(他のイベントより推定)
    width: 円の幅(可視化しないなら大きくすればいい)
    """
    tr = e['targetResources']
    return _is_back(tr['facing'], parse_loc(tr), parse_loc(e['sourceResources']), F, width)
