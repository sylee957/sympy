from __future__ import print_function, division

from sympy.core.basic import Basic
from sympy.core.singleton import S
from sympy.functions import ceiling, log, conjugate


class CayleyDicksonConstruct(Basic):
    def __new__(cls, *args, evaluate=True):
        exp = log(len(args), 2)
        C = CayleyDicksonConstruct
        if not exp.is_integer or exp == 0:
            new_args = args + (S.Zero,) * (2**ceiling(exp) - len(args))
            return C(*new_args)

        if len(args) > 2:
            a = args[:len(args)//2]
            b = args[len(args)//2:]
            return C(C(*a), C(*b))

        a, b = args
        obj = Basic.__new__(cls, a, b)
        return obj

    def flatten(self):
        C = CayleyDicksonConstruct
        a, b = self.a, self.b
        if isinstance(a, C) and isinstance(b, C):
            return a.flatten() + b.flatten()
        return a, b

    @property
    def a(self):
        return self.args[0]

    @property
    def b(self):
        return self.args[1]

    def __add__(self, other):
        a, b = self.a, self.b
        c, d = other.a, other.b
        return self.func(a+c, b+d)

    def __sub__(self, other):
        a, b = self.a, self.b
        c, d = other.a, other.b
        return self.func(a-c, b-d)

    def __neg__(self):
        a, b = self.a, self.b
        return self.func(-a, -b)

    def __mul__(self, other):
        a, b = self.a, self.b
        c, d = other.a, other.b

        new_a = a*c - conjugate(d)*b
        new_b = d*a + b*conjugate(c)
        return self.func(new_a, new_b)

    def _eval_conjugate(self):
        a, b = self.a, self.b
        return self.func(conjugate(a), -b)
