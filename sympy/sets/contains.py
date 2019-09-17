from __future__ import print_function, division

from sympy.core import S
from sympy.core.relational import Eq, Ne
from sympy.logic.boolalg import BooleanFunction, And, Or
from sympy.utilities.misc import func_name

class Contains(BooleanFunction):
    """
    Asserts that x is an element of the set S

    Examples
    ========

    >>> from sympy import Symbol, Integer, S
    >>> from sympy.sets.contains import Contains
    >>> Contains(Integer(2), S.Integers)
    True
    >>> Contains(Integer(-2), S.Naturals)
    False
    >>> i = Symbol('i', integer=True)
    >>> Contains(i, S.Naturals)
    Contains(i, Naturals)

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Element_%28mathematics%29
    """
    @classmethod
    def eval(cls, x, s):
        from .sets import Set

        if not isinstance(s, Set):
            raise TypeError('expecting Set, not %s' % func_name(s))

        ret = s.contains(x)
        if not isinstance(ret, Contains) and (
                ret in (S.true, S.false) or isinstance(ret, Set)):
            return ret

    @property
    def binary_symbols(self):
        return set().union(*[i.binary_symbols
            for i in self.args[1].args
            if i.is_Boolean or i.is_Symbol or
            isinstance(i, (Eq, Ne))])

    def as_set(self):
        raise NotImplementedError()


class IsSubsetOfBase(BooleanFunction):
    def as_set(self):
        raise NotImplementedError


class IsSubsetOf(IsSubsetOfBase):
    r"""If `A` is a subset of `B` denoted by `A \subseteq B`.

    Parameters
    ==========

    A, B : Set, Set
        The SymPy set objects to test subset relationals upon.

    evaluate : bool, optional
        If ``False``, it will not attempt any computation and will
        remain in an unevaluated form, which is often useful for
        notational purposes.

        Default is ``True``.
    """
    @classmethod
    def eval(cls, A, B):
        from .sets import tfn, Set

        if not isinstance(A, Set):
            raise TypeError('{} must be a set.' % A)
        if not isinstance(B, Set):
            raise TypeError('{} must be a set.' % B)

        ret = A.is_subset(B)
        ret = tfn[ret]
        if not isinstance(ret, cls) and ret in (S.true, S.false):
            return ret


class IsSupersetOf(IsSubsetOfBase):
    r"""If `A` is a superset of `B` denoted by `A \supseteq B`.

    Parameters
    ==========

    A, B : Set, Set
        The SymPy set objects to test subset relationals upon.

    evaluate : bool, optional
        If ``False``, it will not attempt any computation and will
        remain in an unevaluated form, which is often useful for
        notational purposes.

        If ``True``, it will try to canonicalize this relational as
        `B \subseteq A`.

        Default is ``True``.
    """
    @classmethod
    def eval(cls, A, B):
        return IsSubsetOf(B, A)


class IsProperSubsetOf(IsSubsetOfBase):
    r"""If `A` is a proper subset of `B` denoted by `A \subsetneq B`.

    Parameters
    ==========

    A, B : Set, Set
        The SymPy set objects to test subset relationals upon.

    evaluate : bool, optional
        If ``False``, it will not attempt any computation and will
        remain in an unevaluated form, which is often useful for
        notational purposes.

        If ``True``, it will try to canonicalize this relational as
        `(A \subseteq B) \wedge (A \neq B)`.

        Default is ``True``.
    """
    @classmethod
    def eval(cls, A, B):
        return And(IsSubsetOf(A, B), Ne(A, B))


class IsProperSupersetOf(IsSubsetOfBase):
    r"""If `A` is a proper superset of `B` denoted by `A \supsetneq B`.

    Parameters
    ==========

    A, B : Set, Set
        The SymPy set objects to test subset relationals upon.

    evaluate : bool, optional
        If ``False``, it will not attempt any computation and will
        remain in an unevaluated form, which is often useful for
        notational purposes.

        If ``True``, it will try to canonicalize this relational as
        `(B \subseteq A) \wedge (A \neq B)`.

        Default is ``True``.
    """
    @classmethod
    def eval(cls, A, B):
        return And(IsSupersetOf(A, B), Ne(A, B))


class IsNonEmptySubsetOf(IsSubsetOfBase):
    r"""If `A` is a non-empty subset of `B` denoted by
    `\varnothing \subsetneq A \subseteq B`.

    Parameters
    ==========

    A, B : Set, Set
        The SymPy set objects to test subset relationals upon.

    evaluate : bool, optional
        If ``False``, it will not attempt any computation and will
        remain in an unevaluated form, which is often useful for
        notational purposes.

        If ``True``, it will try to canonicalize this relational as
        `(A \subseteq B) \wedge (A \neq \varnothing)`.

        Default is ``True``.
    """
    @classmethod
    def eval(cls, A, B):
        return And(IsSubsetOf(A, B), Ne(A, S.EmptySet))


class IsNonEmptyProperSubsetOf(IsSubsetOfBase):
    r"""If `A` is a non-empty proper subset of `B` denoted by
    `\varnothing \subsetneq A \subsetneq B`.

    Parameters
    ==========

    A, B : Set, Set
        The SymPy set objects to test subset relationals upon.

    evaluate : bool, optional
        If ``False``, it will not attempt any computation and will
        remain in an unevaluated form, which is often useful for
        notational purposes.

        If ``True``, it will try to canonicalize this relational as
        `(A \subseteq B) \wedge (A \neq \varnothing) \wedge (A \neq B)`.

        Default is ``True``.
    """
    @classmethod
    def eval(cls, A, B):
        return And(IsSubsetOf(A, B), Ne(A, S.EmptySet), Ne(A, B))
