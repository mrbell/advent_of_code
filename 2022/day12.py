from typing import List, Tuple
import sys
import helper


class Map(object):
    def __init__(self, map: List[str]):
        self.map = map
        self.width = len(map[0])
        self.height = len(map)

        self.destination: Tuple[int, int]
        self.location: Tuple[int, int]        

        for i, row in enumerate(map):
            for j, char in enumerate(row):
                if char == 'S':
                    self.location = (i, j)
                elif char == 'E':
                    self.destination = (i, j)

        self.map[self.location[0]] = self.map[self.location[0]].replace('S', 'a').replace('E', 'z')
        self.map[self.destination[0]] = self.map[self.destination[0]].replace('S', 'a').replace('E', 'z')

    def __str__(self):
        return '\n'.join(self.map)


n_calls = 0

def find_path(map: Map, location: Tuple[int, int], path: List[Tuple[int, int]], verbose=False) -> List[Tuple[int, int]]:

    if verbose:
        global n_calls 
        n_calls += 1
        if (n_calls) % 10_000 == 0:
            print('.', end='')
            if n_calls % 800_000 == 0:
                print()
            sys.stdout.flush()

    if location == map.destination:
        return path

    row, col = location

    possible_paths = []

    # Create a prioritized list of directions to explore
    # Prioritize moving towards the destination
    to_destination = (map.destination[0] - row, map.destination[1] - col)
    dirs_to_destination = sum(1 for d in to_destination if d != 0)
    directions = []
    if to_destination[0] != 0:
        directions.append((to_destination[0] // abs(to_destination[0]), 0))
    if to_destination[1] != 0:
        directions.append((0, to_destination[1] // abs(to_destination[1])))
    directions.extend(
        list(set([(0, 1), (0, -1), (1, 0), (-1, 0)]).difference(set(directions)))
    )

    for i, (drow, dcol) in enumerate(directions):  # [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        if len(possible_paths) > 0 and i >= dirs_to_destination:
            # Don't move away from the goal unless you have to
            break

        new_row = row + drow
        new_col = col + dcol

        if new_row < 0 or new_row >= map.height or new_col < 0 or new_col >= map.width:
            continue

        current_height = ord(map.map[row][col])
        new_height = ord(map.map[new_row][new_col])
        
        if (new_height - current_height) > 1:  # or (new_height - current_height) < -1:
            continue
        elif (new_row, new_col) in path:
            continue
        else:
            possible_path = find_path(map, (new_row, new_col), path + [(new_row, new_col)], verbose=verbose)
            if len(possible_path) > 0:
                possible_paths.append(possible_path)

    if len(possible_paths) == 0:
        # Hit a dead end
        return []
    
    possible_paths.sort(key=lambda x: len(x))

    return possible_paths[0]
    

if __name__ == '__main__':
    ### THE TESTS
    test_map = '''Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi'''.split('\n')
    map = Map(test_map)
    print(map, end='\n\n')

    path = find_path(map, map.location, [map.location])
    assert (len(path) - 1) == 31

    ### THE REAL THING
    puzzle_input = helper.read_input_lines()
    map = Map(puzzle_input)
    path = find_path(map, map.location, [map.location], verbose=True)
    print(f'Part 1: {len(path) - 1}')
    print(f'Part 2: {""}')
