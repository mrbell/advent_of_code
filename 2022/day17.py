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
        self.rocks: Set[Tuple[int, int]] = set([(x, -1) for x in range(self.width)])
    
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
    
    def _get_max_height_in_column(self, x: int) -> int:
        return max(y for (x_, y) in self.rocks if x_ == x)
    
    def trim(self) -> bool:
        # Remove buried rocks 
        column_heights = [self._get_max_height_in_column(x) for x in range(self.width)]
        new_floor = min(column_heights)
        self.rocks = {(x, y) for (x, y) in self.rocks if y >= new_floor}

        if max(column_heights) == new_floor:
            return True
        else:
            return False


def simulation(moves: str, n_rocks: int=2022) -> int:
    chamber = Chamber(7)
    n_rock_types = len(rock_types)
    move_num = 0
    n_moves = len(moves)
    rock_num = 0

    rock_height_offset = 3

    new_level_floor_at = {}
    found_cycle = False

    while rock_num < n_rocks:
        rock = Rock(rock_num % n_rock_types, chamber.height + rock_height_offset)
        rock_num += 1
        step = 0

        # if rock_num <= 10:
        #     print(f'Rock {rock_num}:')
        #     print(chamber.display(rock))
        #     print()
        
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
            
            # if rock_num <= 2:
            #     print(f'  Step {step}:')
            #     print(chamber.display(rock, '  '))
            #     print()

            step += 1

        if chamber.trim():  # Floor is flat
            if ((rock_num % n_rock_types) == 1) and (move_num % n_moves) not in new_level_floor_at:
                new_level_floor_at[move_num % n_moves] = {'height': chamber.height, 'rock_num': rock_num, 'move_num': move_num}
                # print(new_level_floor_at)
            elif not found_cycle and ((rock_num % n_rock_types) == 1):
                found_cycle = True
                # print(f'Found a cycle at {move_num % n_moves}!')
                # print(f'Height: {chamber.height} Rock number: {rock_num} Move number: {move_num}') 
                
                last_height = new_level_floor_at[move_num % n_moves]['height']
                height_added_per_cycle = chamber.height - last_height
                # print(f'Height added per cycle: {height_added_per_cycle}')

                last_rock_num = new_level_floor_at[move_num % n_moves]['rock_num']
                rock_num_added_per_cycle = rock_num - last_rock_num
                cycles_to_go = (n_rocks - rock_num) // rock_num_added_per_cycle
                # print(f'Rock number added per cycle: {rock_num_added_per_cycle}')
                # print(f'Cycles to go: {cycles_to_go}')


                last_move_num = new_level_floor_at[move_num % n_moves]['move_num']
                move_num_added_per_cycle = move_num - last_move_num
                # print(f'Move number added per cycle: {move_num_added_per_cycle}')

                chamber.height += cycles_to_go * height_added_per_cycle
                chamber.rocks = {(x, chamber.height - 1) for x in range(chamber.width)}

                rock_num += cycles_to_go * rock_num_added_per_cycle
                move_num += cycles_to_go * move_num_added_per_cycle
            
    return chamber.height


if __name__ == '__main__':

    ### THE TESTS
    test_input = '''>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>'''
    max_height = simulation(test_input)
    assert max_height == 3068

    # TODO: Solution is not generalized... need to modify to handle arbitrary input
    # Probably remove the check for rock_type 1 in the logic above
    # max_height = simulation(test_input, 1_000_000_000_000)
    # assert max_height == 1514285714288

    ### THE REAL THING
    puzzle_input = helper.read_input()
    max_height = simulation(puzzle_input)
    print(f'Part 1: {max_height}')
    large_n = 1_000_000_000_000
    # 1595973 for 1_000_000 rocks
    # 159620 for 100000 rocks
    # Adding 2785 height per cycle
    # Adding 1745 rocks per cycle
    # Adding 10091 moves per cycle
    max_height = simulation(puzzle_input, large_n)
    print(f'Part 2: {max_height}')
