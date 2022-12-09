from typing import List, Tuple
import helper


def clip(pos: Tuple[int, int], thresh: int=1) -> Tuple[int, int]:
    new_pos = []
    for v in pos:
        v_sign = v // abs(v) if v != 0 else 1
        new_v = v_sign * min(abs(v), thresh)
        new_pos.append(new_v)
        
    return tuple(new_pos) 


class Rope(object):
    def __init__(self):
        self.head_position = (0, 0)
        self.tail_position = (0, 0)
        self.tail_positions = [self.tail_position]
    
    def move(self, command: str):
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
            # print(f'Head: {self.head_position}, Tail: {self.tail_position}')

    def move_tail(self):
        head_tail_offset = (self.head_position[0] - self.tail_position[0], self.head_position[1] - self.tail_position[1])
        if abs(head_tail_offset[0]) > 1 or abs(head_tail_offset[1]) > 1:
            head_tail_offset = clip(head_tail_offset)
            self.tail_position = (self.tail_position[0] + head_tail_offset[0], self.tail_position[1] + head_tail_offset[1])
            self.tail_positions.append(self.tail_position)
        

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
    assert len(set(rope.tail_positions)) == 13

    ### THE REAL THING
    puzzle_input = helper.read_input_lines()
    rope = Rope()
    for move in puzzle_input:
        rope.move(move)
    print(f'Part 1: {len(set(rope.tail_positions))}')
    print(f'Part 2: {""}')
