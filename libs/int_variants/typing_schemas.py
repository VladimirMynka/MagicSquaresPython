from typing import TypeAlias, NamedTuple

Prime: TypeAlias = int


class PrimesWithOtherSets(NamedTuple):
    common: set[Prime]
    only_self: set[Prime]
    only_other: set[Prime]
