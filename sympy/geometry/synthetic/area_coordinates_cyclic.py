from sympy.geometry.synthetic.common import _geometric_quantities
from sympy.geometry.synthetic.quantities import SyntheticGeometrySignedArea as Area
from sympy.geometry.synthetic.quantities import SyntheticGeometryPythagorasDifference as Pythagoras
from sympy.geometry.synthetic.quantities import SyntheticGeometryDiameter as Diameter
from sympy.geometry.synthetic.quantities import SyntheticGeometryChord as Chord
from sympy.geometry.synthetic.quantities import SyntheticGeometryCochord as Cochord


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


def _cylcic_coordinates_pythagoras(objective):
    r"""Express $\widehat{A, B}^2$ as $\delta^2 - \widetilde{A, B}^2$"""
    subs = {}
    for G in _geometric_quantities(objective, Cochord):
        A, B = G.args
        subs[G**2] = Diameter()**2 - Chord(A, B)**2
        subs[G**2] = subs[G**2].doit()
    return subs
