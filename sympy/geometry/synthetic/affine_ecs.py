from sympy.geometry.synthetic.ecs import AffineECS2 as ECS2
from sympy.geometry.synthetic.ecs import AffineECS4 as ECS4
from sympy.geometry.synthetic.ecs import AffineECS5 as ECS5
from sympy.geometry.synthetic.constructions import SyntheticGeometryOn as On
from sympy.geometry.synthetic.constructions import SyntheticGeometryLine as Line
from sympy.geometry.synthetic.constructions import SyntheticGeometryPLine as PLine
from sympy.geometry.synthetic.constructions import SyntheticGeometryLRatio as LRatio
from sympy.geometry.synthetic.constructions import SyntheticGeometryPRatio as PRatio
from sympy.geometry.synthetic.constructions import SyntheticGeometryIntersection as Intersection
from sympy.geometry.synthetic.constructions import SyntheticGeometryMidpoint as Midpoint
from sympy.geometry.synthetic.auxiliary import SyntheticGeometryAuxiliaryRatio as AuxiliaryRatio
from sympy.core.numbers import Rational


def _construction_to_ecs(construction):
    if isinstance(construction, On):
        Y, L = construction.args
        if isinstance(L, Line):
            P, Q = L.args
            return _construction_to_ecs(LRatio(Y, P, Q, AuxiliaryRatio(P, Y, P, Q)))
        if isinstance(L, PLine):
            R, P, Q = L.args
            return _construction_to_ecs(PRatio(Y, R, P, Q, AuxiliaryRatio(R, Y, P, Q)))

    if isinstance(construction, LRatio):
        return construction

    if isinstance(construction, PRatio):
        return construction

    if isinstance(construction, Midpoint):
        Y, P, Q = construction.args
        return _construction_to_ecs(LRatio(Y, P, Q, Rational(1, 2)))

    if isinstance(construction, Intersection):
        Y, L1, L2 = construction.args
        if isinstance(L1, Line) and isinstance(L2, Line):
            P, Q = L1.args
            U, V = L2.args
            return ECS2(Y, P, Q, U, V)
        if isinstance(L1, PLine) and isinstance(L2, Line):
            return _construction_to_ecs(Intersection(Y, L2, L1))
        if isinstance(L1, Line) and isinstance(L2, PLine):
            P, Q = L1.args
            W, U, V = L2.args
            return ECS4(Y, P, Q, W, U, V)
        if isinstance(L1, PLine) and isinstance(L2, PLine):
            R, P, Q = L1.args
            W, U, V = L2.args
            return ECS5(Y, R, P, Q, W, U, V)

    raise NotImplementedError(f"Unknown construction: {construction}")


def _constructions_to_ecs(constructions):
    return tuple(_construction_to_ecs(C) for C in constructions)
