from typing import List, Tuple, Callable
import helper


def clip(pos: Tuple[int, int], thresh: int=1) -> Tuple[int, int]:
    new_pos = []
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
            self.move_tail()
            if verbose:
                print_func(self)

    def move_tail(self):

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
        rope.move(move)
    assert len(set(rope.tail_positions_visited)) == 1

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
