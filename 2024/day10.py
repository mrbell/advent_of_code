from typing import List, Tuple
import helper


def parse_map(input: List[str]) -> List[List[int]]:
    return [[int(x) for x in line] for line in input]


def hike_trail(topo_map: List[List[int]], trail: List[Tuple[int, int]]) -> List[List[Tuple[int, int]]]:
    trails = []

    this_x, this_y = trail[-1]

    if topo_map[this_y][this_x] == 9:
        return [trail]

    for dy, dx in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
        next_y, next_x = this_y + dy, this_x + dx
        if 0 <= next_y < len(topo_map) and 0 <= next_x < len(topo_map[0]):
            if topo_map[next_y][next_x] == topo_map[this_y][this_x] + 1:
                new_trail = trail + [(next_x, next_y)]
                trails += hike_trail(topo_map, new_trail)
    
    return trails


def find_trail_heads(map: List[List[int]]) -> List[Tuple[Tuple[int, int], int, int]]:
    trail_heads = []

    for y, row in enumerate(map):
        for x, cell in enumerate(row):
            if cell == 0:
                trails = hike_trail(map, [(x, y)])
                summits = set([trail[-1] for trail in trails])
                trail_heads += [((y, x), len(summits), len(trails))]

    return trail_heads


def part1(input: List[str]) -> int:
    topo_map = parse_map(input)
    trail_heads = find_trail_heads(topo_map)
    return sum(n for _, n, _ in trail_heads)


def part2(input: List[str]) -> int:
    topo_map = parse_map(input)
    trail_heads = find_trail_heads(topo_map)
    return sum(n for _, _, n in trail_heads)


if __name__ == '__main__':
    ### THE TESTS
    example_input = '''89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732'''.split('\n')
    result = part1(example_input)
    assert result == 36, f'Expected 36 but got {result}'
    result = part2(example_input)
    assert result == 81, f'Expected 81 but got {result}'


    ### THE REAL THING
    puzzle_input = helper.read_input_lines()
    print(f'Part 1: {part1(puzzle_input)}')
    print(f'Part 2: {part2(puzzle_input)}')
