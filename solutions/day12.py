import functools
import multiprocessing


def parse(
    input: str,
) -> tuple[
    list[tuple[tuple[str, ...], ...]], list[tuple[list[list[str]], list[int]]]
]:
    *piece_strs, boxes_and_pi = input.split('\n\n')
    pieces: list[tuple[tuple[str, ...], ...]] = []
    problems: list[tuple[list[list[str]], list[int]]] = []
    for bbb in boxes_and_pi.splitlines():
        box_str, _, ntp_str = bbb.partition(':')
        ntp = [int(v) for v in ntp_str.split()]
        x, y = (int(v) for v in box_str.split('x'))
        box = [
            ['!'] * (x + 2),
            *[['!'] + ['.'] * x + ['!'] for _ in range(y)],
            ['!'] * (x + 2),
        ]
        problems.append((box, ntp))
    for p_str in piece_strs:
        pieces.append(tuple(tuple(row) for row in p_str.splitlines()[1:]))
    return pieces, problems


def rotate_piece_right(
    piece: tuple[tuple[str, ...], ...],
) -> tuple[tuple[str, ...], ...]:
    return tuple(tuple(reversed(z)) for z in zip(*piece))


def mirror_piece(
    piece: tuple[tuple[str, ...], ...],
) -> tuple[tuple[str, ...], ...]:
    return tuple(tuple(reversed(r)) for r in piece)


@functools.cache
def get_all_piece_variants(
    piece: tuple[tuple[str, ...], ...],
) -> list[tuple[tuple[str, ...], ...]]:
    pieces = [piece]
    for _ in range(3):
        pieces.append(rotate_piece_right(pieces[-1]))
    pieces.append(mirror_piece(piece))
    for _ in range(3):
        pieces.append(rotate_piece_right(pieces[-1]))
    return pieces


@functools.cache
def try_fitting_a_piece(
    kernel: tuple[tuple[str, ...], ...], piece: tuple[tuple[str, ...], ...]
) -> tuple[int, tuple[tuple[str, ...], ...]] | None:
    assert len(kernel) == len(piece) + 2
    assert len(kernel[0]) == len(piece[0]) + 2

    for kernel_row, piece_row in zip(kernel[1:-1], piece):
        if not all(
            k_p != '#'
            for k_p, p_p in zip(kernel_row[1:-1], piece_row)
            if p_p == '#'
        ):
            return None
    neighbors: set[tuple[int, int]] = set()
    mut_kernel = [list(r) for r in kernel]

    for y, piece_row in enumerate(piece, 1):
        for x, p_p in enumerate(piece_row, 1):
            if p_p == '#':
                mut_kernel[y][x] = '#'
                neighbors.update(
                    (x + dx, y + dy)
                    for dx in range(-1, 2, 2)
                    for dy in range(-1, 2, 2)
                    if kernel[y + dy][x + dx] == '#'
                )
    return len(neighbors), tuple(tuple(r) for r in mut_kernel)


def pack(
    box: list[list[str]],
    pieces: list[tuple[tuple[str, ...], ...]],
    num_to_place: list[int],
) -> bool:
    while sum(num_to_place):
        best = None
        pieces_to_place = [
            (i, x) for (i, x) in enumerate(pieces) if num_to_place[i] > 0
        ]
        for id, piece in pieces_to_place:
            for y in range(len(box) - len(piece) - 1):
                for x in range(len(box[0]) - len(piece[0]) - 1):
                    kernel = tuple(
                        tuple(box[yy][x : x + len(piece[0]) + 2])
                        for yy in range(y, y + len(piece) + 2)
                    )
                    fits = [
                        try_fitting_a_piece(kernel, v)
                        for v in get_all_piece_variants(piece)
                    ]
                    fits = [v for v in fits if v is not None]
                    if not fits:
                        continue
                    fits.sort(key=lambda x: x[0], reverse=True)
                    chosen_fit = fits[0]
                    hello = (*chosen_fit, id, x, y)
                    best = (
                        hello
                        if best is None
                        else max(best, hello, key=lambda x: x[0])
                    )

        if best is None:
            return False
        _, merged, id, x, y = best

        num_to_place[id] -= 1
        for dy, row in enumerate(merged):
            for dx, char in enumerate(row):
                box[y + dy][x + dx] = char

    return True


def wrap_pack(x) -> bool:
    return pack(*x)


def solve_part1(input: str) -> int:
    pieces, tasks = parse(input)

    with multiprocessing.Pool() as pool:
        return sum(
            pool.map(wrap_pack, [(box, pieces, ntp) for box, ntp in tasks])
        )
