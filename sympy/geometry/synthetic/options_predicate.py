from sympy.core.symbol import Dummy
from sympy.core.relational import Eq
from sympy.core.singleton import S
from sympy.core.basic import Atom
from sympy.geometry.synthetic.quantities import SyntheticGeometrySignedArea as Area
from sympy.geometry.synthetic.quantities import SyntheticGeometrySignedRatio as Ratio
from sympy.geometry.synthetic.predicates import SyntheticGeometryCollinear as Collinear
from sympy.geometry.synthetic.predicates import SyntheticGeometryParallel as Parallel
from sympy.geometry.synthetic.predicates import SyntheticGeometrySamePoints as SamePoints


def _normalize_predicate_affine(objective):
    if isinstance(objective, Collinear):
        A, B, C = objective.args
        return Eq(Area(A, B, C), S.Zero)
    if isinstance(objective, Parallel):
        A, B, C, D = objective.args
        return Eq(Area(A, B, C) - Area(A, B, D), S.Zero)
    if isinstance(objective, SamePoints):
        A, B = objective.args
        X, Y = Dummy('$X'), Dummy('$Y')
        return Eq(Ratio(A, B, X, Y), S.Zero)
    if not isinstance(objective, Atom):
        return objective.func(*(_normalize_predicate_affine(arg) for arg in objective.args))
    return objective
