from typing import List, Tuple
import helper


dirs = ['N', 'E', 'S', 'W']
dir_step = {
    'N': (-1, 0),
    'E': (0, 1),
    'S': (1, 0),
    'W': (0, -1)
}
barrier = '#'
dir_chars = {
    '^': 'N', 
    '>': 'E', 
    'v': 'S', 
    '<': 'W'
}


def parse_map(map: str) -> Tuple[List[str], Tuple[int, int], str]:
    map = map.split('\n')
    for i, row in enumerate(map):
        for dir_char in dir_chars:
            if dir_char in row:
                return map, (i, row.index(dir_char)), dir_chars[dir_char]

    raise ValueError('No starting point found')


def walk_path(map: List[str], starting_point: Tuple[int, int], starting_dir: str) -> List[Tuple[int, int]]:
    path = []
    current_point = starting_point
    current_dir = starting_dir

    while True:
        path.append(current_point)
        next_point = (current_point[0] + dir_step[current_dir][0], current_point[1] + dir_step[current_dir][1])
        if next_point[0] < 0 or next_point[0] >= len(map) or next_point[1] < 0 or next_point[1] >= len(map[0]):
            break
        if map[next_point[0]][next_point[1]] == barrier:
            current_dir = dirs[(dirs.index(current_dir) + 1) % 4]
            continue
        current_point = next_point
    
    return path


def part1(puzzle_input: str) -> int:
    map, starting_point, starting_dir = parse_map(puzzle_input)
    path = walk_path(map, starting_point, starting_dir)
    return len(set(path))


if __name__ == '__main__':
    ### THE TESTS
    test_input = '''....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...'''
    test = part1(test_input)
    assert test == 41, f'Expected 41 but got {test}'


    ### THE REAL THING
    puzzle_input = helper.read_input()
    print(f'Part 1: {part1(puzzle_input)}')
    print(f'Part 2: {""}')
