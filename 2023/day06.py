from typing import List, Tuple
from math import sqrt, ceil, floor
import helper


def parse_races(race_spec: List[str]) -> List[Tuple[int, int]]:
    times = race_spec[0].split()[1:]
    dists = race_spec[1].split()[1:]
    return [(int(t), int(d)) for t, d in zip(times, dists)]


def hold_time_limits(race_time: int, record_length: int) -> Tuple[int, int]:
    sqrt_part = sqrt((race_time / 2) ** 2 - record_length) 
    return race_time / 2 - sqrt_part, race_time / 2 + sqrt_part

def part1(puzzle_input: List[str]) -> int:
    races = parse_races(puzzle_input)
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

    assert part1(test_input) == 288

    ### THE REAL THING
    puzzle_input = helper.read_input_lines(6)
    print(f'Part 1: {part1(puzzle_input)}')
    print(f'Part 2: {""}')
