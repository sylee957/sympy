from sympy.geometry.synthetic.ecs import (
    PlaneECS1 as ECS1,
    PlaneECS5 as ECS5,
    PlaneECS6 as ECS6,
    PlaneECS7 as ECS7,
    PlaneECS8 as ECS8,
)
from sympy.geometry.synthetic.constructions import SyntheticGeometryARatio as ARatio
from sympy.geometry.synthetic.constructions import SyntheticGeometryPRatio as PRatio
from sympy.geometry.synthetic.constructions import SyntheticGeometryTRatio as TRatio
from sympy.geometry.synthetic.constructions import SyntheticGeometryFoot as Foot
from sympy.geometry.synthetic.predicates import (
    SyntheticGeometryEqpoints as Eqpoints,
    SyntheticGeometryParallel as Parallel,
    SyntheticGeometryPerpendicular as Perpendicular,
    SyntheticGeometryCollinear as Collinear,
)


def _degenerate(C):
    if isinstance(C, ECS1):
        Y, P, Q, U, V = C.args
        return Parallel(P, Q, U, V)
    if isinstance(C, Foot):
        Y, P, U, V = C.args
        return Eqpoints(U, V)
    if isinstance(C, PRatio):
        Y, W, U, V, r = C.args
        return Eqpoints(U, V)
    if isinstance(C, TRatio):
        Y, U, V, r = C.args
        return Eqpoints(U, V)
    if isinstance(C, ECS5):
        Y, U, V, R, P, Q = C.args
        return Parallel(P, Q, U, V)
    if isinstance(C, ECS6):
        Y, U, V, R, P, Q = C.args
        return Perpendicular(P, Q, U, V)
    if isinstance(C, ECS7):
        Y, U, V, P, Q = C.args
        return Perpendicular(P, Q, U, V)
    if isinstance(C, ECS8):
        Y, U, V, O = C.args
        return Eqpoints(O, U) | Eqpoints(Y, U) | Eqpoints(U, V)
    if isinstance(C, ARatio):
        Y, O, U, V, r_O, r_U, r_V = C.args
        return Collinear(O, U, V)
    raise NotImplementedError(f"Degenerate condition for {C} is not implemented")
