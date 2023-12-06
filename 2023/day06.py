from typing import List, Tuple
from math import sqrt, ceil, floor
import helper


def parse_races(race_spec: List[str]) -> List[Tuple[int, int]]:
    times = race_spec[0].split()[1:]
    dists = race_spec[1].split()[1:]
    return [(int(t), int(d)) for t, d in zip(times, dists)]


def parse_races_better(spec: List[str]) -> List[Tuple[int, int]]:
    times = spec[0].split(':')[1].replace(' ', '').strip()
    dists = spec[1].split(':')[1].replace(' ', '').strip()
    return [(int(times), int(dists))]


def hold_time_limits(race_time: int, record_length: int) -> Tuple[int, int]:
    sqrt_part = sqrt((race_time / 2) ** 2 - record_length) 
    return race_time / 2 - sqrt_part, race_time / 2 + sqrt_part


def number_of_winning_times(puzzle_input: List[str], parser=parse_races) -> int:
    races = parser(puzzle_input)
    prod = 1
    for race in races:
        ll, hl = hold_time_limits(*race)
        ll = floor(ll + 1)
        hl = ceil(hl - 1)
        n_ways = hl - ll + 1
        prod *= n_ways
    return prod


if __name__ == '__main__':
    ### THE TESTS
    test_input = '''Time:      7  15   30
Distance:  9  40  200'''.split('\n')

    assert number_of_winning_times(test_input) == 288
    assert number_of_winning_times(test_input, parse_races_better) == 71503

    ### THE REAL THING
    puzzle_input = helper.read_input_lines(6)
    print(f'Part 1: {number_of_winning_times(puzzle_input)}')
    print(f'Part 2: {number_of_winning_times(puzzle_input, parse_races_better)}')
