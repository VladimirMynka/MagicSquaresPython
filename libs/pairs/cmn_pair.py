from dataclasses import dataclass

from ..int_variants.factorized_int_by_dict import FactorizedIntByDict
from .functionally_pair import FunctionallyPair
from .pair import T


@dataclass
class CmnPair(FunctionallyPair[T]):
    @property
    def mm_plus_nn(self) -> T:
        """Calculates sum of two squared components."""
        return self.m ** 2 + self.n ** 2

    def value(self) -> T:
        """Calculates (m^2 + n^2)^2."""
        return self.mm_plus_nn ** 2

    def factorize(self) -> FactorizedIntByDict:
        """Factorizes (m^2 + n^2)^2."""
        if isinstance(self.m, FactorizedIntByDict):
            return self.mm_plus_nn ** 2
        return FactorizedIntByDict.parse(self.mm_plus_nn)
