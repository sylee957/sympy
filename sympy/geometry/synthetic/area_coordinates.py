from sympy.core.basic import Basic


class SyntheticGeometryPlanarConfiguration(Basic):
    r"""Represents the free point configuration where all the free
    points are assumed to exist in the whole euclidean plane.
    """
    def __new__(cls):
        return super().__new__(cls)


class SyntheticGeometryCircularConfiguration(Basic):
    r"""Represents the free point configuration where all the free
    points are assumed to exist in an arbitrary circle with radius
    $\delta$.
    """
    def __new__(cls):
        return super().__new__(cls)
