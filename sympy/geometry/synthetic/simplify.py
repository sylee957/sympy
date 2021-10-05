from sympy.polys.polytools import cancel
from sympy.core.relational import Eq, Ne


def _cancel(objective):
    if isinstance(objective, (Eq, Ne)):
        return objective.func(cancel(objective.lhs), cancel(objective.rhs))
    return cancel(objective)
