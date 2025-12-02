import itertools


def solve_part1(input: str) -> int:
    id_ranges: list[tuple[int, int]] = []
    bad_ids: list[int] = []
    for range_str in input.strip().split(','):
        s, _, e = range_str.partition('-')
        id_ranges.append((int(s), int(e)))

    for id_range in id_ranges:
        start, end = id_range
        for id in range(start, end + 1):
            string = str(id)
            length = len(string)
            if length % 2:
                continue
            if string[: length // 2] == string[length // 2 :]:
                bad_ids.append(id)

    return sum(bad_ids)


def solve_part2(input: str) -> int:
    id_ranges: list[tuple[int, int]] = []
    bad_ids: set[int] = set()
    for range_str in input.strip().split(','):
        s, _, e = range_str.partition('-')
        id_ranges.append((int(s), int(e)))

    for id_range in id_ranges:
        start, end = id_range
        for id in range(start, end + 1):
            string = str(id)
            length = len(string)
            for n in range(1, length // 2 + 1):
                if length % n:
                    continue
                batched = list(itertools.batched(string, n))
                if all(part == batched[0] for part in batched):
                    bad_ids.add(id)

    return sum(bad_ids)
