"""Predefined R^n manifolds together with common coord. systems.

Coordinate systems are predefined as well as the transformation laws between
them.

Coordinate functions can be accessed as attributes of the manifold (eg `R2.x`),
as attributes of the coordinate systems (eg `R2_r.x` and `R2_p.theta`), or by
using the usual `coord_sys.coord_function(index, name)` interface.
"""

from typing import Any

from .diffgeom import Manifold, Patch, CoordSystem
from sympy.core.symbol import Dummy, symbols
from sympy.matrices import Matrix
from sympy import sqrt, atan2, acos, sin, cos, Lambda

__all__ = [
    'R2', 'R2_origin', 'R2_r', 'R2_p',
    'R3', 'R3_origin', 'R3_r', 'R3_c', 'R3_s'
]

x, y = symbols('x y', cls=Dummy)
r, t = symbols('rho theta', cls=Dummy)

###############################################################################
# R2
###############################################################################
R2 = Manifold('R^2', 2)  # type: Any
# Patch and coordinate systems.
R2_origin = Patch('origin', R2)  # type: Any
R2_r = CoordSystem('rectangular', R2_origin, ['x', 'y'])  # type: Any
R2_p = CoordSystem('polar', R2_origin, ['r', 'theta'])  # type: Any

transforms_2d = {
    (R2_r, R2_p): Lambda((x, y), Matrix([sqrt(x**2 + y**2), atan2(y, x)])),
    (R2_p, R2_r): Lambda((r, t), Matrix([r*cos(t), r*sin(t)])),
}

# Defining the basis coordinate functions and adding shortcuts for them to the
# manifold and the patch.
R2.x, R2.y = R2_origin.x, R2_origin.y = R2_r.x, R2_r.y = R2_r.coord_functions()
R2.r, R2.theta = R2_origin.r, R2_origin.theta = R2_p.r, R2_p.theta = R2_p.coord_functions()

# Defining the basis vector fields and adding shortcuts for them to the
# manifold and the patch.
R2.e_x, R2.e_y = R2_origin.e_x, R2_origin.e_y = R2_r.e_x, R2_r.e_y = R2_r.base_vectors()
R2.e_r, R2.e_theta = R2_origin.e_r, R2_origin.e_theta = R2_p.e_r, R2_p.e_theta = R2_p.base_vectors()

# Defining the basis oneform fields and adding shortcuts for them to the
# manifold and the patch.
R2.dx, R2.dy = R2_origin.dx, R2_origin.dy = R2_r.dx, R2_r.dy = R2_r.base_oneforms()
R2.dr, R2.dtheta = R2_origin.dr, R2_origin.dtheta = R2_p.dr, R2_p.dtheta = R2_p.base_oneforms()

###############################################################################
# R3
###############################################################################
R3 = Manifold('R^3', 3)  # type: Any
# Patch and coordinate systems.
R3_origin = Patch('origin', R3)  # type: Any
R3_r = CoordSystem('rectangular', R3_origin, ['x', 'y', 'z'])  # type: Any
R3_c = CoordSystem('cylindrical', R3_origin, ['rho', 'psi', 'z'],)  # type: Any
R3_s = CoordSystem('spherical', R3_origin, ['r', 'theta', 'phi'],)  # type: Any

x, y, z = symbols('x y z', cls=Dummy)
r, t, p = symbols('rho theta phi', cls=Dummy)

transforms_3d = {
    (R3_r, R3_c):
        Lambda((x, y, z), Matrix([sqrt(x**2 + y**2), atan2(y, x), z])),
    (R3_c, R3_r):
        Lambda((r, p, z), Matrix([r*cos(p), r*sin(p), z])),
    (R3_r, R3_s):
        Lambda(
            (x, y, z),
            Matrix([
                sqrt(x**2 + y**2 + z**2),
                acos(z/sqrt(x**2 + y**2 + z**2)),
                atan2(y, x)])
        ),
    (R3_s, R3_r):
        Lambda(
            (r, t, p),
            Matrix([r*sin(t)*cos(p), r*sin(t)*sin(p), r*cos(t)])
        ),
    (R3_c, R3_s):
        Lambda(
            (r, p, z),
            Matrix([sqrt(r**2 + z**2), acos(z/sqrt(r**2 + z**2)), p])
        ),
    (R3_s, R3_c):
        Lambda((r, t, p), Matrix([r*sin(t), p, r*cos(t)])),
}

# Defining the basis coordinate functions.
R3_r.x, R3_r.y, R3_r.z = R3_r.coord_functions()
R3_c.rho, R3_c.psi, R3_c.z = R3_c.coord_functions()
R3_s.r, R3_s.theta, R3_s.phi = R3_s.coord_functions()

# Defining the basis vector fields.
R3_r.e_x, R3_r.e_y, R3_r.e_z = R3_r.base_vectors()
R3_c.e_rho, R3_c.e_psi, R3_c.e_z = R3_c.base_vectors()
R3_s.e_r, R3_s.e_theta, R3_s.e_phi = R3_s.base_vectors()

# Defining the basis oneform fields.
R3_r.dx, R3_r.dy, R3_r.dz = R3_r.base_oneforms()
R3_c.drho, R3_c.dpsi, R3_c.dz = R3_c.base_oneforms()
R3_s.dr, R3_s.dtheta, R3_s.dphi = R3_s.base_oneforms()
