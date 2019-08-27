from sympy.core.basic import Atom, Basic
from sympy.core.function import Application
from sympy.core.singleton import Singleton, S
from sympy.core.compatibility import with_metaclass
from sympy.core.sympify import sympify


class Ternary(Basic):
    pass


class TernaryAtom(Ternary, Atom):
    pass


class TernaryTrue(with_metaclass(Singleton, TernaryAtom)):
    def __bool__(self):
        return bool(True)

    __nonzero__ = __bool__

    def _hashable_content(self):
        return (True,)

    def _eval_ternary_not(self):
        return S.TernaryFalse

    _eval_ternary_nti = _eval_ternary_not
    _eval_ternary_pti = _eval_ternary_not

    def _eval_ternary_increment(self):
        return S.TernaryFalse

    def _eval_ternary_decrement(self):
        return S.TernaryNone

    def _eval_ternary_clamp_up(self):
        return self

    def _eval_ternary_clamp_down(self):
        return S.TernaryNone


class TernaryFalse(with_metaclass(Singleton, TernaryAtom)):
    def __bool__(self):
        return bool(False)

    __nonzero__ = __bool__

    def _hashable_content(self):
        return (False,)

    def _eval_not(self):
        return TernaryTrue

    def _eval_ternary_not(self):
        return S.TernaryTrue

    _eval_ternary_nti = _eval_ternary_not
    _eval_ternary_pti = _eval_ternary_not

    def _eval_ternary_increment(self):
        return S.TernaryNone

    def _eval_ternary_decrement(self):
        return S.TernaryTrue

    def _eval_ternary_clamp_up(self):
        return S.TernaryNone

    def _eval_ternary_clamp_down(self):
        return self


class TernaryNone(with_metaclass(Singleton, TernaryAtom)):
    def __bool__(self):
        return bool(None)

    __nonzero__ = __bool__

    def _hashable_content(self):
        return (None,)

    def _eval_ternary_not(self):
        return self

    def _eval_ternary_nti(self):
        return S.TernaryFalse

    def _eval_ternary_pti(self):
        return S.TernaryTrue

    def _eval_ternary_increment(self):
        return S.TernaryTrue

    def _eval_ternary_decrement(self):
        return S.TernaryFalse

    def _eval_ternary_clamp_up(self):
        return self

    def _eval_ternary_clamp_down(self):
        return self


S.TernaryTrue = TernaryTrue()
S.TernaryFalse = TernaryFalse()
S.TernaryNone = TernaryNone()


class TernaryFunction(Application, Ternary):
    pass


class TernaryNot(TernaryFunction):
    @classmethod
    def eval(cls, x):
        x = sympify(x)
        if isinstance(x, Ternary):
            return x._eval_ternary_not()
        raise ValueError()


class TernaryNTI(TernaryFunction):
    @classmethod
    def eval(cls, x):
        x = sympify(x)
        if isinstance(x, Ternary):
            return x._eval_ternary_nti()
        raise ValueError()


class TernaryPTI(TernaryFunction):
    @classmethod
    def eval(cls, x):
        x = sympify(x)
        if isinstance(x, Ternary):
            return x._eval_ternary_pti()
        raise ValueError()


class TernaryIncrement(TernaryFunction):
    @classmethod
    def eval(cls, x):
        x = sympify(x)
        if isinstance(x, Ternary):
            return x._eval_ternary_increment()
        raise ValueError()


class TernaryDecrement(TernaryFunction):
    @classmethod
    def eval(cls, x):
        x = sympify(x)
        if isinstance(x, Ternary):
            return x._eval_ternary_decrement()
        raise ValueError()


class TernaryClampUp(TernaryFunction):
    @classmethod
    def eval(cls, x):
        x = sympify(x)
        if isinstance(x, Ternary):
            return x._eval_ternary_clamp_up()
        raise ValueError()


class TernaryClampDown(TernaryFunction):
    @classmethod
    def eval(cls, x):
        x = sympify(x)
        if isinstance(x, Ternary):
            return x._eval_ternary_clamp_down()
        raise ValueError()


class TernaryMin(TernaryFunction):
    @classmethod
    def eval(cls, a, b):
        a, b = sympify(a), sympify(b)
        if not isinstance(a, Ternary) or not isinstance(b, Ternary):
            raise ValueError()

        if a == S.TernaryFalse or b == S.TernaryFalse:
            return S.TernaryFalse
        elif a == S.TernaryNone or b == S.TernaryNone:
            return S.TernaryNone
        return S.TernaryTrue


class TernaryMax(TernaryFunction):
    @classmethod
    def eval(cls, a, b):
        a, b = sympify(a), sympify(b)
        if not isinstance(a, Ternary) or not isinstance(b, Ternary):
            raise ValueError()

        if a == S.TernaryTrue or b == S.TernaryTrue:
            return S.TernaryTrue
        elif a == S.TernaryNone or b == S.TernaryNone:
            return S.TernaryNone
        return S.TernaryFalse


class TernaryAntiMin(TernaryFunction):
    @classmethod
    def eval(cls, a, b):
        a, b = sympify(a), sympify(b)
        if not isinstance(a, Ternary) or not isinstance(b, Ternary):
            raise ValueError()

        if a == S.TernaryFalse or b == S.TernaryFalse:
            return S.TernaryTrue
        elif a == S.TernaryNone or b == S.TernaryNone:
            return S.TernaryNone
        return S.TernaryFalse


class TernaryAntiMax(TernaryFunction):
    @classmethod
    def eval(cls, a, b):
        a, b = sympify(a), sympify(b)
        if not isinstance(a, Ternary) or not isinstance(b, Ternary):
            raise ValueError()

        if a == S.TernaryTrue or b == S.TernaryTrue:
            return S.TernaryFalse
        elif a == S.TernaryNone or b == S.TernaryNone:
            return S.TernaryNone
        return S.TernaryTrue


class TernaryXor(TernaryFunction):
    @classmethod
    def eval(cls, a, b):
        a, b = sympify(a), sympify(b)
        if not isinstance(a, Ternary) or not isinstance(b, Ternary):
            raise ValueError()

        if a == S.TernaryTrue and b == S.TernaryTrue or\
            a == S.TernaryFalse and b == S.TernaryFalse:
            return S.TernaryFalse
        elif a == S.TernaryTrue and b == S.TernaryFalse or\
            a == S.TernaryFalse and b == S.TernaryTrue:
            return S.TernaryTrue
        return S.TernaryNone


class TernaryConsensus(TernaryFunction):
    @classmethod
    def eval(cls, a, b):
        a, b = sympify(a), sympify(b)
        if not isinstance(a, Ternary) or not isinstance(b, Ternary):
            raise ValueError()

        if a == S.TernaryTrue and b == S.TernaryTrue:
            return S.TernaryTrue
        elif a == S.TernaryFalse and b == S.TernaryFalse:
            return S.TernaryFalse
        return S.TernaryNone


class TernaryAnything(TernaryFunction):
    @classmethod
    def eval(cls, a, b):
        a, b = sympify(a), sympify(b)
        if not isinstance(a, Ternary) or not isinstance(b, Ternary):
            raise ValueError()

        if a == S.TernaryTrue and b != S.TernaryFalse or \
            b == S.TernaryTrue and a != S.TernaryFalse:
            return S.TernaryTrue
        elif a == S.TernaryFalse and b != S.TernaryTrue or \
            b == S.TernaryFalse and a != S.TernaryTrue:
            return S.TernaryFalse
        return S.TernaryNone


class TernaryEquality(TernaryFunction):
    @classmethod
    def eval(cls, a, b):
        a, b = sympify(a), sympify(b)
        if not isinstance(a, Ternary) or not isinstance(b, Ternary):
            raise ValueError()

        if a == b:
            return TernaryTrue
        return S.TernaryFalse


class TernaryUnequality(TernaryFunction):
    @classmethod
    def eval(cls, a, b):
        a, b = sympify(a), sympify(b)
        if not isinstance(a, Ternary) or not isinstance(b, Ternary):
            raise ValueError()

        if a != b:
            return TernaryTrue
        return S.TernaryFalse
