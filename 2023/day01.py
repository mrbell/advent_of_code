from typing import List, Tuple
import helper


digits = {}
for i in range(1, 10):
    digits[str(i)] = i

spelled_digits = {
    'one': 1,
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5,
    'six': 6,
    'seven': 7,
    'eight': 8,
    'nine': 9
}


def parse_calibration_value(s: str, spelled=False, verbose=False) -> int:
    if spelled:
        all_digits = digits.copy()
        for k in spelled_digits:
            all_digits[k] = spelled_digits[k]
    else:
        all_digits = digits.copy()

    val = 0
    
    found_digits = []
    for k in all_digits:
        root = 0
        while root < len(s):
            # The substring may appear more than once
            try:
                pos = s[root:].index(k)
                found_digits.append((pos + root, all_digits[k]))
                root = pos + root + 1
            except ValueError:
                break  # the substring isn't in the string

    first_digit = min(found_digits, key=lambda x: x[0])[1]
    last_digit = max(found_digits, key=lambda x: x[0])[1]

    cal_val = first_digit * 10 + last_digit
    if verbose:
        print(s, cal_val)
    return cal_val


def cal_sums(inps: List[str], spelled=False, verbose=False) -> int:
    return sum(parse_calibration_value(i, spelled, verbose) for i in inps)


if __name__ == '__main__':
    ### THE TESTS
    test_input = '''1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet'''.split('\n')

    test_input2 = '''two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen'''.split('\n')

    assert cal_sums(test_input) == 142
    assert cal_sums(test_input2, True) == 281
    assert parse_calibration_value('sixthree6lxcrsevenseven69twonegs', True) == 61
    assert parse_calibration_value('fpfqp7three7', True) == 77

    ### THE REAL THING
    puzzle_input = helper.read_input_lines()
    print(f'Part 1: {cal_sums(puzzle_input)}')
    print(f'Part 2: {cal_sums(puzzle_input, True)}')
