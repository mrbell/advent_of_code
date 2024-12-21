from typing import List, Optional, Tuple
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
    cache = {}  # Cache to store the cost of each location and direction
    
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
    
    def print(self, path: Optional[List[Tuple[Tuple[int, int], str]]] = None):
        to_plot = []
        for i, row in enumerate(self.maze):
            to_plot_row = []
            for j, c in enumerate(row):
                to_plot_row.append(c)
            to_plot.append(to_plot_row)
            
        if path:
            for location, direction in path:
                match direction:
                    case 'N': 
                        mychar = '^'
                    case 'S':
                        mychar = 'v'
                    case 'E':
                        mychar = '>'
                    case 'W':
                        mychar = '<'
                to_plot[location[0]][location[1]] = mychar
        
        to_plot = [''.join(row) for row in to_plot]
        print('\n'.join(row for row in to_plot))


def fine_ill_use_dijkstra(maze: Maze):
    costs = {}
    prev = {}  # TODO: Modify to store multiple previous locations if equal cost
    Q = []
    for i, row in enumerate(maze.maze):
        for j, c in enumerate(row):
            if c == wall_char:
                continue
            for direction in directions:
                step_in_direction = direction_steps[direction]
                if (maze.maze[i + step_in_direction[0]][j + step_in_direction[1]] != wall_char) or (
                    maze.maze[i - step_in_direction[0]][j - step_in_direction[1]] != wall_char
                ):
                    # Must not have a wall behind or in front to make this a viable location/direction
                    costs[((i, j), direction)] = float('inf')
                    prev[((i, j), direction)] = None
                    Q.append(((i, j), direction))
    costs[(maze.start, 'E')] = 0
    prev[(maze.start, 'E')] = None
    if (maze.start, 'E') not in Q:
        Q.append((maze.start, 'E'))

    Q = set(Q)

    while Q:  
        # print(len(Q))
        u = min(Q, key=lambda x: costs[x])
        (i, j), direction = u
        Q.remove(u)

        neighbors = [
            ((i + direction_steps[direction][0], j + direction_steps[direction][1]), direction),
            ((i, j), directions[(directions.index(direction) + 1) % 4]),
            ((i, j), directions[(directions.index(direction) - 1) % 4])
        ]

        for neighbor in neighbors:        
            if neighbor not in Q:
                continue
            alt = costs[u] + step_cost if neighbor[1] == direction else costs[u] + turn_cost
            if alt < costs[neighbor]:
                costs[neighbor] = alt
                prev[neighbor] = [u]
            elif alt == costs[neighbor]:
                if prev[neighbor] is None:
                    prev[neighbor] = []
                prev[neighbor].append(u)
        
    return costs, prev


def walk_back_from(start_node, prev, end_node, the_path):
    the_path = list(the_path) + [start_node]
    if start_node == end_node:
        return the_path
    other_nodes = prev[start_node]
    for other_node in other_nodes:
        new_path = walk_back_from(other_node, prev, end_node, the_path)
        the_path = set(new_path).union(the_path)
    return the_path



def find_shortest_paths(maze: Maze, costs, prev):
    path_nodes = []
    end_costs = [(costs[(maze.end, direction)], direction) for direction in directions if (maze.end, direction) in costs]
    min_cost, end_direction = min(end_costs)
    end_nodes = [k for k in costs if k[0] == maze.end and costs[k] == min_cost]

    for node in end_nodes:
        the_path = []
        path_nodes.extend(walk_back_from(node, prev, (maze.start, 'E'), the_path))
    
    return path_nodes


def navigate_maze(
    maze: Maze, 
    location: Tuple[int, int], 
    direction: str, 
    visited: List[Tuple[Tuple[int, int], str]],
    cost: int
) -> int:
    
    visited = visited.copy()
    visited.append((location, direction))
    
    maze.print(visited)
    
    if location == maze.end:
        return cost
    
    costs = []

    next_location = (location[0] + direction_steps[direction][0], location[1] + direction_steps[direction][1])
    if maze.maze[next_location[0]][next_location[1]] != wall_char and next_location not in [loc for loc, _ in visited]:
        cost_to_move = cost + step_cost
        if (next_location, direction) not in maze.cache or maze.cache[(next_location, direction)] > cost_to_move:
            maze.cache[(next_location, direction)] = cost_to_move
            fwd_cost = navigate_maze(maze, next_location, direction, visited, cost_to_move)
            costs.append(fwd_cost)
            visited.append((next_location, direction))

    for new_dir in [-1, 1]:
        new_direction = directions[(directions.index(direction) + new_dir) % 4]
        next_location = (location[0] + direction_steps[new_direction][0], location[1] + direction_steps[new_direction][1])
        if maze.maze[next_location[0]][next_location[1]] != wall_char and next_location not in [loc for loc, _ in visited]:
            cost_to_move = cost + turn_cost
            if (location, new_direction) not in maze.cache or maze.cache[(location, new_direction)] > cost_to_move:
                maze.cache[(location, new_direction)] = cost_to_move
                costs.append(navigate_maze(maze, location, new_direction, visited, cost_to_move))
                visited.append((location, new_direction))
     
    if len(costs) == 0:
        # Return ininity cost if a deadend is reached
        return float('inf')

    return min(costs)


def part1_not_working(puzzle_input: List[str]) -> int:
    maze = Maze(puzzle_input)
    return navigate_maze(maze, maze.start, 'E', [], 0)


def part1(puzzle_input: List[str]) -> int:
    import time 
    maze = Maze(puzzle_input)
    t0 = time.time()
    costs, prev = fine_ill_use_dijkstra(maze)
    print(f"Time to execute: {time.time() - t0:.2f} s")
    end_costs = [costs[(maze.end, direction)] for direction in directions if (maze.end, direction) in costs]
    return min(end_costs)


def part2(puzzle_input: List[str]) -> int:
    maze = Maze(puzzle_input)
    costs, prev = fine_ill_use_dijkstra(maze)

    the_paths = find_shortest_paths(maze, costs, prev)

    unique_nodes = set([p[0] for p in the_paths])

    return len(unique_nodes)


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

    result = part2(example_input)
    helper.check(result, 45)

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

    result = part2(example_input)
    helper.check(result, 64)

    ### THE REAL THING
    puzzle_input = helper.read_input_lines()
    print(f'Part 1: {part1(puzzle_input)}')
    print(f'Part 2: {part2(puzzle_input)}')
