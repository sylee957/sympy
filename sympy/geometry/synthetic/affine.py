from sympy.core.numbers import Rational
from sympy.core.singleton import S
from sympy.geometry.synthetic.quantities import (
    SyntheticGeometryFrozenSignedRatio as FrozenRatio,
    SyntheticGeometryMainVariable as MainVariable
)
from sympy.core.relational import Eq
from sympy.geometry.synthetic.constructions import (
    SyntheticGeometryLRatio as LRatio,
    SyntheticGeometryPRatio as PRatio,
    SyntheticGeometryOn as On,
    SyntheticGeometryLine as Line,
    SyntheticGeometryPLine as PLine,
    SyntheticGeometryMidpoint as Midpoint
)
from sympy.geometry.synthetic.common import (
    _quadrilateral_area,
    _uniformize_area,
    _uniformize_ratio,
    _pp_sparse,
    _coeff_sparse,
    _compress
)
from sympy.geometry.synthetic.affine_area import (
    _eliminate_area_lratio,
    _eliminate_area_pratio,
    _eliminate_area_inter_line_line,
    _eliminate_area_inter_pline_line,
    _eliminate_area_inter_pline_pline,
)
from sympy.geometry.synthetic.affine_ratio import (
    _eliminate_ratio_lratio,
    _eliminate_ratio_pratio,
    _eliminate_ratio_inter_line_line,
    _eliminate_ratio_inter_pline_line,
    _eliminate_ratio_inter_pline_pline,
)
from sympy.geometry.synthetic.area_coordinates import _area_coordinates
from sympy.geometry.synthetic.options import (
    _auto_option_prove,
    _auto_coordinates_skew
)
from sympy.geometry.synthetic.options_predicate import _normalize_predicate_affine
from sympy.geometry.synthetic.degenerate import _degenerate_construction
from sympy.polys.rings import sring


def _rewrite_and_eliminate(C, constructions, domain, objective, X):
    if isinstance(C, On):
        Y, L = C.args
        if isinstance(L, Line):
            P, Q = L.args
            C = LRatio(Y, Line(P, Q), FrozenRatio(P, Y, P, Q))
            return _eliminate(C, constructions, domain, objective, X)
        if isinstance(L, PLine):
            R, P, Q = L.args
            C = PRatio(Y, R, Line(P, Q), FrozenRatio(R, Y, P, Q))
            return _eliminate(C, constructions, domain, objective, X)
    if isinstance(C, Midpoint):
        Y, L = C.args
        if isinstance(L, Line):
            U, V = L.args
            C = LRatio(Y, Line(U, V), Rational(1, 2))
            return _eliminate(C, constructions, domain, objective, X)
    return domain, objective


def _eliminate(C, constructions, domain, objective, X):
    while True:
        old = objective

        domain, objective = _uniformize_area(domain, objective)
        domain, objective = _uniformize_ratio(domain, objective)
        domain, objective = _quadrilateral_area(domain, objective)

        domain, objective = _eliminate_area_lratio(C, constructions, domain, objective)
        domain, objective = _eliminate_area_pratio(C, constructions, domain, objective)
        domain, objective = _eliminate_area_inter_line_line(C, constructions, domain, objective)
        domain, objective = _eliminate_area_inter_pline_line(C, constructions, domain, objective)
        domain, objective = _eliminate_area_inter_pline_pline(C, constructions, domain, objective)

        domain, objective = _eliminate_ratio_lratio(C, constructions, domain, objective, area_method_affine)
        domain, objective = _eliminate_ratio_pratio(C, constructions, domain, objective, area_method_affine)
        domain, objective = _eliminate_ratio_inter_line_line(C, constructions, domain, objective, area_method_affine)
        domain, objective = _eliminate_ratio_inter_pline_line(C, constructions, domain, objective, area_method_affine)
        domain, objective = _eliminate_ratio_inter_pline_pline(C, constructions, domain, objective, area_method_affine)

        domain, objective = _rewrite_and_eliminate(C, constructions, domain, objective, X)
        domain, objective = _pp_sparse(domain, objective, X)

        new = objective
        if old == new:
            break
    return domain, objective


def _area_method_affine_thread(constructions, objective, *, O=None, U=None, V=None, prove=None, debug=False):
    X = MainVariable()
    objective = objective.doit()
    numer, denom = objective.as_numer_denom()
    ring, objective = sring(denom * X - numer)
    domain = ring.to_domain()

    for i in reversed(range(len(constructions))):
        C = constructions[i]
        if prove:
            assertion = _degenerate_construction(C)
            if area_method_affine(constructions[:i], assertion, prove=True) is S.true:
                return S.true

        domain, objective = _eliminate(C, constructions[:i], domain, objective, X)

        if debug:
            from IPython.display import display, Latex
            from sympy.printing.latex import latex
            display(Latex(r'$\text{Eliminated points from : } %s$' % latex(C)))
            display(objective)

    a = _coeff_sparse(domain, objective, X, 1)
    b = _coeff_sparse(domain, objective, X, 0)
    if b == 0:
        if prove:
            return S.true
        return S.Zero

    domain, objective = _area_coordinates(O, U, V, domain, objective)
    domain, objective = _pp_sparse(domain, objective, X)
    domain, objective = _compress(domain, objective)

    if debug:
        from IPython.display import display, Latex
        from sympy.printing.latex import latex
        display(Latex(r'$\text{Evaluating area coordinates : }$'))
        display(objective)

    a = _coeff_sparse(domain, objective, X, 1)
    b = _coeff_sparse(domain, objective, X, 0)
    if prove:
        if b == 0:
            return S.true
        return S.false
    return -domain.to_sympy(b) / domain.to_sympy(a)


def area_method_affine(constructions, objective, *, O=None, U=None, V=None, prove=None, debug=False):
    constructions = tuple(constructions)
    prove = _auto_option_prove(objective, prove)
    objective = _normalize_predicate_affine(objective)
    O, U, V = _auto_coordinates_skew(objective, O, U, V)

    if prove:
        if isinstance(objective, Eq):
            lhs, rhs = objective.args
            objective = lhs - rhs
            return _area_method_affine_thread(constructions, objective, O=O, U=U, V=V, prove=True, debug=debug)
        raise NotImplementedError
    return _area_method_affine_thread(constructions, objective, O=O, U=U, V=V, prove=False, debug=debug)
