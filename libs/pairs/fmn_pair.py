import math
import operator
from dataclasses import dataclass
from functools import reduce
from typing import Self

from ..int_variants.factorized_int_by_dict import FactorizedIntByDict
from .cmn_pair import CmnPair
from .functionally_pair import FunctionallyPair
from .pair import T


@dataclass
class FmnPair(FunctionallyPair[T]):
    @property
    def m_plus_n(self) -> T:
        """Calculates the sum of m and n."""
        return self.m + self.n

    @property
    def m_minus_n(self) -> T:
        """Calculates the difference between m and n."""
        return self.m - self.n

    def value(self) -> T:
        return self.m * self.n * self.m_minus_n * self.m_plus_n

    def factorize(self) -> FactorizedIntByDict:
        return reduce(operator.mul, [FactorizedIntByDict.parse(elem) for elem in [
            self.m,
            self.n,
            self.m_plus_n,
            self.m_minus_n,
        ]])

    def R2(self) -> Self:
        """Transforms the pair to a new pair defined by m_plus_n and m_minus_n.

        Returns:
            Self: A new instance of Pair with m_plus_n and m_minus_n as its values.
        """
        return self.__class__(self.m_plus_n, self.m_minus_n)

    def R_half(self) -> Self:
        """Transforms the pair to a new pair defined by half the sum and half the difference.

        Returns:
            Self: A new instance of Pair with half the values of m_plus_n and m_minus_n.
        """
        return self.__class__(self.m_plus_n // 2, self.m_minus_n // 2)

    def F1(self) -> Self:
        """Transforms the pair to a new pair where m is doubled and n is the sum of m and n.

        Returns:
            Self: A new instance of Pair with modified values based on the transformation.
        """
        return self.__class__(2 * self.m, self.m + self.n)

    def F2(self) -> Self:
        """Transforms the pair to a new pair where m is doubled and n is the difference of m and n.

        Returns:
            Self: A new instance of Pair with modified values based on the transformation.
        """
        return self.__class__(2 * self.m, self.m - self.n)

    def F7(self) -> Self:
        m, n = self.m, self.n
        return self.__class__(CmnPair(m, n).value(), 4 * FmnPair(m, n).value())

    def simplify(self) -> Self:
        """Simplifies the pair to an equal odd-even pair by reducing it using gcd.

        Returns:
            Self: A simplified instance of Pair where the values are adjusted based on gcd.
        """
        gcd = math.gcd(self.m, self.n)
        m, n = abs(self.m // gcd), abs(self.n // gcd)
        m, n = max(m, n), min(m, n)
        if m % 2 == n % 2:
            return self.__class__(m, n).R_half()
        return self.__class__(m, n)

    def is_simplified(self) -> bool:
        """Checks if the pair is in its simplified form.

        A pair is considered simplified if:
        - m > n > 0
        - m and n have opposite parity (one is even, the other is odd)
        - the greatest common divisor (gcd) of m and n is 1

        Returns:
            bool: True if the pair is simplified, False otherwise.
        """
        m, n = self.m, self.n
        return (m > n > 0) and (m % 2 != n % 2) and (math.gcd(m, n) == 1)
