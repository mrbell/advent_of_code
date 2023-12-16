from typing import List, Tuple
from day13 import transpose
import helper


n_rotations = {"N": 0, "E": 3, "S": 2, "W": 1}


def flip_map(rock_map: List[str]) -> List[str]:
    """
    Flips the map vertically.
    """
    return rock_map[::-1]


def rotate_map(rock_map: List[str], direction: int) -> List[str]:
    """
    Rotates the map 90 deg in the given direction, 1 = clockwise, -1 = counterclockwise.
    """
    new_map = copy_map(rock_map)
    if direction == 1:
        new_map = flip_map(new_map)
    new_map = transpose(new_map)
    if direction == -1:
        new_map = flip_map(new_map)

    return new_map


def tilt_map_north(rock_map: List[str]) -> List[str]:
    """
    Tilts the map north.
    """
    new_map = rotate_map(rock_map, -1)
    while True:
        rolled_map = [row.replace('.O', 'O.') for row in new_map]
        if maps_equal(new_map, rolled_map):
            break
        else:
            new_map = rolled_map
    new_map = rotate_map(new_map, 1)
    return new_map


def copy_map(rock_map: List[str]) -> List[str]:
    """
    Copies the rock map.
    """
    return rock_map.copy()


def tilt_map(rock_map: List[str], tilt: str) -> List[str]:
    """
    Tilts the map in the given direction (N, S, E, W). 
    Round rocks (O) will roll in the direction tilted, square rocks (#) will not.
    Empty space is represented by a dot (.)
    """
    new_map = copy_map(rock_map)
    for _ in range(n_rotations[tilt]):
        new_map = rotate_map(new_map, 1)
    new_map = tilt_map_north(new_map)
    for _ in range(n_rotations[tilt]):
        new_map = rotate_map(new_map, -1)
    
    return new_map


def calculate_load(rock_map: List[str]) -> int:
    """
    Calculates the load of the rock map.
    """
    total_load = 0
    N = len(rock_map)
    for i, row in enumerate(rock_map):
        single_rock_load = N - i
        total_load += row.count('O') * single_rock_load
    return total_load    


def maps_equal(map1: List[str], map2: List[str]) -> bool:
    """
    Checks if two maps are equal.
    """
    return all(map1[i] == map2[i] for i in range(len(map1)))


def part1(rock_map: List[str]) -> int:
    """
    Returns the load of the rock map after it has been tilted north.
    """
    return calculate_load(tilt_map(rock_map, 'N'))


def cycle_map(rock_map: List[str]) -> List[str]:
    new_map = copy_map(rock_map)
    for tilt in 'NWSE':
        new_map = tilt_map(new_map, tilt)
    return new_map 


def check_for_pattern(seq: List[int]) -> Tuple[int, List[int]]:
    """
    Checks if the given sequence has a pattern. Return when the pattern starts and how long it is.
    """
    for i in range(len(seq)):
        for j in range(i + 2, len(seq)):
            if seq[i:j] == seq[j:2 * j - i]:
                return i, seq[i:j]
    return -1, []


def part2(rock_map: List[str]) -> int:
    
    cycle_loads = []
    N = 1_000_000_000
    for _ in range(N):
        rock_map = cycle_map(rock_map)
        cycle_load = calculate_load(rock_map)
        cycle_loads.append(cycle_load)
        pattern_start, pattern = check_for_pattern(cycle_loads)
        if pattern_start != -1:
            break

    cycle_load = pattern[(N - pattern_start - 1) % len(pattern)]

    return cycle_load


if __name__ == '__main__':
    ### THE TESTS
    test_input = '''O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....'''.splitlines()

    test_input_2 = '''OOOO.#.O..
OO..#....#
OO..O##..O
O..#.OO...
........#.
..#....#.#
..O..#.O.O
..O.......
#....###..
#....#....'''.splitlines()

    test_input_3 = '''.....#....
....#...O#
...OO##...
.OO#......
.....OOO#.
.O#...O#.#
....O#....
......OOOO
#...O###..
#..OO#....'''.splitlines()
    
    test_input_4 = [87, 69, 69, 69, 65, 64, 65, 63, 68, 69, 69, 65, 64, 65, 63, 68]
    assert check_for_pattern(test_input_4) == (2, [69, 69, 65, 64, 65, 63, 68])

    assert calculate_load(test_input_2) == 136
    assert maps_equal(tilt_map(test_input, 'N'), test_input_2)
    assert maps_equal(cycle_map(test_input), test_input_3)
    assert part1(test_input) == 136
    assert part2(test_input) == 64

    ### THE REAL THING
    puzzle_input = helper.read_input_lines()
    print(f'Part 1: {part1(puzzle_input)}')
    print(f'Part 2: {part2(puzzle_input)}')
