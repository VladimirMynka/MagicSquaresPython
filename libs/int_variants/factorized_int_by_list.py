import math
import operator
from functools import reduce
from typing import Self

from .factor_injection import FactorInjection
from .factorized_int_base import FactorizedIntBase
from .typing_schemas import Prime


class FactorizedIntByList(FactorizedIntBase):
    """
    A class representing an integer in its factorized form, using a list of prime factor powers.

    Args:
        powers (List[int]): A list of powers corresponding to the prime factors.
    """

    primes: list[Prime] = [2, 3, 5, 7, 11]

    def __init__(self, powers: list[int]):
        """
        Initializes a FactorizedInt instance with given prime powers.

        Args:
            powers (List[int]): A list of powers for the prime factors.
        """

        self.powers: list[int] = powers

    def normalize(self) -> Self:
        """Removes trailing zero powers in the factorization to keep the representation minimal."""
        while (len(self.powers) > 0) and self.powers[-1] == 0:
            del self.powers[-1]

        return self

    def to_list_of_injection(self) -> Self:
        """Transforms to list of FactorInjection."""
        return [FactorInjection(
            factor=self.primes[i],
            power=self.powers[i]
        ) for i in range(len(self.powers)) if self.powers[i] != 0]

    @classmethod
    def parse(cls, number: int) -> Self:
        """
        Creates a FactorizedInt from a given integer by calculating the prime powers.

        Args:
            number (int): The integer to be factorized.

        Returns:
            FactorizedIntByList: An instance representing the factorized form of the number.
        """
        max_prime = cls.primes[-1]

        if max_prime ** 2 < number:
            cls._extend_primes_to(math.isqrt(number) + 1)

        max_index = cls._find_max_divider_index(number)
        powers = [
            FactorInjection.calculate(number, cls.primes[i]).power
            for i in range(max_index + 1)
        ]
        return cls(powers).normalize()

    def __int__(self) -> int:
        """Returns the integer value of the factorized representation."""
        return reduce(operator.mul, [self.primes[i] ** self.powers[i] for i in range(len(self.powers))], 1)

    def __len__(self) -> int:
        return len([elem for elem in self.powers if elem != 0])

    def __mul__(self, other: Self | int) -> Self:
        """Returns the product of the factorized integer and another factorized integer or an integer."""
        shorter, longer = self._get_shorter_and_longer(other)

        n_short = len(shorter)
        return FactorizedIntByList(
            [a + b for a, b in zip(shorter, longer[:n_short])] + longer[n_short:]
        )

    def __floordiv__(self, other: Self | int) -> Self:
        """Returns the division of the factorized integer and another factorized integer or an integer."""
        other = other if isinstance(other, FactorizedIntByList) else FactorizedIntByList.parse(other)
        n_short = min(len(other.powers), len(self.powers))

        if len(self.powers) == n_short:
            main = [a - b for a, b in zip(self.powers, other.powers[:n_short])]
            remainder = [-b for b in other.powers[n_short:]]
        else:
            main = [a - b for a, b in zip(self.powers[:n_short], other.powers)]
            remainder = self.powers[n_short:]

        return FactorizedIntByList(main + remainder)

    def __and__(self, other: Self | int) -> Self:
        """Returns the GCD of the factorized integer and another factorized integer or an integer."""
        shorter, longer = self._get_shorter_and_longer(other)

        n_short = len(shorter)

        return FactorizedIntByList([min(a, b) for a, b in zip(shorter, longer[:n_short])]).normalize()

    def __or__(self, other: Self | int) -> Self:
        """Returns the LCM of the factorized integer and another factorized integer or an integer."""
        shorter, longer = self._get_shorter_and_longer(other)

        n_short = len(shorter)
        return FactorizedIntByList(
            [max(a, b) for a, b in zip(shorter, longer[:n_short])] + longer[n_short:]
        )

    def __pow__(self, power, modulo=None) -> Self:
        """
        Info:
            Raises the factorized integer to a power, optionally using modular arithmetic.

        Args:
            power (int): The exponent to raise to.
            modulo (int, optional): The modulus for modular exponentiation.

        Returns:
            FactorizedIntByList: The result of exponentiation.
        """
        # TODO: сделать умножение по модулю
        if modulo is None:
            return FactorizedIntByList([elem * power for elem in self.powers])
        raise NotImplementedError()

    def _get_shorter_and_longer(self, other) -> (list[int], list[int]):
        """
        Determines which of the two FactorizedInt instances has more powers.

        Args:
            other (Union[FactorizedInt, int]): Another FactorizedInt instance or an integer.

        Returns:
            (List[int], List[int]): A tuple with the shorter and longer powers lists.
        """
        if not isinstance(other, FactorizedIntByList):
            other = FactorizedIntByList.parse(other)
        if len(other.powers) > len(self.powers):
            return self.powers, other.powers
        else:
            return other.powers, self.powers
