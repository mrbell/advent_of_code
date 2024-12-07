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


def walk_path(map: List[str], starting_point: Tuple[int, int], starting_dir: str) -> List[Tuple[Tuple[int, int], str]]:
    path = []
    current_point = starting_point
    current_dir = starting_dir
    loop_found = False

    while True:
        if (current_point, current_dir) in path:
            loop_found = True
            break
        path.append((current_point, current_dir))
        next_point = (current_point[0] + dir_step[current_dir][0], current_point[1] + dir_step[current_dir][1])
        if next_point[0] < 0 or next_point[0] >= len(map) or next_point[1] < 0 or next_point[1] >= len(map[0]):
            break
        if map[next_point[0]][next_point[1]] == barrier:
            current_dir = dirs[(dirs.index(current_dir) + 1) % 4]
            continue
        current_point = next_point
    
    return path, loop_found


def part1(puzzle_input: str) -> int:
    map, starting_point, starting_dir = parse_map(puzzle_input)
    path, _ = walk_path(map, starting_point, starting_dir)
    return len(set([p[0] for p in path]))


def part2(puzzle_input: str) -> int:
    map, starting_point, starting_dir = parse_map(puzzle_input)
    path, _ = walk_path(map, starting_point, starting_dir)
    
    unique_path = set([p[0] for p in path if p[0] != starting_point])

    count = 0
    for i, p in enumerate(unique_path):
        new_map = [list(row) for row in map]
        new_map[p[0]][p[1]] = barrier
        _, loop_found = walk_path(new_map, starting_point, starting_dir)
        if loop_found:
            count += 1
        
        if (i + 1) % 100 == 0:
            print(f'Checked {i + 1} steps, found {count} loops')

    return count


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
    test2 = part2(test_input)
    assert test2 == 6, f'Expected 6 but got {test2}'

    ### THE REAL THING
    puzzle_input = helper.read_input()
    print(f'Part 1: {part1(puzzle_input)}')
    print(f'Part 2: {part2(puzzle_input)}')  
