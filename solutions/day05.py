def parse(input: str) -> tuple[list[tuple[int, int]], list[int]]:
    ranges_str, _, available_str = input.partition('\n\n')

    ranges: list[tuple[int, int]] = []
    for range_str in ranges_str.splitlines():
        ll, _, rr = range_str.partition('-')
        ranges.append((int(ll), int(rr)))
    available = [int(v) for v in available_str.splitlines()]

    return ranges, available


def solve_part1(input: str) -> int:
    ranges, available = parse(input)
    c = 0
    for id in available:
        for ll, rr in ranges:
            if ll <= id <= rr:
                c += 1
                break

    return c


def intersect(
    r1: tuple[int, int], r2: tuple[int, int]
) -> tuple[int, int] | None:
    r1_left, r1_right = r1
    r2_left, r2_right = r2
    if any(r1_left <= r <= r1_right for r in r2):
        return min(r1_left, r2_left), max(r1_right, r2_right)
    return None


def solve_part2(input: str) -> int:
    ranges, _ = parse(input)

    changed = True
    while changed:
        changed = False
        for i, r1 in enumerate(ranges):
            for j, r2 in enumerate(ranges):
                if i == j:
                    continue
                intersected = intersect(r1, r2)
                if intersected:
                    ranges[i] = intersected
                    del ranges[j]
                    changed = True
                    break
            if changed:
                break

    return sum(rr - ll + 1 for ll, rr in ranges)


# NOTE: from the future
# i like this solution more
# but i did solve the puzzle with the one above
def solve_part3(input: str) -> int:
    ranges, _ = parse(input)

    i = j = 0
    while i != len(ranges):
        if i != j:
            r1 = ranges[i]
            r2 = ranges[j]

            intersected = intersect(r1, r2)
            if intersected:
                ranges[i] = intersected
                del ranges[j]
                if j < i:
                    i -= 1
                j = -1
        j += 1
        if j == len(ranges):
            j = 0
            i += 1

    return sum(rr - ll + 1 for ll, rr in ranges)
