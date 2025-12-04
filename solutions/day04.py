def solve_part1(input: str) -> int:
    matrix = [list(row) for row in input.splitlines()]
    height = len(matrix)
    width = len(matrix[0])

    c = 0
    for y, row in enumerate(matrix):
        for x, char in enumerate(row):
            if char == '@':
                c += (
                    sum(
                        matrix[y + dy][x + dx] == '@'
                        for dx in range(-1, 2)
                        for dy in range(-1, 2)
                        if 0 <= y + dy < height and 0 <= x + dx < width
                    )
                    < 5
                )

    return c


def solve_part2(input: str) -> int:
    matrix = [list(row) for row in input.splitlines()]
    height = len(matrix)
    width = len(matrix[0])

    c = 0
    remove = set(((0, 0),))
    while remove:
        remove.clear()
        for y, row in enumerate(matrix):
            for x, char in enumerate(row):
                if char == '@' and (
                    sum(
                        matrix[y + dy][x + dx] == '@'
                        for dx in range(-1, 2)
                        for dy in range(-1, 2)
                        if 0 <= y + dy < height and 0 <= x + dx < width
                    )
                    < 5
                ):
                    remove.add((x, y))

        for x, y in remove:
            c += 1
            matrix[y][x] = '.'

    return c
