import operator
from functools import reduce
from typing import Self, Callable

from .factor_injection import FactorInjection
from .factorized_int_base import FactorizedIntBase
from .typing_schemas import Prime, PrimesWithOtherSets


class FactorizedIntByDict(FactorizedIntBase):
    """
    A class representing an integer in its factorized form, using a list of FactorInjection.
    """
    def __init__(self, injections: dict[Prime, int]):
        """
        Initializes a FactorizedInt instance with given prime powers.

        Args:
            injections (List[FactorInjection]): A list of injections for the prime factors.
        """

        self.injections: dict[Prime, int] = injections

    def normalize(self) -> Self:
        """Removes zero injections to keep the representation minimal."""
        for prime in list(self.injections.keys()):
            if self.injections[prime] == 0:
                del self.injections[prime]

        return self

    def to_list_of_injection(self) -> list[FactorInjection]:
        """Transforms to list of FactorInjection."""
        return [FactorInjection(key, value) for key, value in sorted(self.injections.items(), key=lambda pair: pair[0])]

    @classmethod
    def parse(cls, number: int) -> Self:
        """
        Creates a FactorizedIntByInjections from a given integer by calculating the prime powers.

        Args:
            number (int): The integer to be factorized.

        Returns:
            FactorizedIntByDict: An instance representing the factorized form of the number.
        """
        powers = {inj.factor: inj.power for inj in cls._injections_generator(number) if inj.power != 0}

        return cls(powers)

    def __int__(self) -> int:
        """Returns the integer value of the factorized representation."""
        return reduce(operator.mul, [prime ** power for prime, power in self.injections.items()], 1)

    def __len__(self) -> int:
        return len([elem for elem in self.injections.values() if elem != 0])

    def _mul(self, other: Self) -> Self:
        """Returns the product of the factorized integer and another factorized integer."""
        primes = self._get_primes_sets(other)

        result = {}
        result.update({prime: self.injections[prime] for prime in primes.only_self})
        result.update({prime: other.injections[prime] for prime in primes.only_other})
        result.update({prime: self.injections[prime] + other.injections[prime] for prime in primes.common})

        return FactorizedIntByDict(result)

    def _floordiv(self, other: Self) -> Self:
        """Returns the division of the factorized integer and another factorized integer."""
        primes = self._get_primes_sets(other)

        result = {}
        result.update({prime: self.injections[prime] for prime in primes.only_self})
        result.update({prime: -other.injections[prime] for prime in primes.only_other})
        result.update({prime: self.injections[prime] - other.injections[prime] for prime in primes.common})

        return FactorizedIntByDict(result)

    def _gcd(self, other: Self) -> Self:
        """Returns the GCD of the factorized integer and another factorized integer."""
        common = set(self.injections.keys()).intersection(other.injections.keys())

        result = {}
        result.update({prime: min(self.injections[prime], other.injections[prime]) for prime in common})

        return FactorizedIntByDict(result)

    def _lcm(self, other: Self) -> Self:
        """Returns the LCM of the factorized integer and another factorized integer or an integer."""
        primes = self._get_primes_sets(other)

        result = {}
        result.update({prime: self.injections[prime] for prime in primes.only_self})
        result.update({prime: other.injections[prime] for prime in primes.only_other})
        result.update({prime: max(self.injections[prime], other.injections[prime]) for prime in primes.common})

        return FactorizedIntByDict(result)

    def _get_primes_sets(self, other: Self) -> PrimesWithOtherSets:
        """
        Separates primes of self and other to three sets: common primes, only other primes and only self primes.

        Args:
            other (Union[FactorizedIntByDict, int]): Another FactorizedIntByDict instance or an integer.

        Returns:
            PrimesWithOtherSets: A tuple with the sets.
        """
        self_primes = set(self.injections.keys())
        other_primes = set(other.injections.keys())
        
        common = self_primes.intersection(other_primes)
        
        return PrimesWithOtherSets(
            common=common,
            only_self=self_primes.difference(common),
            only_other=other_primes.difference(common),
        )

    def apply(self, action: Callable) -> Self:
        """Applies given action for powers of each prime."""
        generator = ((prime, action(power)) for prime, power in self.injections)
        return self.__class__({prime: power for prime, power in generator if power != 0})
