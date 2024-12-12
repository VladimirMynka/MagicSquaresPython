from dataclasses import dataclass
from typing import Generic, Self, TypeAlias, TypeVar

from ..int_variants.factorized_int_base import FactorizedIntBase

IntNumber: TypeAlias = int | FactorizedIntBase
T = TypeVar('T', bound=IntNumber)


@dataclass
class Pair(Generic[T]):
    m: T
    n: T

    def __eq__(self, other: Self) -> bool:
        """Checks two pairs is equal or not."""
        return (self.m == other.m) and (self.n == other.n)
