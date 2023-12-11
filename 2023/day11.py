from typing import List, Tuple
import helper


def find_galaxies(input: List[str], expansion: int=2) -> List[Tuple[int, int]]:

    expanded_rows = []
    for i, row in enumerate(input):
        if all(char == '.' for char in row):
            expanded_rows.append(i)
    expanded_cols = []
    for col in range(len(input[0])):
        if all(row[col] == '.' for row in input):
            expanded_cols.append(col)

    galaxies = []
    for y, line in enumerate(input):
        for x, char in enumerate(line):
            if char == '#':
                dy = sum(expansion - 1 for r in expanded_rows if r < y)
                dx = sum(expansion - 1 for c in expanded_cols if c < x)
                galaxies.append((x + dx, y + dy))

    return galaxies


def shortest_path(galaxy1: Tuple[int, int], galaxy2: Tuple[int, int]) -> int:
    return abs(galaxy1[0] - galaxy2[0]) + abs(galaxy1[1] - galaxy2[1])


def part1(puzzle_input: List[str], expansion: int=2) -> int:
    galaxies = find_galaxies(puzzle_input, expansion)
    path_sum = 0
    for i, galaxy1 in enumerate(galaxies):
        for galaxy2 in galaxies[(i+1):]:
            path_sum += shortest_path(galaxy1, galaxy2)
    return path_sum


def part2(puzzle_input: List[str]) -> int:
    return part1(puzzle_input, expansion=1000000)


if __name__ == '__main__':
    ### THE TESTS
    test_input = '''...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....'''.splitlines()
    assert part1(test_input) == 374

    ### THE REAL THING
    puzzle_input = helper.read_input_lines()
    print(f'Part 1: {part1(puzzle_input)}')
    print(f'Part 2: {part2(puzzle_input)}')
