from sympy.geometry.synthetic.quantities import SyntheticGeometrySignedArea as Area
from sympy.geometry.synthetic.quantities import SyntheticGeometrySignedRatio as Ratio
from sympy.geometry.synthetic.quantities_twoline import SyntheticGeometryTwolineAlpha as Alpha
from sympy.geometry.synthetic.quantities_twoline import SyntheticGeometryTwolineBeta as Beta
from sympy.geometry.synthetic.quantities import SyntheticGeometrySignedLength as Length
from sympy.geometry.synthetic.auxiliary import SyntheticGeometryAuxiliaryTwolineO1 as O1
from sympy.geometry.synthetic.auxiliary import SyntheticGeometryAuxiliaryTwolineO2 as O2
from sympy.core.singleton import S


def _get_areas(E):
    r"""Get areas"""
    if not E.args:
        return set()
    if isinstance(E, Area):
        return {E}
    return set.union(*(_get_areas(arg) for arg in E.args))


def _get_ratios(E):
    r"""Get areas"""
    if not E.args:
        return set()
    if isinstance(E, Ratio):
        return {E}
    return set.union(*(_get_ratios(arg) for arg in E.args))


def _get_lengths(E):
    r"""Get areas"""
    if not E.args:
        return set()
    if isinstance(E, Length):
        return {E}
    return set.union(*(_get_lengths(arg) for arg in E.args))


def _match_twoline(A, B, C, line_1, line_2):
    if A in line_1 and {B, C}.issubset(line_2):
        return 1, A, B, C
    elif B in line_1 and {C, A}.issubset(line_2):
        return 1, B, C, A
    elif C in line_1 and {A, B}.issubset(line_2):
        return 1, C, A, B
    elif A in line_2 and {B, C}.issubset(line_1):
        return -1, A, B, C
    elif B in line_2 and {C, A}.issubset(line_1):
        return -1, B, C, A
    elif C in line_2 and {A, B}.issubset(line_1):
        return -1, C, A, B


def _twoline_area_A(objective, line_1, line_2):
    subs = {}
    for G in _get_areas(objective):
        if not len(G.args) == 3:
            continue
        A, B, C = G.args
        if {A, B, C}.issubset(line_1):
            subs[G] = S.Zero
            continue
        if {A, B, C}.issubset(line_2):
            subs[G] = S.Zero
            continue

        match = _match_twoline(A, B, C, line_1, line_2)
        if match is None:
            continue
        sign, _, B, C = match
        subs[G] = sign * S.Half * Alpha() * Length(B, C)
        subs[G] = subs[G].doit()
    return subs


def _twoline_area_B(objective, line_1, line_2, O):
    subs = {}
    for G in _get_areas(objective):
        if not len(G.args) == 3:
            continue
        A, B, C = G.args
        if {A, B, C}.issubset(line_1):
            subs[G] = S.Zero
            continue
        if {A, B, C}.issubset(line_2):
            subs[G] = S.Zero
            continue

        match = _match_twoline(A, B, C, line_1, line_2)
        if match is None:
            continue
        sign, A, B, C = match
        subs[G] = sign * S.Half * Beta() * Length(O, A) * Length(B, C)
        subs[G] = subs[G].doit()
    return subs


def _twoline_split_ratio(objective):
    subs = {}
    for G in _get_ratios(objective):
        if not len(G.args) == 4:
            continue

        A, B, C, D = G.args
        subs[G] = Length(A, B) / Length(C, D)
        subs[G] = subs[G].doit()
    return subs


def _twoline_length_A(objective, line_1, line_2):
    subs = {}
    for G in _get_lengths(objective):
        A, B = G.args
        if {A, B}.issubset(line_1):
            subs[G] = Length(O1(), B) - Length(O1(), A)
            subs[G] = subs[G].doit()
        elif {A, B}.issubset(line_2):
            subs[G] = Length(O2(), B) - Length(O2(), A)
            subs[G] = subs[G].doit()
    return subs


def _twoline_length_B(objective, line_1, line_2, O):
    subs = {}
    for G in _get_lengths(objective):
        A, B = G.args
        subs[G] = Length(O, B) - Length(O, A)
        subs[G] = subs[G].doit()
    return subs
