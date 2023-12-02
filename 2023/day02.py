from typing import List, Tuple, Dict
from collections import defaultdict
import helper


colors = ['red', 'blue', 'green']


def parse_line(s: str) -> Tuple[int, List[Dict[str, int]]]:
    game_id = int(s.split(': ')[0].replace('Game ', ''))
    cube_sets_raw = s.split(': ')[1].split('; ')
    cube_sets = []
    for cube_set in cube_sets_raw:
        cubes = cube_set.split(', ')
        cube_colors = [c.split(' ')[1] for c in cubes]
        cube_counts = [int(c.split(' ')[0]) for c in cubes]
        cube_dict = defaultdict(int)
        for color, count in zip(cube_colors, cube_counts):
            cube_dict[color] = count
        cube_sets.append(cube_dict)

    return game_id, cube_sets

def min_cubes(cube_sets: List[Dict[str, int]]) -> Dict[str, int]:
    min_cube_dict = {color: -1 for color in colors}
    for cube_set in cube_sets:
        for color in colors:
            min_cube_dict[color] = max(min_cube_dict[color], cube_set[color])
    return min_cube_dict


def set_power(cube_set: Dict[str, int]) -> int:
    product = 1
    for color in colors:
        product *= cube_set[color]
    return product


def check_if_possible(cube_sets: List[Dict[str, int]], cube_limits: Dict[str, int]) -> bool:

    for cube_set in cube_sets:
        for color in colors:
            if cube_set[color] > cube_limits[color]:
                return False
    return True


def part1(puzzle_input: List[str]) -> int:
    games = [parse_line(i) for i in puzzle_input]
    game_sum = sum(game[0] for game in games if check_if_possible(game[1], {'red': 12, 'blue': 14, 'green': 13}))
    return game_sum


def part2(puzzle_input: List[str]) -> int:
    games = [parse_line(i) for i in puzzle_input]
    power_sum = sum(set_power(min_cubes(game[1])) for game in games)
    return power_sum


if __name__ == '__main__':
    ### THE TESTS

    test_input = '''Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green'''.split('\n')

    assert part1(test_input) == 8
    assert part2(test_input) == 2286

    ### THE REAL THING
    puzzle_input = helper.read_input_lines()
    print(f'Part 1: {part1(puzzle_input)}')
    print(f'Part 2: {part2(puzzle_input)}')
