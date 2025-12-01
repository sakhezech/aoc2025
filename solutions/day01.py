def solve_part1(input: str) -> int:
    pointer = 50
    count = 0
    for line in input.splitlines():
        direction, number_str = line[0], line[1:]
        number = int(number_str)
        if direction == 'L':
            pointer -= number
        elif direction == 'R':
            pointer += number
        else:
            raise ValueError(f'unknown direction: {direction}')

        pointer %= 100
        if not pointer:
            count += 1

    return count


def solve_part2(input: str) -> int:
    pointer = 50
    count = 0
    for line in input.splitlines():
        direction, number_str = line[0], line[1:]
        number = int(number_str)
        if direction == 'L':
            started_at_0 = pointer == 0
            pointer -= number

            rotations, _ = divmod(pointer - 1, 100)
            _, pointer = divmod(pointer, 100)
            count += abs(rotations) - started_at_0
        elif direction == 'R':
            pointer += number

            rotations, pointer = divmod(pointer, 100)
            count += rotations
        else:
            raise ValueError(f'unknown direction: {direction}')

    return count
