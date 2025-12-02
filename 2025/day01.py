from typing import List, Tuple
import helper

positions_on_dial = 100
initial_position = 50


def rotate_dial(current_position: int, command: str) -> Tuple[int, int]:
    sign = -1 if command[0] == 'L' else 1
    raw_number_of_clicks = int(command[1:])
    number_of_clicks = raw_number_of_clicks % positions_on_dial

    n_zero_crossings = raw_number_of_clicks // positions_on_dial

    if number_of_clicks == 0:
        return current_position, n_zero_crossings

    new_position = (current_position + number_of_clicks * sign)
    unwrapped_new_position = new_position % positions_on_dial

    crossed_zero = (unwrapped_new_position == 0) or (
        (current_position != 0) and (new_position != unwrapped_new_position)
    )

    if crossed_zero:
        n_zero_crossings += 1

    return unwrapped_new_position, n_zero_crossings


def rotate_dial_simplistic(current_position: int, command: str) -> Tuple[int, int]:
    sign = -1 if command[0] == 'L' else 1
    number_of_clicks = int(command[1:])

    n_zero_crossings = 0
    for _ in range(number_of_clicks):
        current_position += sign
        if current_position % positions_on_dial == 0:
            n_zero_crossings += 1
    
    return current_position % positions_on_dial, n_zero_crossings


def count_visits_to_zero(instructions: List[str], must_end_on: bool = True) -> int:
    
    current_position = initial_position
    zero_counter = 0
    for instruction in instructions:
        new_position, crossed_zero = rotate_dial(current_position, instruction)
        if must_end_on and (new_position == 0):
            zero_counter += 1
        elif (not must_end_on and crossed_zero > 0):
            zero_counter += crossed_zero
        
        current_position = new_position
    
    return zero_counter


def part1(puzzle_input: List[str]) -> int:
    return count_visits_to_zero(puzzle_input)


def part2(puzzle_input: List[str]) -> int:
    return count_visits_to_zero(puzzle_input, must_end_on=False)


if __name__ == '__main__':
    ### THE TESTS
    test_input = '''L68
L30
R48
L5
R60
L55
L1
L99
R14
L82'''.split('\n')

    p, n = rotate_dial(98, 'L96')
    assert p == 2 and n == 0
    p, n = rotate_dial(98, 'R4')
    assert p == 2 and n == 1
    p, n = rotate_dial(98, 'R104')
    assert p == 2 and n == 2
    p, n = rotate_dial(98, 'R2')
    assert p == 0 and n == 1
    p, n = rotate_dial(98, 'R102')
    assert p == 0 and n == 2

    p, n = rotate_dial(16, "R206")
    assert p == 22 and n == 2

    p, n = rotate_dial_simplistic(16, "R206")
    assert p == 22 and n == 2

    p, n = rotate_dial(0, 'R100')
    assert p == 0 and n == 1
    p, n = rotate_dial(0, 'L100')
    assert p == 0 and n == 1
    p, n = rotate_dial(0, 'R200')
    assert p == 0 and n == 2
    p, n = rotate_dial(0, 'L200')
    assert p == 0 and n == 2

    assert part1(test_input) == 3
    assert part2(test_input) == 6

    ### THE REAL THING
    puzzle_input = helper.read_input_lines()
    print(f'Part 1: {part1(puzzle_input)}')
    print(f'Part 2: {part2(puzzle_input)}')
