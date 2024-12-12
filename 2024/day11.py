from typing import List, Tuple
from math import log10
import helper


def parse_stones(input: str) -> List[int]:
    return [int(x) for x in input.split()]


def blink(stones: List[int]) -> List[int]:
    new_stones = []

    for stone in stones:
        if stone == 0:
            new_stones.append(1)
        elif int(log10(stone)) % 2 == 1:
            digits = str(stone)
            new_stones.extend([int(digits[:len(digits)//2]), int(digits[len(digits)//2:])]) 
        else:
            new_stones.append(stone * 2024)

    return new_stones


def part1(input: str) -> int:
    stones = parse_stones(input)
    for _ in range(25):
        stones = blink(stones)

    return len(stones)


def part2(input: str) -> int:
    stones = parse_stones(input)
    for i in range(75):
        stones = blink(stones)
        print(f'{i}: {len(stones)}')

    return len(stones)


cache = {}

def blink_stone(stone: int, n_blinks: int) -> int:
    if n_blinks == 0:
        return 1
    
    if (stone, n_blinks) in cache:
        return cache[(stone, n_blinks)]
    
    if stone == 0:
        total_stones = blink_stone(1, n_blinks - 1)
    
    elif int(log10(stone)) % 2 == 1:
        digits = str(stone)
        total_stones = blink_stone(int(digits[:len(digits)//2]), n_blinks - 1) + blink_stone(int(digits[len(digits)//2:]), n_blinks - 1)

    else:
        total_stones = blink_stone(stone * 2024, n_blinks - 1)

    cache[(stone, n_blinks)] = total_stones
    return total_stones


def part2_faster(input: str) -> int:
    stones = parse_stones(input)
    total_stones = 0

    for stone in stones:
        total_stones += blink_stone(stone, 75)

    return total_stones



if __name__ == '__main__':
    ### THE TESTS
    example_input = '''0 1 10 99 999'''
    stones = parse_stones(example_input)
    new_stones = blink(stones)

    example_input = '''125 17'''
    results = part1(example_input)
    assert results == 55312, f'Expected 55312 but got {results}'

    ### THE REAL THING
    puzzle_input = helper.read_input()
    print(f'Part 1: {part1(puzzle_input)}')
    print(f'Part 2: {part2_faster(puzzle_input)}')
