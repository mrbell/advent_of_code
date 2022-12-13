from typing import List, Tuple, Optional
import sys
import helper


class Map(object):
    def __init__(self, map: List[str]):
        self.map = map
        self.width = len(map[0])
        self.height = len(map)

        self.destination: Optional[Tuple[int, int]] = None
        self.location: Optional[Tuple[int, int]] = None       

        for i, row in enumerate(map):
            for j, char in enumerate(row):
                if char == 'S':
                    self.location = (i, j)
                elif char == 'E':
                    self.destination = (i, j)

        if self.location is not None:
            self.map[self.location[0]] = self.map[self.location[0]].replace('S', 'a').replace('E', 'z')
        if self.destination is not None:
            self.map[self.destination[0]] = self.map[self.destination[0]].replace('S', 'a').replace('E', 'z')

        self.explored = {}

    def __str__(self):
        return '\n'.join(self.map)

    def find_path(
        self, 
        location: Tuple[int, int], 
        path: List[Tuple[int, int]] 
    ) -> List[Tuple[int, int]]:
        '''
        DOESN'T WORK!
        '''

        starting_path_length = len(path) 

        if location == map.destination:
            self.explored[location] = []
            return path

        row, col = location

        possible_paths = []

        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        for (drow, dcol) in directions:

            new_row = row + drow
            new_col = col + dcol

            if new_row < 0 or new_row >= self.height or new_col < 0 or new_col >= self.width:
                continue

            current_height = ord(self.map[row][col])
            new_height = ord(self.map[new_row][new_col])
            possible_path = []

            if (new_height - current_height) > 1 or (new_row, new_col) in path:  
                continue
            elif (new_row, new_col) in self.explored and self.explored[(new_row, new_col)] is None:
                continue
            elif (new_row, new_col) in self.explored:
                possible_path = path + [(new_row, new_col)] + self.explored[(new_row, new_col)]
            else:
                possible_path = self.find_path((new_row, new_col), path + [(new_row, new_col)])

            if len(possible_path) > 0:
                possible_paths.append(possible_path)

        if len(possible_paths) == 0:
            # Hit a dead end
            self.explored[location] = None
            return []
        
        possible_paths.sort(key=lambda x: len(x))

        shortest_path = possible_paths[0]

        self.explored[location] = shortest_path[starting_path_length:]

        return shortest_path


def get_neighboring_points(point: Tuple[int, int]) -> List[Tuple[int, int]]:
    return [
        (point[0] + 1, point[1]),
        (point[0] - 1, point[1]),
        (point[0], point[1] - 1),
        (point[0], point[1] + 1)
    ]


def is_oob(height_map: Map, point: Tuple[int, int]) -> bool:
    return not(0 <= point[0] < height_map.height and 0 <= point[1] < height_map.width)


def find_shortest_path(elev_map: Map) -> int:
    '''
    Code up Dijkstra's algorithm.
    '''
    visited_points = [[False] * len(elev_map.map[0]) for _ in range(len(elev_map.map))]

    least_path_risks = [[1e9] * len(elev_map.map[0]) for _ in range(len(elev_map.map))]

    current_node = elev_map.location
    destination_node = elev_map.destination 
    
    least_path_risks[current_node[0]][current_node[1]] = 0

    while True:
        current_height = ord(elev_map.map[current_node[0]][current_node[1]])
        neighbors = get_neighboring_points(current_node)
        neighbors = [
            n for n in neighbors 
            if not is_oob(elev_map, n) 
            and not visited_points[n[0]][n[1]]
            and not (ord(elev_map.map[n[0]][n[1]]) - current_height > 1)
        ]

        for n in neighbors:
            tentative_dist = 1 + least_path_risks[current_node[0]][current_node[1]]
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


def find_best_start(map: Map) -> Tuple[Tuple[int, int], int]:
    # FIXME: Not the best way to do this... I should be able to look at the map of least path risks in 
    # Dijsktra's algorithm and find the best start point from there with one pass through the map.

    shortest_path_start = None
    shortest_path = 1e9

    for row_num, row in enumerate(map.map):
        
        for col_num, char in enumerate(row):
            print(f'{char} ', end='')
            sys.stdout.flush()
            if char == 'a':
                start_point = (row_num, col_num)
                
                new_map = Map(map.map)
                new_map.location = start_point
                new_map.destination = map.destination

                path = find_shortest_path(new_map)
                if path < shortest_path:
                    shortest_path = path
                    shortest_path_start = start_point
        print()

    return shortest_path_start, shortest_path


if __name__ == '__main__':
    ### THE TESTS
    test_map = '''Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi'''.split('\n')
    map = Map(test_map)
    print(map, end='\n\n')

    path = find_shortest_path(map)
    assert path == 31
    start_point, path = find_best_start(map)
    assert path == 29

    ### THE REAL THING
    puzzle_input = helper.read_input_lines()
    map = Map(puzzle_input)
    path = find_shortest_path(map) 
    print(f'Part 1: {path}')

    start_point, path = find_best_start(map)
    print(f'Part 2: {path}')
