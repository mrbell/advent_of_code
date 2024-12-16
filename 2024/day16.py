from typing import List, Tuple
from dataclasses import dataclass
import helper

directions = ['N', 'E', 'S', 'W']
direction_steps = {'N': (-1, 0), 'E': (0, 1), 'S': (1, 0), 'W': (0, -1)}
wall_char = '#'
step_cost = 1
turn_cost = 1000


@dataclass
class Maze:
    maze: List[str]
    
    def __post_init__(self):
        self.start = self.find_start()
        self.end = self.find_end()
    
    def _find_char(self, char):
        for i, row in enumerate(self.maze):
            for j, c in enumerate(row):
                if c == char:
                    return (i, j)

    def find_start(self):
        return self._find_char('S')

    def find_end(self):
        return self._find_char('E')
    
    def print(self, location=None, direction=None):
        match direction:
            case 'N': 
                mychar = '^'
            case 'S':
                mychar = 'v'
            case 'E':
                mychar = '>'
            case 'W':
                mychar = '<'
        to_plot = []
        for i, row in enumerate(self.maze):
            to_plot_row = []
            for j, c in enumerate(row):
                if (i, j) == location:
                    to_plot_row.append(mychar)
                elif c in ('S', 'E'):
                    to_plot_row.append('.')
                else:
                    to_plot_row.append(c)
            to_plot.append(''.join(to_plot_row))
        print('\n'.join(row for row in to_plot))


def navigate_maze(
    maze: Maze, 
    location: Tuple[int, int], 
    direction: str, 
    visited: List[Tuple[Tuple[int, int], str]],
    cost: int
) -> int:
    
    maze.print(location, direction)

    visited = visited.copy()
    visited.append((location, direction))
    
    if location == maze.end:
        return cost
    
    costs = []

    next_location = (location[0] + direction_steps[direction][0], location[1] + direction_steps[direction][1])
    if maze.maze[next_location[0]][next_location[1]] != wall_char and next_location not in [loc for loc, _ in visited]:
        fwd_cost = navigate_maze(maze, next_location, direction, visited, cost + step_cost) 
        costs.append(fwd_cost)

    for new_dir in [-1, 1]:
        new_direction = directions[(directions.index(direction) + new_dir) % 4]
        next_location = (location[0] + direction_steps[new_direction][0], location[1] + direction_steps[new_direction][1])
        if maze.maze[next_location[0]][next_location[1]] != wall_char and next_location not in [loc for loc, _ in visited]:
            costs.append(navigate_maze(maze, location, new_direction, visited, cost + turn_cost))
     
    if len(costs) == 0:
        # Return ininity cost if a deadend is reached
        return float('inf')

    return min(costs)


def part1(puzzle_input: List[str]) -> int:
    maze = Maze(puzzle_input)
    return navigate_maze(maze, maze.start, 'E', [], 0)


if __name__ == '__main__':
    ### THE TESTS
    example_input = '''###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############'''.split('\n')
    result = part1(example_input)
    helper.check(result, 7036)

    example_input = '''#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################'''.split('\n')
    result = part1(example_input)
    helper.check(result, 11048)

    ### THE REAL THING
    puzzle_input = helper.read_input_lines()
    print(f'Part 1: {part1(puzzle_input)}')
    print(f'Part 2: {""}')
