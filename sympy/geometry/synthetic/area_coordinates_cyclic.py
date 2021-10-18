from sympy.geometry.synthetic.common import _geometric_quantities
from sympy.geometry.synthetic.quantities import SyntheticGeometrySignedArea as Area
from sympy.geometry.synthetic.quantities import SyntheticGeometryPythagorasDifference as Pythagoras
from sympy.geometry.synthetic.quantities import SyntheticGeometryDiameter as Diameter
from sympy.geometry.synthetic.quantities import SyntheticGeometryChord as Chord
from sympy.geometry.synthetic.quantities import SyntheticGeometryCochord as Cochord
from collections import Counter


def _auto_cyclic_coordinates(objective):
    def _get_points_quantity(expr):
        all_points = Counter()
        for G in _geometric_quantities(expr):
            all_points += Counter(G.args)
        return all_points

    free_points = _get_points_quantity(objective)
    free_points = free_points.most_common(1)

    if len(free_points) < 1:
        return None
    J = free_points[0][0]
    return J


def _cyclic_coordinates(objective):
    r"""Express $\mathcal{S}_{A, B, C}, \mathcal{P}_{A, B, C}$ as the
    area coordinates in the cyclic configuration
    """
    subs = {}
    for G in _geometric_quantities(objective, (Area, Pythagoras)):
        if isinstance(G, Area) and len(G.args) == 3:
            A, B, C = G.args
            subs[G] = Chord(A, B) * Chord(C, B) * Chord(C, A) / (2 * Diameter())
            subs[G] = subs[G].doit()
        elif isinstance(G, Pythagoras) and len(G.args) == 3:
            A, B, C = G.args
            subs[G] = Chord(A, B) * Chord(C, B) * Cochord(C, A) / Diameter() * 2
            subs[G] = subs[G].doit()
    return subs


def _cyclic_coordinates_sin_cos(J, objective):
    subs = {}
    for G in _geometric_quantities(objective, (Chord, Cochord)):
        if isinstance(G, Chord):
            A, B = G.args
            if J in (A, B):
                continue
            subs[G] = (Chord(J, B) * Cochord(J, A) - Chord(J, A) * Cochord(J, B)) / Diameter()
            subs[G] = subs[G].doit()
        elif isinstance(G, Cochord):
            A, B = G.args
            if J in (A, B):
                continue
            subs[G] = (Chord(J, A) * Chord(J, B) + Cochord(J, A) * Cochord(J, B)) / Diameter()
            subs[G] = subs[G].doit()
    return subs


def _cylcic_coordinates_pythagoras(objective):
    r"""Express $\widehat{A, B}^2$ as $\delta^2 - \widetilde{A, B}^2$"""
    subs = {}
    for G in _geometric_quantities(objective, Cochord):
        A, B = G.args
        subs[G**2] = Diameter()**2 - Chord(A, B)**2
        subs[G**2] = subs[G**2].doit()
    return subs
