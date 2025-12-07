import dataclasses
import functools
from typing import Self


@dataclasses.dataclass(slots=True, frozen=True)
class v2:
    x: int
    y: int

    def __add__(self, other: Self) -> Self:
        return self.__class__(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Self) -> Self:
        return self.__class__(self.x - other.x, self.y - other.y)


def parse(input: str) -> tuple[list[list[str]], v2]:
    matrix = [list(row) for row in input.splitlines()]
    for y, row in enumerate(matrix):
        for x, char in enumerate(row):
            if char == 'S':
                return matrix, v2(x, y)
    raise ValueError('no head')


def solve_part1(input: str) -> int:
    matrix, head = parse(input)
    width = len(matrix[0])
    height = len(matrix)
    down = v2(0, 1)
    left = v2(-1, 0)
    right = v2(1, 0)
    c = 0

    visited: list[v2] = []
    heads = [head]
    while heads:
        new_heads = []
        for head in heads:
            if head in visited:
                continue
            visited.append(head)
            head = head + down
            if not (0 <= head.x < width) or not (0 <= head.y < height):
                continue
            if matrix[head.y][head.x] == '^':
                new_heads.extend((head + left, head + right))
                c += 1
            else:
                new_heads.append(head)
        heads = new_heads

    return c


def solve_part2(input: str) -> int:
    matrix, head = parse(input)
    width = len(matrix[0])
    height = len(matrix)
    down = v2(0, 1)
    left = v2(-1, 0)
    right = v2(1, 0)

    @functools.cache
    def splits_from_head(head: v2) -> int:
        while True:
            head = head + down
            if not (0 <= head.x < width) or not (0 <= head.y < height):
                return 1
            if matrix[head.y][head.x] == '^':
                return splits_from_head(head + left) + splits_from_head(
                    head + right
                )

    return splits_from_head(head)


# NOTE: from the future
# part1 solution made from part2 solution
# way faster than what i came up with initially
def solve_part3(input: str) -> int:
    matrix, head = parse(input)
    width = len(matrix[0])
    height = len(matrix)
    down = v2(0, 1)
    left = v2(-1, 0)
    right = v2(1, 0)
    splitters: set[v2] = set()

    @functools.cache
    def splits_from_head(head: v2) -> int:
        while True:
            head = head + down
            if not (0 <= head.x < width) or not (0 <= head.y < height):
                return 1
            if matrix[head.y][head.x] == '^':
                splitters.add(head)
                return splits_from_head(head + left) + splits_from_head(
                    head + right
                )

    _ = splits_from_head(head)
    return len(splitters)
