from sympy.geometry.synthetic.ecs import (
    AffineECS2 as ECS2,
    AffineECS4 as ECS4,
    AffineECS5 as ECS5
)
from sympy.geometry.synthetic.constructions import (
    SyntheticGeometryLRatio as LRatio,
    SyntheticGeometryPRatio as PRatio
)
from sympy.geometry.synthetic.predicates import (
    SyntheticGeometryEqpoints as Eqpoints,
    SyntheticGeometryParallel as Parallel
)


def _degenerate(C):
    if isinstance(C, LRatio):
        Y, P, Q, r = C.args
        return Eqpoints(P, Q)
    if isinstance(C, ECS2):
        Y, P, Q, U, V = C.args
        return Parallel(P, Q, U, V)
    if isinstance(C, PRatio):
        Y, R, P, Q, r = C.args
        return Eqpoints(P, Q)
    if isinstance(C, ECS4):
        Y, U, V, R, P, Q = C.args
        return Parallel(P, Q, U, V)
    if isinstance(C, ECS5):
        Y, W, U, V, R, P, Q = C.args
        return Parallel(P, Q, U, V)
    raise NotImplementedError(f"Degenerate condition for {C} is not implemented")
