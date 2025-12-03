from typing import List, Tuple
from textwrap import dedent
import helper


def get_largest_joltage_v1(bank: str) -> int:
    max_first_digit = max(bank[:-1])
    index_of_max_first_digit = bank.index(max_first_digit)
    max_second_digit = max(bank[index_of_max_first_digit + 1:])
    return 10*int(max_first_digit) + int(max_second_digit)


def get_largest_joltage(bank: str, n_digits: int=2) -> int:

    joltage = 0
    current_index = -1

    while n_digits > 0:

        start_range = current_index + 1
        end_range = len(bank) - (n_digits - 1)

        max_next_digit = max(bank[start_range:end_range])
        current_index = start_range + bank[start_range:end_range].index(max_next_digit)
        
        n_digits -= 1

        joltage += (10 ** n_digits) * int(max_next_digit)


    return joltage


def part1(puzzle_input: List[str]) -> int:
    joltage = 0
    for bank in puzzle_input:
        joltage += get_largest_joltage(bank)
    return joltage


def part2(puzzle_input: List[str]) -> int:
    joltage = 0
    for bank in puzzle_input:
        joltage += get_largest_joltage(bank, 12)
    return joltage


if __name__ == '__main__':
    ### THE TESTS
    test_input = dedent("""
        987654321111111
        811111111111119
        234234234234278
        818181911112111
    """).strip().split('\n')

    assert get_largest_joltage('987654321111111') == 98
    assert get_largest_joltage('987654321111111', 12) == 987654321111
    assert get_largest_joltage('811111111111119') == 89
    assert get_largest_joltage('811111111111119', 12) == 811111111119
    assert get_largest_joltage('234234234234278') == 78
    assert get_largest_joltage('234234234234278', 12) == 434_234_234_278
    assert get_largest_joltage('818181911112111') == 92
    assert get_largest_joltage('818181911112111', 12) == 888911112111 

    400_000_000_000

    assert part1(test_input) == 357
    assert part2(test_input) == 3121910778619

    ### THE REAL THING
    puzzle_input = helper.read_input_lines()
    print(f'Part 1: {part1(puzzle_input)}')
    print(f'Part 2: {part2(puzzle_input)}')
