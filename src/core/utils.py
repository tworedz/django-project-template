import math
from typing import Union


def get_choices_max_length(choices: tuple[str, str]) -> int:
    """Получить максимальную длину строк в выборке"""

    return max(len(field) for field, _ in choices)


def round_half_up(value: Union[int, float]) -> int:
    """Round half up as "arithmetic" rounding

    Examples:

        >>> round_half_up(2.5)
        3
        >>> round_half_up(2.6)
        3
        >>>round_half_up(2.3)
        2
    """

    return math.floor(value + 0.5)
