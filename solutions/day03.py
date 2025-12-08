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

                # NOTE: from the future
                # result calculation misplaced
                # at least should be inside the if block below
                # and idealy calculated only if the last digit is changed
                result = max(
                    result,
                    sum(
                        d * 10 ** (len(digits) - 1 - i)
                        for i, d in enumerate(digits)
                    ),
                )

                # NOTE: from the future
                # also this block is triggered more times than we need
                # we sould calculate how deep the battery goes
                # and only then set the digit and wipe everything else
                if left_batteries >= left_digits and battery > digit:
                    digits[id] = battery
                    digits[id + 1 :] = [-999999 for _ in range(left_digits)]

        c += result
    return c


# NOTE: from the future
# solution_part2 with the changes form the comments implemented
def extra_part2_0(input: str) -> int:
    banks = [[int(battery) for battery in bank] for bank in input.splitlines()]
    c = 0
    for bank in banks:
        digits = [-999999 for _ in range(12)]
        result = -999999
        for ib, battery in enumerate(bank):
            left_batteries = len(bank) - 1 - ib

            id = -999999
            for id, digit in reversed(list(enumerate(digits))):
                if battery <= digit or left_batteries < (len(digits) - 1 - id):
                    break
            else:
                id -= 1

            if id == len(digits) - 1:
                continue

            id += 1
            left_digits = len(digits) - 1 - id

            digits[id] = battery
            if left_digits:
                digits[id + 1 :] = [-999999 for _ in range(left_digits)]
            else:
                result = sum(
                    d * 10 ** (len(digits) - 1 - i)
                    for i, d in enumerate(digits)
                )

        c += result
    return c
