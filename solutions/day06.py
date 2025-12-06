from collections.abc import Iterable


def mul(iterable: Iterable[int]) -> int:
    c = 1
    for n in iterable:
        c *= n
    return c


def solve_part1(input: str) -> int:
    matrix = [row.split() for row in input.splitlines()]
    problems: list[tuple[str, list[int]]] = []
    for i in range(len(matrix[0])):
        op = matrix[-1][i]
        numbers = [int(matrix[j][i]) for j in range(len(matrix) - 1)]
        problems.append((op, numbers))

    return sum(
        mul(numbers) if op == '*' else sum(numbers) for op, numbers in problems
    )


def solve_part2(input: str) -> int:
    matrix = [list(row) for row in input.splitlines()]
    width = len(matrix[0])
    height = len(matrix)

    ops = iter(input.splitlines()[-1].split())

    problems: list[tuple[str, list[int]]] = []

    curr_column = -1
    prev_column = -1
    for i in range(width + 1):
        if i == width or all(matrix[j][i] == ' ' for j in range(len(matrix))):
            prev_column = curr_column
            curr_column = i

            numbers = []
            for j in range(prev_column + 1, curr_column):
                numbers.append(
                    int(''.join(matrix[k][j] for k in range(height - 1)))
                )

            problems.append((next(ops), numbers))

    return sum(
        mul(numbers) if op == '*' else sum(numbers) for op, numbers in problems
    )
