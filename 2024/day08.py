from typing import List, Tuple, Dict
from collections import defaultdict
import helper


def parse_map(the_map: List[str]) -> Dict[str, List[Tuple[int, int]]]:
    
    antennas = defaultdict(list)

    for row_num, line in enumerate(the_map):
        for col_num, char in enumerate(line):
            if char != '.':
                antennas[char].append((row_num, col_num))
    
    return antennas


def find_antinodes(antenna_locations: List[Tuple[int, int]], map: List[str]) -> List[Tuple[int, int]]:

    antinodes = []

    for i in range(len(antenna_locations)):
        for j in range(i+1, len(antenna_locations)):
            x1, y1 = antenna_locations[i]
            x2, y2 = antenna_locations[j]

            x_diff = x2 - x1
            y_diff = y2 - y1

            ax1, ay1 = x1 - x_diff, y1 - y_diff
            ax2, ay2 = x2 + x_diff, y2 + y_diff

            if ax1 >= 0 and ax1 < len(map) and ay1 >= 0 and ay1 < len(map[0]):
                antinodes.append((ax1, ay1))
            if ax2 >= 0 and ax2 < len(map) and ay2 >= 0 and ay2 < len(map[0]):
                antinodes.append((ax2, ay2))
    
    return antinodes


def find_antinodes_w_resonant_harmonics(antenna_locations: List[Tuple[int, int]], map: List[str]) -> List[Tuple[int, int]]:

    antinodes = []

    if len(antenna_locations) > 1:
        antinodes.extend([al for al in antenna_locations])

    for i in range(len(antenna_locations)):
        for j in range(i+1, len(antenna_locations)):
            x1, y1 = antenna_locations[i]
            x2, y2 = antenna_locations[j]

            x_diff = x2 - x1
            y_diff = y2 - y1

            mul = 1
            while True:
                ax1, ay1 = x2 + x_diff * mul, y2 + y_diff * mul
                ax2, ay2 = x1 - x_diff * mul, y1 - y_diff * mul                

                anodes = len(antinodes)

                if ax1 >= 0 and ax1 < len(map) and ay1 >= 0 and ay1 < len(map[0]):
                    antinodes.append((ax1, ay1))
                if ax2 >= 0 and ax2 < len(map) and ay2 >= 0 and ay2 < len(map[0]):
                    antinodes.append((ax2, ay2))

                if len(antinodes) == anodes:
                    break

                mul += 1
    
    return antinodes


def find_all_antinodes(antennas: Dict[str, List[Tuple[int, int]]], map: List[str], find_func: callable=None) -> List[Tuple[int, int]]:

    antinodes = []

    if find_func is None:
        find_func = find_antinodes

    for antenna in antennas:
        antinodes.extend(find_func(antennas[antenna], map))
    
    return antinodes


def part1(map: List[str]) -> int:

    antennas = parse_map(map)
    antinodes = find_all_antinodes(antennas, map)

    return len(set(antinodes))


def part2(map: List[str]) -> int:
    
    antennas = parse_map(map)
    antinodes = find_all_antinodes(antennas, map, find_antinodes_w_resonant_harmonics)

    return len(set(antinodes))


if __name__ == '__main__':
    ### THE TESTS
    example_input = '''............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............'''.split('\n')

    example = part1(example_input)
    assert example == 14, f'Expected 14 but got {example}'
    example2 = part2(example_input)
    assert example2 == 34, f'Expected 34 but got {example2}'

    ### THE REAL THING
    puzzle_input = helper.read_input_lines()
    print(f'Part 1: {part1(puzzle_input)}')
    print(f'Part 2: {part2(puzzle_input)}')
