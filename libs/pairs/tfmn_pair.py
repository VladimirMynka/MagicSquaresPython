import operator
from dataclasses import dataclass
from functools import reduce

from ..int_variants.factorized_int_by_dict import FactorizedIntByDict
from .fmn_pair import FmnPair
from .pair import T


@dataclass
class TfmnPair(FmnPair[T]):
    def value(self) -> T:
        return self.m * self.n * self.m_minus_n * self.m_plus_n


    def factorize(self) -> FactorizedIntByDict:
        """Factorizes m * n * (m - n) * (m + n) using reduce and collection."""
        factors = [self.m, self.n, self.m_minus_n, self.m_plus_n]
        
        factorized_factors = [
            FactorizedIntByDict.parse(factor) if not isinstance(factor, FactorizedIntByDict) else factor
            for factor in factors
        ]

        return reduce(operator.mul, factorized_factors)
        
        
    @classmethod
    def t(cls, n: T) -> T:
        """Calculates n divided by most square."""
        if isinstance(n, FactorizedIntByDict):
            return n.apply(lambda x: x % 2)
        return int(FactorizedIntByDict.parse(n).apply(lambda x: x % 2))

