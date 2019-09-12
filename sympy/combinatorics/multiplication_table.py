from __future__ import print_function, division

from sympy.core.basic import Atom, Basic
from sympy.core.containers import Dict
from sympy.matrices import ImmutableDenseMatrix

from .permutations import Permutation


class GroupMultiplicationTable(Atom):
    def __new__(cls, data, index=None, columns=None):
        cls._data = data
        cls._index = index
        cls._columns = columns

        index_mapping_dict = dict()
        for i, item in enumerate(index):
            index_mapping_dict[item] = i
        cls._index_mapping = Dict(index_mapping_dict)

        columns_mapping_dict = dict()
        for i, item in enumerate(columns):
            columns_mapping_dict[item] = i
        cls._columns_mapping = Dict(columns_mapping_dict)

        return Atom.__new__(cls)


    @property
    def index(self):
        return self._index


    @property
    def columns(self):
        return self._columns


    @property
    def data(self):
        return self._data


    def as_canonical(self):
        """Return the canonical Cayley multiplication table with sorted
        index and columns labels"""
        pass


    def is_associative(self):
        """Uses Light's associativity test to check if the
        multiplication table represents associtivity.
        """
        pass


    def transform(self, mapping):
        """Transforms the entries of a group multiplication table as
        given by the mapping.
        """
        new_rows = ImmutableDenseMatrix(
            [mapping[item] for item in self.index])
        new_cols = ImmutableDenseMatrix(
            [mapping[item] for item in self.columns])
        new_data = ImmutableDenseMatrix(
            self.data.rows, self.data.cols,
            [mapping[item] for item in self.data])

        return GroupMultiplicationTable(new_data, new_rows, new_cols)


    def regular_representation(self, left=True, mapping=None):
        """Returns an another isomorphic multiplication table from the
        given multiplication table.

        Parameters
        ==========

        left : bool, optional
            Controls whether to use a left regular representation or
            the right regular representation.

        mapping : dict, optional
            The current implementation of ``Permutation`` does not allow
            any cycles to have any non-integer values.
            So a mapping from group elements to a range of nonnegative
            integers should be explicitedly be provided for this
            representation to work
        """
        if not mapping:
            group_elements = self.index
            mapping = dict()
            for i, elem in enumerate(group_elements):
                mapping[elem] = i

        # Temporarily transform the entries of the multiplication table
        # into integers from 0
        transformed = self.transform(mapping)

        transformed_index = transformed.index
        transformed_columns = transformed.columns
        transformed_data = transformed.data

        regular_representation_mapping = dict()
        for i, item in enumerate(transformed_index):
            af_upper = Permutation(transformed_columns)
            af_lower = Permutation(transformed_data[i, :])
            regular_representation_mapping[item] = af_upper * af_lower

        return transformed.transform(regular_representation_mapping)


def group_multiplication_table(group, rows=None, cols=None):
    """Returns the cayley table from the given permutation group.
    """
    rows = ImmutableDenseMatrix([*group.generate()])
    cols = ImmutableDenseMatrix([*group.generate()])
    data = ImmutableDenseMatrix(
        len(rows), len(cols), lambda i, j: rows[i]*cols[j])

    return GroupMultiplicationTable(data, index=rows, columns=cols)
