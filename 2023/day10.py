from typing import List, Tuple, Dict
from dataclasses import dataclass
import helper


dirs = {'N': (0, -1), 'S': (0, 1), 'E': (1, 0), 'W': (-1, 0)}
pipes = {'|': 'NS', '-': 'EW', 'L': 'NE', 'J': 'NW', '7': 'SW', 'F': 'SE'}
inv_pipes = {}
for pipe in pipes:
    inv_pipes[pipes[pipe]] = pipe
    inv_pipes[pipes[pipe][::-1]] = pipe
opposites = {'N': 'S', 'S': 'N', 'E': 'W', 'W': 'E'}


@dataclass
class Node:
    x: int
    y: int
    pipe: str
    distance: int

    def __post_init__(self):
        self.neighbors = {'N': None, 'E': None, 'S': None, 'W': None}


def find_start(grid: List[str]) -> Tuple[int, int]:
    for y, row in enumerate(grid):
        for x, col in enumerate(row):
            if col == 'S':
                return x, y


def make_network(grid: List[str]) -> Dict[Tuple[int, int], Node]:
    (x0, y0) = find_start(grid)
    x, y = x0, y0
    node = Node(x, y, 'S', 0)
    network = {(x, y): node}

    for dir in dirs:
        dx, dy = dirs[dir]
        next_x, next_y = x + dx, y + dy
        if next_x < 0 or next_x >= len(grid[0]) or next_y < 0 or next_y >= len(grid):
            continue

        if grid[next_y][next_x] in pipes and opposites[dir] in pipes[grid[next_y][next_x]]:
            next_node = Node(next_x, next_y, grid[next_y][next_x], 1)
            node.neighbors[dir] = next_node
            next_node.neighbors[opposites[dir]] = node

            network[(next_x, next_y)] = next_node

            break

    node = next_node
    x, y = node.x, node.y
    from_dir = opposites[dir]
    pipe = node.pipe

    while True:
        to_dir = pipes[pipe].replace(from_dir, '')
        dx, dy = dirs[to_dir]
        next_x, next_y = x + dx, y + dy
        if (next_x, next_y) in network:
            if network[(next_x, next_y)].pipe != 'S':
                raise Exception('Something went wrong')
            start_node = network[(next_x, next_y)]
            node.neighbors[to_dir] = start_node
            start_node.neighbors[opposites[to_dir]] = node
            break
        else:
            next_node = Node(next_x, next_y, grid[next_y][next_x], node.distance + 1)
            node.neighbors[to_dir] = next_node
            next_node.neighbors[opposites[to_dir]] = node

            network[(next_x, next_y)] = next_node
            node = next_node
            x, y = node.x, node.y
            from_dir = opposites[to_dir]
            pipe = node.pipe
    
    max_dist = (max(node.distance for node in network.values()) + 1) // 2

    for node in network.values():
        node.distance = node.distance if node.distance <= max_dist else 2 * max_dist - node.distance
    
    start_node = network[(x0, y0)]
    start_node.pipe = inv_pipes[''.join([dir for dir in start_node.neighbors if start_node.neighbors[dir] is not None])]

    return network


def is_interior(x, y, grid, network) -> bool:
    # Trying for the ray tracing algorithm here, but it's tough around "corners"
    dir = 'N'
    n_crossings = 0
    dx, dy = dirs[dir]
    while True:
        next_x, next_y = x + dx, y + dy
        if next_x < 0 or next_x >= len(grid[0]) or next_y < 0 or next_y >= len(grid):
            break
        if (next_x, next_y) in network and network[(next_x, next_y)].pipe in 'LJ7F-':
            n_crossings += 1
        x, y = next_x, next_y

    if n_crossings % 2 == 0:
        return False
    else:
        return True        


def part1(test_input: List[str]) -> int:
    network = make_network(test_input)
    return max(node.distance for node in network.values())


def part2(test_input: List[str]) -> int:
    network = make_network(test_input)
    interior_nodes = 0
    for y, row in enumerate(test_input):
        for x, col in enumerate(row):
            if (x, y) not in network and is_interior(x, y, test_input, network):
                interior_nodes += 1
    return interior_nodes


if __name__ == '__main__':
    ### THE TESTS
    test_input1 = '''.....
.S-7.
.|.|.
.L-J.
.....'''.split('\n')
    test_input2 = '''-L|F7
7S-7|
L|7||
-L-J|
L|-JF'''.split('\n')
    test_input3 = '''..F7.
.FJ|.
SJ.L7
|F--J
LJ...'''.split('\n')

    assert part1(test_input1) == 4
    assert part1(test_input2) == 4
    assert part1(test_input3) == 8


    test_input4 = '''...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
...........'''.split('\n')
    assert part2(test_input4) == 4

    test_input5 = '''.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ...'''.split('\n')
    assert part2(test_input5) == 8

    ### THE REAL THING
    puzzle_input = helper.read_input_lines()
    print(f'Part 1: {part1(puzzle_input)}')
    print(f'Part 2: {part2(puzzle_input)}')
