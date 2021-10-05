from sympy.core.expr import Expr
from sympy.core.sympify import _sympify
from sympy.core.compatibility import default_sort_key
from sympy.core.singleton import S



class SyntheticGeometryTwolineAlpha(Expr):
    """Signed length of two parallel lines"""
    def __new__(cls):
        return super().__new__(cls,)

    def _eval_is_real(self):
        return True


class SyntheticGeometryTwolineBeta(Expr):
    """$\sin\angle(l1, l2)$ of two nonparallel lines"""
    def __new__(cls):
        return super().__new__(cls)

    def _eval_is_real(self):
        return True
