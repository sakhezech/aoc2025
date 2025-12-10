import dataclasses
import functools


@dataclasses.dataclass
class Machine:
    indicators: tuple[bool, ...]
    buttons: tuple[tuple[int, ...], ...]
    joltages: tuple[int, ...]


def parse(input: str) -> list[Machine]:
    machines: list[Machine] = []
    for line in input.splitlines():
        indicators_str, *buttons_str, joltage_str = line.split()
        indicators = tuple(char == '#' for char in indicators_str[1:-1])
        buttons = tuple(
            tuple(int(d) for d in button[1:-1].split(','))
            for button in buttons_str
        )
        joltages = tuple(int(d) for d in joltage_str[1:-1].split(','))
        machines.append(Machine(indicators, buttons, joltages))

    return machines


@functools.cache
def press_button(
    indicators: tuple[bool, ...], button: tuple[int, ...]
) -> tuple[bool, ...]:
    return tuple(
        indicator if i not in button else not indicator
        for i, indicator in enumerate(indicators)
    )


@functools.cache
def fix_indicator(
    indicators: tuple[bool, ...],
    buttons: tuple[tuple[int, ...], ...],
    target: tuple[bool, ...],
    depth: int = 0,
) -> int:
    if indicators == target:
        return depth
    if not buttons:
        return 9999

    return min(
        fix_indicator(indicators, buttons[1:], target, depth),
        fix_indicator(
            press_button(indicators, buttons[0]),
            buttons[1:],
            target,
            depth + 1,
        ),
    )


def solve_part1(input: str) -> int:
    machines = parse(input)
    return sum(
        fix_indicator(
            tuple([False] * len(m.indicators)), m.buttons, m.indicators
        )
        for m in machines
    )
