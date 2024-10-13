from abc import abstractmethod
from dataclasses import dataclass

from ..int_variants.factorized_int_by_dict import FactorizedIntByDict
from .pair import Pair, T


@dataclass
class FunctionallyPair(Pair[T]):
    @abstractmethod
    def value(self) -> T:
        """Apply function to pair: (N, N) -> N."""

    @abstractmethod
    def factorize(self) -> FactorizedIntByDict:
        """Get factorized value."""
