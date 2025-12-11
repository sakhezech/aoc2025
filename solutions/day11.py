import functools


def parse(input: str) -> dict[str, set[str]]:
    devices: dict[str, set[str]] = {}
    for line in input.splitlines():
        device, outputs = line[:3], set(line[4:].split())
        devices[device] = outputs
    return devices


def solve_part1(input: str) -> int:
    devices = parse(input)

    @functools.cache
    def paths_from_device_to_out(device: str) -> int:
        if device == 'out':
            return 1
        return sum(paths_from_device_to_out(d) for d in devices[device])

    return paths_from_device_to_out('you')


def solve_part2(input: str) -> int:
    devices = parse(input)

    @functools.cache
    def paths_from_device_to_device(from_: str, to: str) -> int:
        if from_ == to:
            return 1
        if from_ == 'out':
            return 0
        return sum(paths_from_device_to_device(d, to) for d in devices[from_])

    return (
        paths_from_device_to_device('svr', 'fft')
        * paths_from_device_to_device('fft', 'dac')
        * paths_from_device_to_device('dac', 'out')
    )
