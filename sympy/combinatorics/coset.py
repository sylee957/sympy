from __future__ import print_function, division

from sympy.core.sympify import _sympify
from sympy.core.logic import fuzzy_bool
from sympy.core.relational import Eq
from sympy.sets.sets import Set, FiniteSet

from .perm_groups import PermutationGroup
from .permutations import Permutation


class CosetBase(Set):
    def __new__(cls, elem, subgroup, group, **kwargs):
        subgroup, elem = _sympify(subgroup), _sympify(elem)
        group = _sympify(group)

        if not subgroup.is_subgroup(group):
            raise ValueError(
                '{} is not a subgroup of {}.'.format(subgroup, group))

        if not group.contains(elem):
            raise ValueError(
                "{} is not an element of {}.".format(elem, group))

        return super(CosetBase, cls).__new__(cls, elem, subgroup, group)


    def __iter__(self):
        g, H, _ = self.args
        for elem in H.generate():
            yield g * elem


    def __len__(self):
        _, H, _ = self.args
        return H.order()


    def _eval_rewrite_as_FiniteSet(self, *args, **kwargs):
        return FiniteSet(*self)


    def _contains(self, x):
        g, H, _ = self.args

        any_none = False
        for elem in H.generate():
            truth = fuzzy_bool(Eq(x, g * elem))
            if truth:
                return True
            elif truth == None:
                any_none = True

        if any_none:
            return None
        return False


class LeftCoset(CosetBase):
    def __iter__(self):
        g, H, _ = self.args
        for elem in H.generate():
            yield g * elem


    def _contains(self, x):
        g, H, _ = self.args

        any_none = False
        for elem in H.generate():
            truth = fuzzy_bool(Eq(x, g * elem))
            if truth:
                return True
            elif truth == None:
                any_none = True

        if any_none:
            return None
        return False


class RightCoset(CosetBase):
    def __iter__(self):
        g, H, _ = self.args
        for elem in H.generate():
            yield elem * g


    def _contains(self, x):
        g, H, _ = self.args

        any_none = False
        for elem in H.generate():
            truth = fuzzy_bool(Eq(x, elem * g))
            if truth:
                return True
            elif truth == None:
                any_none = True

        if any_none:
            return None
        return False
