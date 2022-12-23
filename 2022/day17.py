from typing import List, Tuple, Set, Optional
import helper


rock_types = {
    0: ((0, 0), (1, 0), (2, 0), (3, 0)),
    1: ((1, 0), (0, 1), (1, 1), (2, 1), (1, 2)),
    2: ((0, 0), (1, 0), (2, 0), (2, 1), (2, 2)),
    3: ((0, 0), (0, 1), (0, 2), (0, 3)),
    4: ((0, 0), (1, 0), (0, 1), (1, 1))
}


class Rock(object):
    def __init__(self, type: int, starting_height: int):
        self.height = starting_height
        self.lateral = 2
        self._positions = rock_types[type]

    @property
    def positions(self) -> List[Tuple[int, int]]:
        return [(x + self.lateral, y + self.height) for x, y in self._positions]

        
class Chamber(object):
    def __init__(self, width: int):
        self.width = width
        self.height = 0
        self.rocks: Set[Tuple[int, int]] = set()
    
    def add_rocks(self, rock: 'Rock'):
        self.rocks = self.rocks.union(rock.positions)
        self.height = max(y for _, y in self.rocks) + 1
    
    def collision(self, rock: 'Rock') -> bool:
        return any(
            (p in self.rocks) or (p[0] < 0) or (p[0] >= self.width) or (p[1] < 0) 
            for p in rock.positions
        )

    def display(self, rock: Optional['Rock']=None, indent: str='') -> str:

        rock_positions = self.rocks
        height = self.height
        if rock is not None:
            rock_positions = rock_positions.union(rock.positions)
            height = max(y for _, y in rock_positions)

        return indent + f'\n{indent}'.join(
            '|' + ''.join('#' if (x, y) in rock_positions else '.' for x in range(self.width)) + '|'
            for y in range(height, -1, -1)
        ) + f'\n{indent}+{"-" * self.width}+'


def simulation(moves: str, n_rocks: int=2022) -> int:
    chamber = Chamber(7)
    n_rock_types = len(rock_types)
    move_num = 0
    n_moves = len(moves)
    rock_num = 0

    rock_height_offset = 3

    while rock_num < n_rocks:
        rock = Rock(rock_num % n_rock_types, chamber.height + rock_height_offset)
        rock_num += 1
        step = 0

        if rock_num <= 10:
            print(f'Rock {rock_num}:')
            print(chamber.display(rock))
            print()
        
        while True:
            if step % 2 == 0:  # Wind pushes the rock
                wind_movement = 1 if moves[move_num % n_moves] == '>' else -1
                move_num += 1
                rock.lateral += wind_movement
                if chamber.collision(rock):
                    # Hit a wall or something, move back
                    rock.lateral -= wind_movement
            else:  # The rock falls
                rock.height -= 1
                if chamber.collision(rock):
                    # Hit the ground, add to the chamber
                    rock.height += 1
                    chamber.add_rocks(rock)
                    step = 0
                    break
            
            if rock_num <= 2:
                print(f'  Step {step}:')
                print(chamber.display(rock, '  '))
                print()

            step += 1

    return chamber.height


if __name__ == '__main__':
    ### THE TESTS
    test_input = '''>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>'''
    max_height = simulation(test_input)
    assert max_height == 3068

    ### THE REAL THING
    puzzle_input = helper.read_input()
    max_height = simulation(puzzle_input)
    print(f'Part 1: {max_height}')
    print(f'Part 2: {""}')
