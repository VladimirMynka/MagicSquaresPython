import math
from abc import abstractmethod
from bisect import bisect_right
from typing import Self, Generator, Callable

from .factor_injection import FactorInjection
from .typing_schemas import Prime


class FactorizedIntBase:
    """
    A base class for different factorize int classes.
    """

    primes: list[Prime] = [2, 3, 5, 7, 11]

    @abstractmethod
    def normalize(self) -> Self:
        """Removes zero powers in the factorization to keep the representation minimal."""

    @abstractmethod
    def to_list_of_injection(self) -> list[FactorInjection]:
        """Transforms to list of FactorInjection."""

    @classmethod
    @abstractmethod
    def parse(cls, number: int) -> Self:
        """
        Creates a class object from a given integer by calculating the prime powers.

        Args:
            number (int): The integer to be factorized.

        Returns:
            Self: The result of parsing.
        """

    @classmethod
    def _injections_generator(cls, number: int, min_index: int = 0) -> Generator[FactorInjection, None, None]:
        """Generator for extracting number dividers."""
        last_factor: FactorInjection

        max_index = cls._find_max_divider_index(number)

        min_index, last_factor = cls._search_first_prime_injection(number, min_index, max_index)
        while last_factor is not None:
            yield last_factor
            number //= last_factor.value
            max_index = cls._find_max_divider_index(number)
            min_index, last_factor = cls._search_first_prime_injection(number, min_index, max_index)

        if number > cls.primes[min_index]:
            cls._extend_to_divide(number)

            max_index = len(cls.primes) - 1
            min_index, last_factor = cls._search_first_prime_injection(number, min_index, max_index)
            while last_factor is not None:
                yield last_factor
                number //= last_factor.value
                max_index = cls._find_max_divider_index(number)
                min_index, last_factor = cls._search_first_prime_injection(number, min_index, max_index)

    @classmethod
    def _search_first_prime_injection(
        cls,
        number: int,
        min_prime_index: int,
        max_prime_index: int,
    ) -> (int, FactorInjection | None):
        """Finds first prime divider of number from primes[min_prime_index] to primes[max_prime_index]"""
        injections_generator = (
            (i, FactorInjection.calculate(number=number, factor=cls.primes[i]))
            for i in range(min_prime_index, max_prime_index + 1)
        )
        return next(((i, inj) for i, inj in injections_generator if inj.power != 0), (max_prime_index, None))

    @abstractmethod
    def __int__(self) -> int:
        """Returns the integer value of the factorized representation."""

    def __float__(self) -> float:
        """Returns the float representation of the factorized integer."""
        return float(int(self))

    def __str__(self) -> str:
        """Returns the string representation of the factorized integer."""
        if len(self) == 0:
            return '1'

        return '·'.join([str(injection) for injection in self.to_list_of_injection()])

    @abstractmethod
    def __len__(self) -> int:
        """Returns count of unique primes injections."""

    def __add__(self, other: Self | int) -> Self:
        """Returns the sum of the factorized integer and another factorized integer or an integer."""
        return self.__class__.parse(int(self) + int(other))

    def __sub__(self, other: Self | int) -> Self:
        """Returns the difference of the factorized integer and another factorized integer or an integer."""
        return self.__class__.parse(int(self) - int(other))

    def __mul__(self, other: Self | int) -> Self:
        """Returns the product of the factorized integer and another factorized integer or an integer."""
        if isinstance(other, int):
            other = self.__class__.parse(other)
        return self._mul(other)

    @abstractmethod
    def _mul(self, other: Self) -> Self:
        """Returns the product of the factorized integer and another factorized integer."""

    def __floordiv__(self, other: Self | int) -> Self:
        """Returns the division of the factorized integer and another factorized integer or an integer."""
        if isinstance(other, int):
            other = self.__class__.parse(other)
        return self._floordiv(other)

    @abstractmethod
    def _floordiv(self, other: Self) -> Self:
        """Returns the division of the factorized integer and another factorized integer."""

    def __and__(self, other: Self | int) -> Self:
        """Returns the GCD of the factorized integer and another factorized integer or an integer."""
        if isinstance(other, int):
            other = self.__class__.parse(other)
        return self._gcd(other)

    @abstractmethod
    def _gcd(self, other: Self) -> Self:
        """Returns the GCD of the factorized integer and another factorized integer."""

    def __or__(self, other: Self | int) -> Self:
        """Returns the LCM of the factorized integer and another factorized integer or an integer."""
        if isinstance(other, int):
            other = self.__class__.parse(other)
        return self._lcm(other)

    @abstractmethod
    def _lcm(self, other: Self | int) -> Self:
        """Returns the LCM of the factorized integer and another factorized integer."""

    @abstractmethod
    def apply(self, action: Callable) -> Self:
        """Applies given action for powers of each prime."""

    def __pow__(self, power, modulo=None) -> Self:
        """
        Info:
            Raises the factorized integer to a power, optionally using modular arithmetic.

        Args:
            power (int): The exponent to raise to.
            modulo (int, optional): The modulus for modular exponentiation.

        Returns:
            Self: The result of exponentiation.
        """
        if modulo is None:
            return self.apply(lambda current_power: current_power * power)
        raise NotImplementedError()

    @classmethod
    def _extend_primes_to(cls, infimum: int) -> None:
        """Extends the list of primes up to a given limit."""
        current_max_prime = cls.primes[-1]  # no 2!!!

        for number in range(current_max_prime + 2, infimum + 1, 2):
            max_diver = math.isqrt(number)
            max_i_divider_index = cls._find_max_divider_index(max_diver)
            if next(
                i
                for i, p in enumerate(cls.primes)
                if (number % p == 0) or (i == max_i_divider_index)
            ) == max_i_divider_index:
                cls.primes.append(number)

    @classmethod
    def _extend_to_divide(cls, dividing: int) -> None:
        current_max_prime = cls.primes[-1]  # no 2!!!
        try_to = math.isqrt(dividing)

        for number in range(current_max_prime + 2, try_to + 1, 2):
            max_diver = math.isqrt(number)
            max_i_divider_index = cls._find_max_divider_index(max_diver)

            if dividing % number == 0:
                cls.primes.append(number)
                inj = FactorInjection.calculate(dividing, number).value
                cls._extend_to_divide(dividing // inj)
                return

            result = next(
                i
                for i, p in enumerate(cls.primes)
                if (number % p == 0) or (i == max_i_divider_index)
            )
            if (result == max_i_divider_index) and (number % cls.primes[result] != 0):
                cls.primes.append(number)

        cls._extend_primes_to(dividing + 1)

    @classmethod
    def _find_max_divider_index(cls, number) -> int:
        """Finds the index of the largest prime that potentially divides the given number."""
        return min(bisect_right(cls.primes, math.isqrt(number) + 1), len(cls.primes) - 1)
