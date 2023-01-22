"""Tools for direct construction of trigonometric expansion terms from the
additive list of arguments
"""
from __future__ import annotations
from typing import Iterator, TypeVar, Callable, Generic, final
from dataclasses import dataclass


T = TypeVar('T')


@final
@dataclass(frozen=True)
class TrigExpandOptions(Generic[T]):
    cos: Callable[[T], T]
    sin: Callable[[T], T]
    cosh: Callable[[T], T]
    sinh: Callable[[T], T]


def sin_add(
    first: tuple[int, T], *others: tuple[int, T],
    options: TrigExpandOptions[T]
) -> Iterator[tuple[int, tuple[T, ...]]]:
    r"""Expand $\sin$ for additive list of signed arguments"""
    if not others:
        sign, arg = first
        if not sign % 2:
            yield sign, (options.sin(arg),)
        else:
            yield sign, (options.sinh(arg),)
        return None

    for sign, out_first in cos_add(first, options=options):
        for _sign, out_others in sin_add(*others, options=options):
            yield (sign + _sign) % 4, (*out_first, *out_others)

    for sign, out_first in sin_add(first, options=options):
        for _sign, out_others in cos_add(*others, options=options):
            yield (sign + _sign) % 4, (*out_first, *out_others)


def cos_add(
    first: tuple[int, T], *others: tuple[int, T],
    options: TrigExpandOptions[T]
) -> Iterator[tuple[int, tuple[T, ...]]]:
    r"""Expand $\cos$ for additive list of signed arguments"""
    if not others:
        sign, arg = first
        if not sign % 2:
            yield 0, (options.cos(arg),)
        else:
            yield 0, (options.cosh(arg),)
        return None

    for sign, out_first in cos_add(first, options=options):
        for _sign, out_others in cos_add(*others, options=options):
            yield (sign + _sign) % 4, (*out_first, *out_others)

    for sign, out_first in sin_add(first, options=options):
        for _sign, out_others in sin_add(*others, options=options):
            yield (sign + _sign + 2) % 4, (*out_first, *out_others)


def sinh_add(
    first: tuple[int, T], *others: tuple[int, T],
    options: TrigExpandOptions[T]
) -> Iterator[tuple[int, tuple[T, ...]]]:
    r"""Expand $\sinh$ for additive list of signed arguments"""
    if not others:
        sign, arg = first
        if not sign % 2:
            yield sign, (options.sinh(arg),)
        else:
            yield sign, (options.sin(arg),)
        return None

    for sign, out_first in cosh_add(first, options=options):
        for _sign, out_others in sinh_add(*others, options=options):
            yield (sign + _sign) % 4, (*out_first, *out_others)

    for sign, out_first in sinh_add(first, options=options):
        for _sign, out_others in cosh_add(*others, options=options):
            yield (sign + _sign) % 4, (*out_first, *out_others)


def cosh_add(
    first: tuple[int, T], *others: tuple[int, T],
    options: TrigExpandOptions[T]
) -> Iterator[tuple[int, tuple[T, ...]]]:
    r"""Expand $\cosh$ for additive list of signed arguments"""
    if not others:
        sign, arg = first
        if not sign % 2:
            yield 0, (options.cosh(arg),)
        else:
            yield 0, (options.cos(arg),)
        return None

    for sign, out_first in cosh_add(first, options=options):
        for _sign, out_others in cosh_add(*others, options=options):
            yield (sign + _sign) % 4, (*out_first, *out_others)

    for sign, out_first in sinh_add(first, options=options):
        for _sign, out_others in sinh_add(*others, options=options):
            yield (sign + _sign) % 4, (*out_first, *out_others)
