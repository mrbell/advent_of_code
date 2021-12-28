from __future__ import annotations
from time import time
from dataclasses import dataclass, field
from typing import List, Tuple, Dict
import helper


costs = {
    'A': 1,
    'B': 10,
    'C': 100,
    'D': 1000
}

hall_positions = {
    'A': 2,
    'B': 4,
    'C': 6,
    'D': 8
}


@dataclass
class Map: 
    a_room: List[str]
    b_room: List[str]
    c_room: List[str]
    d_room: List[str]
    hall: List[str] = field(default_factory=lambda: ['.'] * 11)

    def from_diagram(diagram: str, unfold: bool=False) -> Map:
        diagram_rows = diagram.strip().split('\n')
        folded_a = ['D', 'D'] if unfold else []
        folded_b = ['B', 'C'] if unfold else []
        folded_c = ['A', 'B'] if unfold else []
        folded_d = ['C', 'A'] if unfold else []

        a_room = [diagram_rows[3][3]] + folded_a + [diagram_rows[2][3]]
        b_room = [diagram_rows[3][5]] + folded_b + [diagram_rows[2][5]]
        c_room = [diagram_rows[3][7]] + folded_c + [diagram_rows[2][7]]
        d_room = [diagram_rows[3][9]] + folded_d + [diagram_rows[2][9]]

        return Map(a_room, b_room, c_room, d_room)

    def __hash__(self):
        return hash(str(self))

    def __str__(self) -> str:
        unfolded = len(self.a_room) > 2
        unfolded_lines = [
            f'###{self.a_room[2]}#{self.b_room[2]}#{self.c_room[2]}#{self.d_room[2]}###',
            f'###{self.a_room[1]}#{self.b_room[1]}#{self.c_room[1]}#{self.d_room[1]}###'
        ] if unfolded else []
        lines = [
            '#' * 13,
            '#' + ''.join(self.hall) + '#',
            f'###{self.a_room[-1]}#{self.b_room[-1]}#{self.c_room[-1]}#{self.d_room[-1]}###'
        ] + unfolded_lines + [
            f'  #{self.a_room[0]}#{self.b_room[0]}#{self.c_room[0]}#{self.d_room[0]}#  ',
            '  #########  ',
            ' ' * 13 
        ]
        return '\n'.join(lines)

    def copy(self) -> Map:
        return Map(
            self.a_room.copy(),
            self.b_room.copy(),
            self.c_room.copy(),
            self.d_room.copy(),
            self.hall.copy()
        )

    def move(self, starting_point: Tuple[str, int], ending_point: Tuple[str, int]) -> Map:
        '''
        Returns a new Map that has been updated with the given move. The move is assumed
        to be legal.
        '''
        thing_to_move = getattr(self, starting_point[0])[starting_point[1]]
        new_map = self.copy()
        getattr(new_map, starting_point[0])[starting_point[1]] = '.'
        getattr(new_map, ending_point[0])[ending_point[1]] = thing_to_move 
        return new_map

    def move_score(self, starting_point: Tuple[str, int], ending_point: Tuple[str, int]) -> int:
        '''
        Given a starting and ending point, how much does the move cost. The move is assumed
        to be legal (i.e. this function does not check whether the move is possible and 
        may not work for impossible moves e.g. from hall to hall).
        '''
        steps = 0
        whos_moving = getattr(self, starting_point[0])[starting_point[1]]
        cost_per_step = costs[whos_moving]
        room_size = len(self.a_room)
        if 'room' in starting_point[0] and 'room' in ending_point[0]:
            steps += (room_size - starting_point[1])
            which_room = starting_point[0][0].upper()
            to_which_room = ending_point[0][0].upper()
            steps += abs(hall_positions[which_room] - hall_positions[to_which_room])
            steps += (room_size - ending_point[1])
        elif 'room' in starting_point[0]:
            steps += (room_size - starting_point[1])
            which_room = starting_point[0][0].upper()
            steps += abs(hall_positions[which_room] - ending_point[1])
        else:
            steps += abs(starting_point[1] - hall_positions[whos_moving])
            steps += (room_size - ending_point[1])
        return steps * cost_per_step

    def eligible_to_move(self) -> Tuple[str, int]:
        elig_to_move = []

        for room_id in 'abdc':
            room_name = f'{room_id}_room'
            room = getattr(self, room_name)

            try:
                for i in range(len(room) - 1, -1, -1):
                    if room[i].isalpha():
                        if room[i] != room_id.upper():
                            elig_to_move.append((room_name, i))
                            raise StopIteration
                        else:
                            for j in range(i):
                                if room[j] != room_id.upper():
                                    elig_to_move.append((room_name, i))
                                    raise StopIteration
            except StopIteration:
                continue
          
        for hall_id, amph in enumerate(self.hall):
            if amph.isalpha():
                elig_to_move.append(('hall', hall_id))
        
        return elig_to_move
    
    def legal_moves(self, starting_point: Tuple[str, int]) -> List[Tuple[str, int]]:
        legal_moves = []
        whos_moving = getattr(self, starting_point[0])[starting_point[1]]
        if 'room' in starting_point[0]:
            # All valid moves would be to a hall position or to the proper room
            starting_room_position = hall_positions[starting_point[0][0].upper()]
            for hall_pos in range(starting_room_position + 1, 11):
                if self.hall[hall_pos] == '.' and hall_pos not in hall_positions.values():
                    legal_moves.append(('hall', hall_pos))
                elif self.hall[hall_pos].isalpha():
                    break
            for hall_pos in range(starting_room_position - 1, -1, -1):
                if self.hall[hall_pos] == '.' and hall_pos not in hall_positions.values():
                    legal_moves.append(('hall', hall_pos))
                elif self.hall[hall_pos].isalpha():
                    break
            # Now pretend that we're just outside of the starting room in the hall and 
            # check if we can move into the proper room directly
            starting_point = ('hall', starting_room_position)
        
        # Starting in the hall, we have to move to the proper destination room if 
        # we can move at all
        destination_room_position = hall_positions[whos_moving]
        destination_room_name = f'{whos_moving.lower()}_room'
        destination_room = getattr(self, destination_room_name)
        step = 1 if starting_point[1] > destination_room_position else -1
        found_cheapest_move = False
        if all(
            p == '.' for p in self.hall[
                destination_room_position:starting_point[1]:step
            ]
        ):
            try:
                # Returns the index of the first open space in the room
                destination_room_position = destination_room.index('.')
                for i in range(0, destination_room_position):
                    if destination_room[i] != whos_moving: 
                        raise ValueError
                legal_moves = [(destination_room_name, destination_room_position)]
                found_cheapest_move = True
            except ValueError:
                # There are no empty spaces in the room
                pass

        return legal_moves, found_cheapest_move

    def solved(self) -> bool:
        for room_id in 'abcd':
            if not all(o == room_id.upper() for o in getattr(self, f'{room_id}_room')):
                return False
        return True


class Solver():

    def __init__(self):
        self.map_state_solution_costs: Dict[Map, int] = {}

    def find_cheapest_solution(
        self, the_map: Map, 
        cost_so_far: int=0, path_so_far: List[Map]=None, 
        verbose=False
    ) -> Tuple(int, List[Map]):

        if the_map in self.map_state_solution_costs:
            # We've seen this map state before and have stored the solution
            # relative to this state.
            if self.map_state_solution_costs[the_map][0] < 0:
                return (-1, [])
            else:
                return (
                    cost_so_far + self.map_state_solution_costs[the_map][0], 
                    path_so_far + self.map_state_solution_costs[the_map][1]
                ) 

        if path_so_far is None:
            path_so_far = []
            if verbose:
                print(the_map)
        solutions = []

        elig_to_move = the_map.eligible_to_move()
        legal_move_map = {}

        found_cheapest_move = False
        # If a amphipod is able to move to its room, that will always
        # be the cheapest next move... we don't have to search through other 
        # moves. So we'll loop over all amphipods that are eligible to move
        # and see if any can move to their correct room. If so, we take that
        # move as cheapest. If not, we'll loop over all amphipods that can 
        # move again and find which one leads to the cheapest solution.
        for i, mover in enumerate(elig_to_move):
            legal_moves, direct_to_goal = the_map.legal_moves(mover)
            # Store these so we don't have to compute again in the next loop 
            legal_move_map[mover] = legal_moves  
            if direct_to_goal:
                starting_point = mover
                ending_point = legal_moves[0]
                incremental_cost = the_map.move_score(starting_point, ending_point)
                updated_map = the_map.move(starting_point, ending_point)
                if updated_map.solved():
                    solutions.append((
                        cost_so_far + incremental_cost,
                        path_so_far + [updated_map]
                    ))
                else:
                    cheapest_solution = self.find_cheapest_solution(
                        updated_map,
                        cost_so_far + incremental_cost,
                        path_so_far + [updated_map]
                    )
                    if cheapest_solution[0] > 0:
                        solutions.append(cheapest_solution)
                found_cheapest_move = True
                break

        if not found_cheapest_move:
            for i, mover in enumerate(elig_to_move):
                
                legal_moves = legal_move_map[mover]
                for j, legal_move in enumerate(legal_moves):
                    incremental_cost = the_map.move_score(mover, legal_move)
                    updated_map = the_map.move(mover, legal_move)
                    if updated_map.solved():
                        solutions.append((
                            cost_so_far + incremental_cost,
                            path_so_far + [updated_map]
                        ))
                    else:
                        cheapest_solution = self.find_cheapest_solution(
                            updated_map, 
                            cost_so_far + incremental_cost,
                            path_so_far + [updated_map]
                        )
                        if cheapest_solution[0] > 0:
                            solutions.append(cheapest_solution)
                    if len(path_so_far) < 2 and verbose:
                        print(
                            '.' * len(path_so_far) + 
                            f'mover {i+1}/{len(elig_to_move)}, move {j}/{len(legal_moves)}'
                        )

        lowest_cost, lowest_cost_path = min(solutions, key=lambda x: x[0]) if len(solutions) > 0 else (-1, [])

        # Store the lowest incremental cost and associated path required to find the solution from the current state
        self.map_state_solution_costs[the_map] = (
            lowest_cost - cost_so_far if lowest_cost > 0 else -1,
            lowest_cost_path[len(path_so_far):] if lowest_cost > 0 else []
        )

        return lowest_cost, lowest_cost_path 


if __name__ == '__main__':
    ### THE TESTS
    test_starting_map = '''#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########'''

    test_solved_map = '''#############
#...........#
###A#B#C#D###
  #A#B#C#D#
  #########'''


    test_starting_map2 = '''#############
#...B.....BA#
###.#.#C#.###
  #A#D#C#D#  
  #########'''
    test_map = Map.from_diagram(test_starting_map2)
    assert test_map.move_score(('b_room', 0), ('d_room', 1)) == 7000

    test_map_unfolded = Map.from_diagram(test_starting_map, unfold=True)
    print(test_map_unfolded)

    test_map = Map.from_diagram(test_starting_map)
    print(test_map)
    updated_test_map = test_map.move(('a_room', 1), ('hall', 0))

    elig_to_move = test_map.eligible_to_move()
    dests = test_map.legal_moves(elig_to_move[0])
    elig_to_move = updated_test_map.eligible_to_move()
    dests = updated_test_map.legal_moves(elig_to_move[0])
    dests = updated_test_map.legal_moves(elig_to_move[-1])

    t0 = time()
    solver = Solver()
    test_solutions = solver.find_cheapest_solution(test_map)
    print(f'Time to solve: {time() - t0:.2f} s')  # Benchmark time: 3.4 s 
    assert test_solutions[0] == 12521

    t0 = time()
    solver = Solver()
    test_solutions_unfolded = solver.find_cheapest_solution(test_map_unfolded)
    print(f'Time to solve: {time() - t0:.2f} s')  # Benchmark time: 
    assert test_solutions_unfolded[0] == 44169

    test_map = Map.from_diagram(test_solved_map)
    assert test_map.solved()

    ### THE REAL THING
    puzzle_input = helper.read_input()
    the_map = Map.from_diagram(puzzle_input)
    t0 = time()
    solver = Solver()
    the_solution = solver.find_cheapest_solution(the_map)
    print(f'Time to solve: {time() - t0:.2f} s')  # Benchmark time: 1.0 s
    print(f'Part 1: {the_solution[0]}')


    the_unfolded_map = Map.from_diagram(puzzle_input, unfold=True)
    t0 = time()
    solver = Solver()
    the_unfolded_solution = solver.find_cheapest_solution(the_unfolded_map)
    print(f'Time to solve: {time() - t0:.2f} s')  # Benchmark time: 1.0 s
    print(f'Part 2: {the_unfolded_solution[0]}')
