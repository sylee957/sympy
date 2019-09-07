from sympy.core.containers import Tuple
from sympy.core.sympify import _sympify


class NTuple(Basic):
    def __new__(cls, length, offset, *args, **kwargs):

