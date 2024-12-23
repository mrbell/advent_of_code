from typing import List, Tuple, Dict
from dataclasses import dataclass
import helper


@dataclass(frozen=True)
class Cell:
    x: int
    y: int

    def __add__(self, other):
        return Cell(self.x + other.x, self.y + other.y)
    
    def __str__(self):
        return f'({self.x}, {self.y})'


@dataclass
class Maze:
    maze: List[List[str]]
    
    def __post_init__(self):
        self.start = find_start(self)
        self.end = find_end(self)
        self.nx = len(self.maze[0])
        self.ny = len(self.maze)
    
    def __getitem__(self, cell: Cell):
        return self.maze[cell.y][cell.x]
    
    def __setitem__(self, cell: Cell, value: str):
        self.maze[cell.y][cell.x] = value
    
    def make_shortcut(self, cell: Cell) -> 'Maze':
        copy_maze = []
        for row in self.maze:
            copy_maze.append(row.copy())
        new_maze = Maze(copy_maze)
        new_maze[cell] = '.'
        return new_maze


def get_maze(puzzle_input: List[str]) -> Maze:
    maze = []
    for row in puzzle_input:
        new_row = []
        for char in row:
            new_row.append(char)
        maze.append(new_row)
    return Maze(maze)


def _find_char(maze: Maze, char: str):
    for y, row in enumerate(maze.maze):
        for x, c in enumerate(row):
            if c == char:
                return Cell(x, y)


def find_start(maze: Maze):
    return _find_char(maze, 'S')


def find_end(maze: Maze):
    return _find_char(maze, 'E')


def get_neighbors(cell: Cell, maze: Maze) -> List[Cell]:
    directions = [Cell(0, 1), Cell(1, 0), Cell(0, -1), Cell(-1, 0)]
    neighbors = []
    for direction in directions:
        neighbor = cell + direction
        if 0 <= neighbor.x < maze.nx and 0 <= neighbor.y < maze.ny and maze[neighbor] != '#':
            neighbors.append(neighbor)
    return neighbors


def dijstra(maze: Maze) -> Dict[Cell, int]:
    start = maze.start

    costs = {}
    queue = []
    for y, row in enumerate(maze.maze):
        for x, cell_val in enumerate(row):
            if cell_val != '#':
                cell_coords = Cell(x, y)
                costs[cell_coords] = float('inf')
                queue.append(cell_coords)
    costs[start] = 0

    while queue:
        current = min(queue, key=lambda x: costs[x])
        queue.remove(current)
        for neighbor in get_neighbors(current, maze):
            new_cost = costs[current] + 1
            if new_cost < costs[neighbor]:
                costs[neighbor] = new_cost
            
    return costs


def print_map(maze: Maze) -> None:
    for row in maze.maze:
        print(''.join(row))
    

def find_possible_shortcuts(maze: Maze) -> List[Cell]:
    shortcuts = []
    for y, row in enumerate(maze.maze):
        for x, cell_val in enumerate(row):
            if cell_val == '#':
                cell = Cell(x, y)
                neighbors = get_neighbors(cell, maze)
                if len(neighbors) > 1:
                    shortcuts.append(cell)
    return shortcuts


def check_shortcut(maze: Maze, shortcut: Cell, costs: Dict[Cell, int]) -> int:

    neighbors = get_neighbors(shortcut, maze)

    neighbors = sorted(neighbors, key=lambda x: costs[x])

    savings = []

    for i, neighbor in enumerate(neighbors[:-1]):
        for j, neighbor2 in enumerate(neighbors[(i+1):]):
            if costs[neighbor2] - costs[neighbor] > 2:
                # shortcut found            
                savings.append(costs[neighbor2] - costs[neighbor] - 2)
    
    if len(savings) == 0:
        return 0
    elif len(savings) > 1:
        raise ValueError('Multiple savings found')
    
    return savings[0]


def part1(puzzle_input: List[str]) -> int:
    maze = get_maze(puzzle_input)
    costs = dijstra(maze)
    default_length = costs[maze.end]
    possible_shortcuts = find_possible_shortcuts(maze)

    print(default_length, len(possible_shortcuts))
    
    shortcuts = {}

    for i, shortcut in enumerate(possible_shortcuts):
        savings = check_shortcut(maze, shortcut, costs)
        if savings > 0:
            shortcuts[shortcut] = savings
    
    # shortcut_lengths = {}
    # for shortcut in shortcuts:
    #     if shortcuts[shortcut] not in shortcut_lengths:
    #         shortcut_lengths[shortcuts[shortcut]] = 0
    #     shortcut_lengths[shortcuts[shortcut]] += 1

    # print(shortcut_lengths)

    return sum(1 for shortcut in shortcuts if shortcuts[shortcut] >= 100)


if __name__ == '__main__':
    ### THE TESTS
    example_input = '''###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############'''.split('\n')

    result = part1(example_input)
    helper.check(result, 0)

    ### THE REAL THING
    puzzle_input = helper.read_input_lines()
    print(f'Part 1: {part1(puzzle_input)}')
    print(f'Part 2: {""}')
