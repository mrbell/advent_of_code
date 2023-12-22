from typing import List, Tuple, Optional
import helper


directions = {'up': (-1, 0), 'down': (1, 0), 'left': (0, -1), 'right': (0, 1)}


class Beam(object):
    def __init__(self, start_position: Tuple[int, int], start_direction: str):
        self.start_position = start_position
        self.start_direction = start_direction
        self.position = start_position
        self.direction = start_direction
        self.positions = [start_position]
        self.followed = False

    def __repr__(self):
        return f'Beam({self.start_position}, {self.start_direction})'
    
    def __eq__(self, other: 'Beam') -> bool:
        return (
            self.start_position == other.start_position and 
            self.start_direction == other.start_direction
        )

    def turn(self, mirror: str) -> None:
        if self.direction == 'up' and mirror == '/':
            self.direction = 'right'
        elif self.direction == 'up' and mirror == '\\':
            self.direction = 'left'
        elif self.direction == 'down' and mirror == '/':
            self.direction = 'left'
        elif self.direction == 'down' and mirror == '\\':
            self.direction = 'right'
        elif self.direction == 'left' and mirror == '/':
            self.direction = 'down'
        elif self.direction == 'left' and mirror == '\\':
            self.direction = 'up'
        elif self.direction == 'right' and mirror == '/':
            self.direction = 'up'
        elif self.direction == 'right' and mirror == '\\':
            self.direction = 'down'

    def step(self, contraption: List[str]) -> Optional[str]:
        if contraption[self.position[0]][self.position[1]] in r'/\\':
            self.turn(contraption[self.position[0]][self.position[1]]) 
            
        new_position = tuple(sum(x) for x in zip(self.position, directions[self.direction])) 
        self.position = new_position
        if (
            self.position[0] < 0 or self.position[0] >= len(contraption) or 
            self.position[1] < 0 or self.position[1] >= len(contraption[0])
        ):
            return None
        self.positions.append(new_position)
        return contraption[new_position[0]][new_position[1]]

    def follow(self, contraption: List[str]) -> List['Beam']:
        new_beams = []
        while True:
            next_step = self.step(contraption)
            if next_step is None:
                # We've fallen off the edge    
                break
            elif self.direction in ['left', 'right'] and next_step == '|':
                # split vertically
                new_beams = [Beam(self.position, 'up'), Beam(self.position, 'down')]
                break
            elif self.direction in ['up', 'down'] and next_step == '-':
                # split horizontally
                new_beams = [Beam(self.position, 'left'), Beam(self.position, 'right')]
                break
        self.followed = True
        return new_beams


def part1(
        contraption: List[str], 
        start_pos: Optional[Tuple[int, int]]=None, 
        start_dir: Optional[str]=None
) -> int:
    if start_pos is None:
        start_pos = (0, 0)
    if start_dir is None:
        start_dir = 'right'
    beams = [Beam(start_pos, start_dir)]
    followed_beams = []
    while len(beams) > 0:
        beam = beams.pop(0)     
        
        new_beams = beam.follow(contraption)
        new_beams = [b for b in new_beams if not any(b == fb for fb in followed_beams)]
        beams.extend(new_beams)
        
        followed_beams.append(beam)
        
    energized_positions = []
    for beam in followed_beams:
        energized_positions.extend(beam.positions)

    return len(set(energized_positions))


def part2(contraption: List[str]) -> int:
    
    results = {}

    for col, dir in zip([0, len(contraption[0])-1], ['right', 'left']):
        for row in range(len(contraption)):
            result = part1(contraption, (row, col), dir)
            results[(row, col, dir)] = result

    for row, dir in zip([0, len(contraption)-1], ['down', 'up']):
        for col in range(len(contraption[0])):
            result = part1(contraption, (row, col), dir)
            results[(row, col, dir)] = result
    
    return max(results.values())


if __name__ == '__main__':
    ### THE TESTS
    test_input = r'''.|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|....'''.splitlines()
    result = part1(test_input)
    print(result)
    assert result == 46
    assert part1(test_input, (0, 3), 'down') == 51
    assert part2(test_input) == 51

    ### THE REAL THING
    puzzle_input = helper.read_input_lines()
    print(f'Part 1: {part1(puzzle_input)}')
    print(f'Part 2: {part2(puzzle_input)}')
