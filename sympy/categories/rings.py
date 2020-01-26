from sympy.core.basic import Basic
from sympy.core.logic import fuzzy_and
from sympy.core.singleton import S
from sympy.core.sympify import _sympify
from sympy.sets.sets import Set


class AlgebraicStructure(Basic):
    """A formal representation of an algebraic structure."""
    def __new__(cls, *args):
        return Basic.__new__(*args)

    def __contains__(self, a):
        raise NotImplementedError

    def __call__(self, a):
        if a in self:
            return AlgebraicStructureElement(self, a)


class AlgebraicStructureElement(Basic):
    """A formal representation of an algebraic structure."""
    pass


class Group(AlgebraicStructure):
    def __new__(cls, s, op):
        s = _sympify(s)
        op = _sympify(op)
        if not isinstance(s, Set):
            raise ValueError("{} must be a set".format(s))

        if not isinstance(op, AssocativeBinaryOperator):
            raise ValueError(
                "{} must be a associative binary operator".format(op))

        a, b = op.args[:2]
        c = op.codomain

        if not (a == s and b == s and c == s):
            raise ValueError(
                "The operator {} must have the domain and codomain
                "identical to the base set.".format(op))

        return Basic.__new__(cls, s, *ops)

    def base_set(self):
        return self.args[0]

    def _contains(self, a):
        return self.base_set._contains(a)

    def __contains__(self, a):
        a = _sympify(a)
        contains = self._contains(a)
        if contains is True:
            return True
        elif contains is False:
            return False
        raise ValueError

    def is_subgroup(self, other):
        other = _sympify(other)
        if not isinstance(other, Group):
            return False

    def one(self):
        raise NotImplementedError


class Ring(AlgebraicStructure):
    def __new__(cls, s, add, mul):
        pass


class BinaryOperator(Basic):
    """A formal representation of a binary operation

    Notes
    =====

    A binary operation can be defined as a function
    $f : A \times B \rightarrow U$
    """
    def __new__(cls, a, b, u=S.UniversalSet):
        if not isinstance(a, Set):
            raise ValueError('{} must be a set.'.format(a))
        if not isinstance(b, Set):
            raise ValueError('{} must be a set.'.format(b))
        if not isinstance(u, Set):
            raise ValueError('{} must be a set.'.format(u))

        return Basic.__new__(cls, a, b, u)

    def domain(self):
        return self.args[0] * self.args[1]

    def codomain(self):
        return self.args[1]

    def _check_domain(self, a, b):
        A, B = self.args[0], self.args[1]
        return fuzzy_and([A.contains(a), B.contains(b)])

    def __call__(self, a, b):
        a, b = _sympify(a), _sympify(b)
        if self._check_domain(a, b):
            return AppliedBinaryOperator._new(self, a, b)
        raise ValueError(
            "The operation with {}, {} is not defined for the operator."
            .format(a, b))


class AssociativeBinaryOperator(BinaryOperator):
    pass


class CommutativeBinaryOperator(BinaryOperator):
    pass


class IdempotentBinaryOperator(BinaryOperator):
    pass


class AppliedBinaryOperator(Basic):
    def __new__(cls, op, a, b):
        a, b, op = _sympify(a), _sympify(b), _sympify(op)

        A, B = op.args[0], op.args[1]
        if A.contains(a) == False or B.contains(b) == False:
            raise ValueError

        return cls._new(op, a, b)

    @classmethod
    def _new(cls, op, a, b):
        return Basic.__new__(cls, op, a, b)


class BinaryAddOperator(
    AssociativeBinaryOperator,
    CommutativeBinaryOperator):
    def __new__(cls, a, b, u=S.UniversalSet):
        return super(BinaryAddOperator, cls).__new__(cls, a, b, u)

    def __call__(self, a, b):
        from sympy.core.add import Add
        if self._check_domain(a, b):
            return Add(a, b)
        raise ValueError(
            "The operation with {}, {} is not defined for the operator."
            .format(a, b))


class BinaryMulOperator(
    AssociativeBinaryOperator,
    CommutativeBinaryOperator):
    def __new__(cls, a, b, u=S.UniversalSet):
        return super(BinaryMulOperator, cls).__new__(cls, a, b, u)

    def __call__(self, a, b):
        from sympy.core.mul import Mul
        if self._check_domain(a, b):
            return Mul(a, b)
        raise ValueError(
            "The operation with {}, {} is not defined for the operator."
            .format(a, b))
