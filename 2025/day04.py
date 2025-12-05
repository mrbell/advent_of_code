from typing import List, Tuple
import helper
from textwrap import dedent

ROLL = '@'
BLANK = '.'
type Coord = Tuple[int, int]

def is_roll_accessible(row: int, col: int, diagram: List[str]) -> bool:
    neighboring_rolls = 0
    for d_row in [-1, 0, 1]:
        neighboring_row = row + d_row
        if neighboring_row < 0 or neighboring_row >= len(diagram):
            continue
        for d_col in [-1, 0, 1]:
            neighboring_col = col + d_col
            if (
                (d_row == 0 and d_col == 0) or 
                (neighboring_col < 0 or neighboring_col >= len(diagram[0]))
            ):
                continue
            elif diagram[neighboring_row][neighboring_col] == ROLL:
                neighboring_rolls += 1
    return neighboring_rolls < 4


def find_accessible_rolls(diagram: List[str]) -> List[Coord]:
    accessible_rolls = []
    for row_num, row in enumerate(diagram):
        for col_num, col in enumerate(row):
            if col == ROLL and is_roll_accessible(row_num, col_num, diagram):
                accessible_rolls.append(
                    (row_num, col_num)
                )
    return accessible_rolls


def remove_rolls(diagram: List[str], accessible_rolls: List[Coord]) -> List[str]:
    new_diagram = []
    for row in diagram:
        new_row = []
        for col in row:
            new_row.append(col)
        new_diagram.append(new_row)

    for accessible_roll in accessible_rolls:
        new_diagram[accessible_roll[0]][accessible_roll[1]] = BLANK
    return [''.join(row) for row in new_diagram]


def part1(puzzle_input: List[str]) -> int:
    accessible_rolls = find_accessible_rolls(puzzle_input)
    return len(accessible_rolls)


def part2(puzzle_input: List[str]) -> int:
    removed_rolls = 0
    diagram = [row for row in puzzle_input]
    while True:
        accessible_rolls = find_accessible_rolls(diagram)
        if len(accessible_rolls) == 0:
            break
        removed_rolls += len(accessible_rolls)
        diagram = remove_rolls(diagram, accessible_rolls)

    return removed_rolls


if __name__ == '__main__':
    ### THE TESTS
    test_input = dedent('''
        ..@@.@@@@.
        @@@.@.@.@@
        @@@@@.@.@@
        @.@@@@..@.
        @@.@@@@.@@
        .@@@@@@@.@
        .@.@.@.@@@
        @.@@@.@@@@
        .@@@@@@@@.
        @.@.@@@.@.
    ''').strip().split('\n')

    assert part1(test_input) == 13
    assert part2(test_input) == 43

    ### THE REAL THING
    puzzle_input = helper.read_input_lines()
    print(f'Part 1: {part1(puzzle_input)}')
    print(f'Part 2: {part2(puzzle_input)}')
