import dataclasses
import math
from typing import Self


@dataclasses.dataclass(slots=True, frozen=True)
class v3:
    x: int
    y: int
    z: int

    def __add__(self, other: Self) -> Self:
        return self.__class__(
            self.x + other.x, self.y + other.y, self.z + other.z
        )

    def __sub__(self, other: Self) -> Self:
        return self.__class__(
            self.x - other.x, self.y - other.y, self.z - other.z
        )

    def __pow__(self, num: int | float) -> Self:
        return self.__class__(self.x**num, self.y**num, self.z**num)

    def get_distance(self, other: Self) -> float:
        v = (self - other) ** 2
        # NOTE: because we only need the distance for sorting
        # we dont actually need to math.sqrt
        # x > y -> math.sqrt(x) > math.sqrt(y)
        return v.x + v.y + v.z  # return math.sqrt(v.x + v.y + v.z)


def parse(input: str) -> list[v3]:
    return [v3(*map(int, row.split(','))) for row in input.splitlines()]


def solve_part1(input: str) -> int:
    junctions = parse(input)
    distances: list[tuple[float, v3, v3]] = []
    for i, j1 in enumerate(junctions):
        for j2 in junctions[i + 1 :]:
            distances.append((j1.get_distance(j2), j1, j2))
    distances.sort()

    circuits: list[set[v3]] = []
    cache: dict[v3, set[v3]] = {}

    for _ in range(1000):
        # NOTE: from the future (last comment)
        # i remembered why i did distances.pop() instead of
        # `for _, j1, j2 in distances[:1000]`
        # i thought that when we skip a connection we shouldn't include it
        # in the 1000 we are connecting
        # and so this originally was a `while c < 1000:` loop
        # and when i realized that we shouldn't skip counting
        # i just changed the while loop to `for _ in range(1000):`
        # and left everything else unchanged
        _, j1, j2 = distances.pop(0)
        if j1 in cache and j2 in cache:
            s1 = cache[j1]
            s2 = cache[j2]
            if s1 is s2:
                continue

            s1.update(s2)
            circuits.remove(s2)
            for j in s2:
                cache[j] = s1
        elif j1 in cache:
            s = cache[j1]
            s.add(j2)
            cache[j2] = s
        elif j2 in cache:
            s = cache[j2]
            s.add(j1)
            cache[j1] = s
        else:
            s: set[v3] = set()
            s.add(j1)
            s.add(j2)
            cache[j1] = s
            cache[j2] = s
            circuits.append(s)

    return math.prod(sorted(len(s) for s in circuits)[-3:])


def solve_part2(input: str) -> int:
    junctions = parse(input)
    distances: list[tuple[float, v3, v3]] = []
    for i, j1 in enumerate(junctions):
        for j2 in junctions[i + 1 :]:
            distances.append((j1.get_distance(j2), j1, j2))
    distances.sort()
    # NOTE: from the future
    # actually embarrassing, learnt nothing from day07
    # use collections.deque
    # makes the solution ~15x faster on my machine
    # idiot

    circuits: list[set[v3]] = []
    cache: dict[v3, set[v3]] = {}

    result = 0
    # NOTE: from the future
    # or just iterate through the distances
    # even more embarrassing
    # 2x idiot
    # for _, j1, j2 in distances:
    while distances:
        _, j1, j2 = distances.pop(0)
        if j1 in cache and j2 in cache:
            s1 = cache[j1]
            s2 = cache[j2]
            if s1 is s2:
                continue

            s1.update(s2)
            circuits.remove(s2)
            for j in s2:
                cache[j] = s1
        elif j1 in cache:
            s = cache[j1]
            s.add(j2)
            cache[j2] = s
        elif j2 in cache:
            s = cache[j2]
            s.add(j1)
            cache[j1] = s
        else:
            s: set[v3] = set()
            s.add(j1)
            s.add(j2)
            cache[j1] = s
            cache[j2] = s
            circuits.append(s)
        result = j1.x * j2.x

    return result


# NOTE: from the future
# solution_part1 with the changes form the comments implemented
def extra_part1_0(input: str) -> int:
    junctions = parse(input)
    distances: list[tuple[float, v3, v3]] = []
    for i, j1 in enumerate(junctions):
        for j2 in junctions[i + 1 :]:
            distances.append((j1.get_distance(j2), j1, j2))
    distances.sort()

    circuits: list[set[v3]] = []
    cache: dict[v3, set[v3]] = {}

    for _, j1, j2 in distances[:1000]:
        if j1 in cache and j2 in cache:
            s1 = cache[j1]
            s2 = cache[j2]
            if s1 is s2:
                continue

            s1.update(s2)
            circuits.remove(s2)
            for j in s2:
                cache[j] = s1
        elif j1 in cache:
            s = cache[j1]
            s.add(j2)
            cache[j2] = s
        elif j2 in cache:
            s = cache[j2]
            s.add(j1)
            cache[j1] = s
        else:
            s: set[v3] = set()
            s.add(j1)
            s.add(j2)
            cache[j1] = s
            cache[j2] = s
            circuits.append(s)

    return math.prod(sorted(len(s) for s in circuits)[-3:])


# NOTE: from the future
# solution_part2 with the changes form the comments implemented
def extra_part2_0(input: str) -> int:
    junctions = parse(input)
    distances: list[tuple[float, v3, v3]] = []
    for i, j1 in enumerate(junctions):
        for j2 in junctions[i + 1 :]:
            distances.append((j1.get_distance(j2), j1, j2))
    distances.sort()

    circuits: list[set[v3]] = []
    cache: dict[v3, set[v3]] = {}

    result = 0
    for _, j1, j2 in distances:
        if j1 in cache and j2 in cache:
            s1 = cache[j1]
            s2 = cache[j2]
            if s1 is s2:
                continue

            s1.update(s2)
            circuits.remove(s2)
            for j in s2:
                cache[j] = s1
        elif j1 in cache:
            s = cache[j1]
            s.add(j2)
            cache[j2] = s
        elif j2 in cache:
            s = cache[j2]
            s.add(j1)
            cache[j1] = s
        else:
            s: set[v3] = set()
            s.add(j1)
            s.add(j2)
            cache[j1] = s
            cache[j2] = s
            circuits.append(s)
        result = j1.x * j2.x

    return result
