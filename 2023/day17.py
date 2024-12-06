from typing import List, Tuple, Optional
from day16 import directions
import helper


turns = {
    'right': ['up', 'down', 'right'],
    'left': ['down', 'up', 'left'],
    'up': ['left', 'right', 'up'],
    'down': ['right', 'left', 'down']
}


def go_in_direction(node, direction):
    return tuple(sum(x) for x in zip(node, directions[direction]))


def out_of_bounds(node, heat_loss_map):
    return (
        node[0] < 0 or node[0] >= (len(heat_loss_map) - 1) or 
        node[1] < 0 or node[1] >= (len(heat_loss_map[0]) - 1)
    )


def read_map(node, heat_loss_map):
    return int(heat_loss_map[node[0]][node[1]])


def find_path(
        heat_loss_map: List[str], 
        visit_map: Optional[List[List[int]]]=None,
        start_node: Optional[Tuple[int, int]]=None, 
        direction: str='right', 
        steps_in_dir: int=0
) -> Tuple[List[Tuple[int, int]], int]:
    destination_node = (len(heat_loss_map) - 1, len(heat_loss_map[0]) - 1)
    if start_node is None:
        start_node = (0, 0)
    
    if visit_map is None:
        # Maybe I can track nodes that I've visited already and cut the path off if my current path is longer than 
        # however I got there before? 
        visit_map = [[1e9 for _ in range(len(heat_loss_map[0]))] for _ in range(len(heat_loss_map))]
        visit_map[start_node[0]][start_node[1]] = 0
    
    heat_loss = read_map(start_node, heat_loss_map)

    if start_node == destination_node:
        return [start_node], heat_loss 

    possible_directions = turns[direction]
    if steps_in_dir >= 3:
        possible_directions.remove(direction)

    possible_paths = []
    for possible_direction in possible_directions:
        new_node = go_in_direction(start_node, possible_direction)
        if out_of_bounds(new_node, heat_loss_map):
            continue
        if possible_direction == direction:
            next_steps_in_dir = steps_in_dir + 1
        else:
            next_steps_in_dir = 1
        new_path, new_heat_loss = find_path(
            heat_loss_map, new_node, possible_direction, next_steps_in_dir
        )
        possible_paths.append((new_path, new_heat_loss))
    
    best_path = min(possible_paths, key=lambda x: x[1])

    return [start_node] + best_path[0], best_path[1] + heat_loss
    

def part1(heat_loss_map: List[str]) -> int:
    path, heat_loss = find_path(heat_loss_map)
    return heat_loss - read_map(path[0], heat_loss_map)


if __name__ == '__main__':
    ### THE TESTS
    test_input = '''2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533'''.splitlines()
    assert part1(test_input) == 102

    ### THE REAL THING
    puzzle_input = helper.read_input()
    print(f'Part 1: {""}')
    print(f'Part 2: {""}')
