import collections
import dataclasses
import itertools
from typing import Self


@dataclasses.dataclass(slots=True, frozen=True)
class v2:
    x: int
    y: int

    def __add__(self, other: Self) -> Self:
        return self.__class__(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Self) -> Self:
        return self.__class__(self.x - other.x, self.y - other.y)


def solve_part1(input: str) -> int:
    red_tiles = [v2(*map(int, row.split(','))) for row in input.splitlines()]
    return max(
        (abs((rect := (a - b)).x) + 1) * (abs(rect.y) + 1)
        for a, b in itertools.combinations(red_tiles, r=2)
    )


def edge_in_rect(a: v2, b: v2, edge_tiles: set[v2]) -> bool:
    # NOTE: from the future
    # there has to be a better way to check this
    # instead of going through each edge tile
    # but i have spent too much time already
    # maybe later
    minx, maxx = sorted((a.x, b.x))
    miny, maxy = sorted((a.y, b.y))
    return any(minx < t.x < maxx and miny < t.y < maxy for t in edge_tiles)


def solve_part2(input: str) -> int:
    red_tiles = set(
        v2(*map(int, row.split(','))) for row in input.splitlines()
    )

    path: list[v2] = []
    start = min(red_tiles, key=lambda t: (t.y, t.x))
    horiz = True

    pos = start
    while True:
        possible_next = [
            t
            for t in red_tiles
            if ((t.y == pos.y) if horiz else (t.x == pos.x)) and t is not pos
        ]
        assert len(possible_next) == 1

        if len(path) and pos is start:
            break
        path.append(pos)

        pos = possible_next[0]
        horiz = not horiz

    edge_tiles: set[v2] = set()
    for ab in itertools.pairwise(path + [start]):
        a, b = sorted(ab, key=lambda t: (t.y, t.x))
        edge_tiles.update(
            v2(x, y) for x in range(a.x, b.x + 1) for y in range(a.y, b.y + 1)
        )

    return max(
        (abs((rect := (a - b)).x) + 1) * (abs(rect.y) + 1)
        for a, b in itertools.combinations(red_tiles, r=2)
        if not edge_in_rect(a, b, edge_tiles)
    )


def edge_in_rect2(
    a: v2, b: v2, tile_map: dict[tuple[int, int], set[v2]], scale: int
) -> bool:
    minx, maxx = sorted((a.x, b.x))
    miny, maxy = sorted((a.y, b.y))

    return any(
        minx < t.x < maxx and miny < t.y < maxy
        for xxx in range(minx // scale, maxx // scale + 1)
        for yyy in range(miny // scale, maxy // scale + 1)
        for t in tile_map[xxx, yyy]
    )


# NOTE: from the future
# version with more optimized collision detection
def extra_part2_0(input: str) -> int:
    red_tiles = set(
        v2(*map(int, row.split(','))) for row in input.splitlines()
    )

    path: list[v2] = []
    start = min(red_tiles, key=lambda t: (t.y, t.x))
    horiz = True

    pos = start
    while True:
        possible_next = [
            t
            for t in red_tiles
            if ((t.y == pos.y) if horiz else (t.x == pos.x)) and t is not pos
        ]
        assert len(possible_next) == 1

        # NOTE: from the future
        # i also put the append before the break
        # so we don't need to `path + [start]` later
        path.append(pos)
        if len(path) > 1 and pos is start:
            break

        pos = possible_next[0]
        horiz = not horiz

    # NOTE: from the future
    # 1000 is better than whatever calculation i came up with
    scale = 1000
    tile_map: collections.defaultdict[tuple[int, int], set[v2]] = (
        collections.defaultdict(set)
    )
    for ab in itertools.pairwise(path):
        a, b = sorted(ab, key=lambda t: (t.y, t.x))
        for x in range(a.x, b.x + 1):
            for y in range(a.y, b.y + 1):
                tile = v2(x, y)
                tile_map[x // scale, y // scale].add(tile)

    return max(
        (abs((rect := (a - b)).x) + 1) * (abs(rect.y) + 1)
        for a, b in itertools.combinations(red_tiles, r=2)
        if not edge_in_rect2(a, b, tile_map, scale)
    )
