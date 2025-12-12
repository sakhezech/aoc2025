import dataclasses
import functools
import itertools
from collections.abc import Generator


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


# Gaussian elimination
# adapted from pseudocode
# https://en.wikipedia.org/wiki/Gaussian_elimination
# https://en.wikipedia.org/wiki/Gaussian_elimination#Pseudocode
def gaussian_elimination(matrix: list[list[float]]) -> None:
    h = 0
    k = 0
    m = len(matrix)
    n = len(matrix[0])
    while h < m and k < n:
        i_max = max(range(h, m), key=lambda x: abs(matrix[x][k]))
        if matrix[i_max][k] == 0:
            k += 1
        else:
            matrix[h], matrix[i_max] = matrix[i_max], matrix[h]
            for i in range(h + 1, m):
                f = matrix[i][k] / matrix[h][k]
                matrix[i][k] = 0.0
                for j in range(k + 1, n):
                    matrix[i][j] = matrix[i][j] - matrix[h][j] * f
            h += 1
            k += 1


def product_with_sum(n: int, m: int) -> Generator[tuple[int, ...]]:
    product = itertools.product(range(m + 1), repeat=n)
    for prod in product:
        if sum(prod) != m:
            continue
        yield prod


def find_min_presses(matrix: list[list[float]]) -> float:
    original_matrix = [list(r) for r in matrix]
    gaussian_elimination(matrix)
    for row in matrix:
        for i, val in enumerate(row):
            if abs(val) < 0.001:
                row[i] = 0

    n = len(matrix[0])
    ans: list[int | float] = [0 for _ in range(n - 1)]
    unknowns = [
        i
        for i in range(n - 1)
        if not any(
            all(v == 0.0 for v in row[:i]) and row[i] != 0 for row in matrix
        )
    ]

    times_with_worse_results = 0
    result = None
    # HACK: should be max joltage of the machine
    # hardcoded value
    for prod_sum in range(200):
        local_result = None
        for product in product_with_sum(len(unknowns), prod_sum):
            for j, i in enumerate(unknowns):
                ans[i] = product[j]
            for row in reversed(matrix):
                coefficients = [x for x in enumerate(row[:-1]) if x[1] != 0]
                if not coefficients:
                    continue
                (i, head), tail = coefficients[0], coefficients[1:]

                res = (row[-1] - sum(ans[j] * val for j, val in tail)) / head
                ans[i] = res

            if any(abs(round(v) - v) > 0.1 for v in ans):
                continue
            ans = [round(v) for v in ans]

            if (
                not all(
                    abs(
                        sum(c * val for c, val in zip(row[:-1], ans)) - row[-1]
                    )
                    < 0.1
                    for row in original_matrix
                )
                > 0.01
            ):
                continue
            if any(int(v) < 0 for v in ans):
                continue

            s = sum(ans)
            local_result = s if local_result is None else min(local_result, s)

        if result is None and local_result is None:
            continue
        elif result is None:
            result = local_result
        elif local_result is None or local_result >= result:
            # HACK: arbitrary number
            if times_with_worse_results == 10:
                return result
            else:
                times_with_worse_results += 1
        else:
            result = local_result
            times_with_worse_results = 0

    assert result
    return result


def solve_part2(input: str) -> int:
    machines = parse(input)
    c = 0
    for m in machines:
        matrix = [
            [float(i in button) for button in m.buttons] + [joltage]
            for i, joltage in enumerate(m.joltages)
        ]
        c += int(find_min_presses(matrix))

    return c
