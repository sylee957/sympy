from __future__ import print_function, division

from sympy.core.basic import Atom
from sympy.matrices import ImmutableDenseMatrix


class GroupMultiplicationTable(Atom):
    def __new__(cls, data, rows=None, cols=None):
        cls._data = data
        cls._rows = rows
        cls._cols = cols
        return Atom.__new__(cls)

    @property
    def rows(self):
        return self._rows

    @property
    def cols(self):
        return self._cols

    @property
    def data(self):
        return self._data


def group_multiplication_table(group, rows=None, cols=None):
    rows = ImmutableDenseMatrix([*group.generate()])
    cols = ImmutableDenseMatrix([*group.generate()])
    data = ImmutableDenseMatrix(
        len(rows), len(cols), lambda i, j: rows[i]*cols[j])

    return GroupMultiplicationTable(data, rows=rows, cols=cols)
