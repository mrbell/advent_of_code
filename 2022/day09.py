from typing import List, Tuple, Callable
import helper


def clip(pos: Tuple[int, int], thresh: int=1) -> Tuple[int, int]:
    new_pos: List[int] = []
    for v in pos:
        v_sign = v // abs(v) if v != 0 else 1
        new_v = v_sign * min(abs(v), thresh)
        new_pos.append(new_v)
    return tuple(new_pos) 


class Rope(object):
    def __init__(self, n_knots: int=2):
        self.head_position = (0, 0)
        self.tail_positions = [(0, 0) for _ in range(n_knots - 1)]
        self.tail_positions_visited = [self.tail_positions[-1]]
    
    def move(self, command: str, print_func: Callable=print, verbose: bool=False):
        direction, distance = command[0], int(command[1:])
        for _ in range(distance): 
            if direction == 'R':
                self.head_position = (self.head_position[0] + 1, self.head_position[1])
            elif direction == 'L':
                self.head_position = (self.head_position[0] - 1, self.head_position[1])
            elif direction == 'U':
                self.head_position = (self.head_position[0], self.head_position[1] + 1)
            elif direction == 'D':
                self.head_position = (self.head_position[0], self.head_position[1] - 1)
            else:
                raise ValueError(f'Unknown direction: {direction}')
            self._move_tail()
        if verbose:
            print_func(self)

    def _move_tail(self):

        for i, tail in enumerate(self.tail_positions):
            if i == 0:
                lead = self.head_position
            else:
                lead = self.tail_positions[i - 1]

            head_tail_offset = (lead[0] - tail[0], lead[1] - tail[1])
            if abs(head_tail_offset[0]) > 1 or abs(head_tail_offset[1]) > 1:
                head_tail_offset = clip(head_tail_offset)
                self.tail_positions[i] = (
                    self.tail_positions[i][0] + head_tail_offset[0], 
                    self.tail_positions[i][1] + head_tail_offset[1]
                )

        self.tail_positions_visited.append(self.tail_positions[-1])
        

def display(rope: Rope, grid_x: int=6, grid_y: int=5, init_x: int=0, init_y: int=0):
    
    grid = [['.' for _ in range(grid_x)] for _ in range(grid_y)]
    grid[init_y][init_x] = 's'

    for i, tail in enumerate(rope.tail_positions[::-1]):
        grid[init_y + tail[1]][tail[0] + init_x] = str(len(rope.tail_positions) - i)
    grid[init_y + rope.head_position[1]][rope.head_position[0] + init_x] = 'H'

    for row in grid[::-1]:
        print(''.join(row))
    print()


if __name__ == '__main__':
    ### THE TESTS
    test_moves = '''R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2'''.split('\n')
    rope = Rope()
    for move in test_moves:
        rope.move(move)
    assert len(set(rope.tail_positions_visited)) == 13

    rope = Rope(n_knots=10)
    for move in test_moves:
        rope.move(move, verbose=True, print_func=lambda x: display(x, 6, 5))
    assert len(set(rope.tail_positions_visited)) == 1

    longer_test_moves = '''R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20'''.split('\n')
    rope = Rope(10)
    for move in longer_test_moves:
        rope.move(move, verbose=True, print_func=lambda x: display(x, 26, 21, 11, 5))
    assert len(set(rope.tail_positions_visited)) == 36  

    ### THE REAL THING
    puzzle_input = helper.read_input_lines()
    rope = Rope()
    for move in puzzle_input:
        rope.move(move)
    print(f'Part 1: {len(set(rope.tail_positions_visited))}')
    rope = Rope(n_knots=10)
    for move in puzzle_input:
        rope.move(move)
    print(f'Part 2: {len(set(rope.tail_positions_visited))}')
