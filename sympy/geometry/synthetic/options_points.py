from sympy.geometry.synthetic.common import _geometric_quantities


def _get_points_quantity(expr):
    all_points = set()
    for G in _geometric_quantities(expr):
        new_points = set(G.args)
        all_points = all_points.union(new_points)
    return all_points
