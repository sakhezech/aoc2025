def solve_part1(input: str) -> int:
    banks = [[int(battery) for battery in bank] for bank in input.splitlines()]
    c = 0
    for bank in banks:
        first = second = old = -999999
        for battery in bank:
            if battery > second:
                second = battery
            if battery > first:
                old = first * 10 + second
                first = battery
                second = -999999
        c += max(old, first * 10 + second)
    return c


def solve_part2(input: str) -> int:
    banks = [[int(battery) for battery in bank] for bank in input.splitlines()]
    c = 0
    for bank in banks:
        digits = [-999999 for _ in range(12)]
        result = -999999
        for ib, battery in enumerate(bank):
            left_batteries = len(bank) - 1 - ib

            for id, digit in reversed(list(enumerate(digits))):
                left_digits = len(digits) - 1 - id

                result = max(
                    result,
                    sum(
                        d * 10 ** (len(digits) - 1 - i)
                        for i, d in enumerate(digits)
                    ),
                )

                if left_batteries >= left_digits and battery > digit:
                    digits[id] = battery
                    digits[id + 1 :] = [-999999 for _ in range(left_digits)]

        c += result
    return c
