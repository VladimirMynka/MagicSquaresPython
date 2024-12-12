from dataclasses import dataclass
from typing import Self

from .typing_schemas import Prime


@dataclass
class FactorInjection:
    factor: Prime
    power: int

    def __str__(self) -> str:
        base = str(self.factor)
        power = '' if self.power == 1 else self._make_superscript(self.power)
        return base + power

    @property
    def value(self) -> int:
        return self.factor ** self.power

    def __int__(self) -> int:
        return self.value

    @classmethod
    def _make_superscript(cls, number: int) -> str:
        superscripts = {
            0: '⁰', 1: '¹', 2: '²', 3: '³', 4: '⁴',
            5: '⁵', 6: '⁶', 7: '⁷', 8: '⁸', 9: '⁹'
        }
        if number > 9:
            return cls._make_superscript(number // 10) + cls._make_superscript(number % 10)
        return superscripts.get(number, '')

    @classmethod
    def calculate(cls, number: int, factor: int) -> Self:
        power: int = 0
        divider: int = factor
        while number % divider == 0:
            divider *= factor
            power += 1

        return cls(factor, power)
