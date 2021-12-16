from ast import parse
from typing import List, Tuple
import helper
from day09 import get_neighboring_points, is_oob


def parse_risk_levels(risk_level_map: str) -> List[List[int]]:
    return [
        [
            int(val) for val in row.strip()
        ] for row in risk_level_map.strip().split('\n')
    ]


to_add = [
    [0, 1, 2, 3, 4],
    [1, 2, 3, 4, 5],
    [2, 3, 4, 5, 6],
    [3, 4, 5, 6, 7],
    [4, 5, 6, 7, 8]
]


def make_full_map(risk_map: List[List[int]]) -> List[List[int]]:

    full_map = [[0] * (len(risk_map[0]) * 5) for _ in range(len(risk_map) * 5)]

    for super_row in range(5):
        for super_col in range(5):
            add_this = to_add[super_row][super_col]
            for row_num, row in enumerate(risk_map):
                for col_num, val in enumerate(row):
                    new_val = val + add_this
                    new_val = new_val if new_val <= 9 else (new_val - 9)
                    full_map[
                        super_row * len(risk_map) + row_num
                    ][
                        super_col * len(risk_map[0]) + col_num
                    ] = new_val
    
    return full_map


def find_shortest_path_risk(risk_map: List[List[int]]) -> int:
    '''
    Code up Dijkstra's algorithm, using "risk" as a measure of distance between nodes.
    '''
    visited_points = [[False] * len(risk_map[0]) for _ in range(len(risk_map))]

    least_path_risks = [[1e9] * len(risk_map[0]) for _ in range(len(risk_map))]
    least_path_risks[0][0] = 0

    current_node = (0, 0)
    destination_node = (len(risk_map) - 1, len(risk_map[0]) - 1)

    while True:
        neighbors = get_neighboring_points(current_node)
        neighbors = [
            n for n in neighbors 
            if not is_oob(risk_map, n) 
            and not visited_points[n[0]][n[1]]
        ]

        for n in neighbors:
            tentative_dist = risk_map[n[0]][n[1]] + least_path_risks[current_node[0]][current_node[1]]
            if tentative_dist < least_path_risks[n[0]][n[1]]:
                least_path_risks[n[0]][n[1]] = tentative_dist
        
        visited_points[current_node[0]][current_node[1]] = True

        if visited_points[destination_node[0]][destination_node[1]]:
            break
        else:
            unvisited_node_risks = []
            for row_num, row in enumerate(visited_points):
                for col_num, is_visited in enumerate(row):
                    if not is_visited:
                        unvisited_node_risks.append(((row_num, col_num), least_path_risks[row_num][col_num]))
            current_node = min(unvisited_node_risks, key=lambda x: x[1])[0]

    return least_path_risks[destination_node[0]][destination_node[1]]


if __name__ == '__main__':
    ### THE TESTS
    example_risk_levels = '''1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581
'''
    risk_levels = parse_risk_levels(example_risk_levels)
    assert find_shortest_path_risk(risk_levels) == 40

    full_map = make_full_map(risk_levels)

    assert find_shortest_path_risk(full_map) == 315

    ### THE REAL THING
    puzzle_input = helper.read_input()
    risk_levels = parse_risk_levels(puzzle_input)
    print(f'Part 1: {find_shortest_path_risk(risk_levels)}')
    full_map = make_full_map(risk_levels)
    print(f'Part 2: {find_shortest_path_risk(full_map)}')
