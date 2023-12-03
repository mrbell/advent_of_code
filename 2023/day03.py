from typing import List, Tuple
import helper


def is_symbol(schematic: List[str], row: int, col: int) -> bool:
    try:
        if not schematic[row][col].isdigit() and schematic[row][col] != '.':
            return True
    except IndexError:
        pass
    return False


def check_if_part_no(schematic: List[str], row: int, col: int) -> bool:
    if (
        is_symbol(schematic, row, col+1) or is_symbol(schematic, row, col-1) or
        is_symbol(schematic, row+1, col) or is_symbol(schematic, row-1, col) or 
        is_symbol(schematic, row+1, col+1) or is_symbol(schematic, row-1, col-1) or
        is_symbol(schematic, row+1, col-1) or is_symbol(schematic, row-1, col+1)
    ):
        return True
    return False


def read_schematic(schematic: List[str]) -> List[int]:
    part_nos = []

    for row, line in enumerate(schematic):
        part_no = ''
        is_part_no = False
        for col, char in enumerate(line):
            if char.isdigit():
                part_no += char
                is_part_no = is_part_no or check_if_part_no(schematic, row, col)
            elif len(part_no) > 0:
                if is_part_no:
                    part_nos.append(int(part_no))
                part_no = ''
                is_part_no = False

        if len(part_no) > 0 and is_part_no:
            # Handle a number at the very end of the line
            part_nos.append(int(part_no))
    return part_nos


def find_adjacent_part_nos(schematic: List[str], row: int, col: int) -> List[int]:
    adjacent_part_nos = []
    for r in range(row-1, row+2):
        c = col - 1
        while c < (col + 2):
            if r != row or c != col:
                 
                try:
                    if schematic[r][c].isdigit():
                        c_start = c
                        while c_start > 0 and schematic[r][c_start - 1].isdigit():
                            c_start -= 1
                        c_end = c
                        while c_end < len(schematic[r]) and schematic[r][c_end + 1].isdigit():
                            c_end += 1
                        c_end += 1
                        part_no = int(schematic[r][c_start:c_end])
                        adjacent_part_nos.append(part_no)
                        c = c_end
                        continue
                except IndexError:
                    pass
                
            c += 1
    return adjacent_part_nos


def find_gears(schematic: List[str]) -> List[int]:
    gear_ratios = []
    for row, line in enumerate(schematic):
        for col, char in enumerate(line):
            if char == '*':
                adjacent_part_nos = find_adjacent_part_nos(schematic, row, col)
                if len(adjacent_part_nos) == 2:
                    gear_ratios.append(adjacent_part_nos[0] * adjacent_part_nos[1])

    return gear_ratios


def part1(puzzle_input: List[str]) -> int:
    part_nos = read_schematic(puzzle_input)
    return sum(part_nos)


def part2(puzzle_input: List[str]) -> int:
    gear_ratios = find_gears(puzzle_input)
    return sum(gear_ratios)


if __name__ == '__main__':
    ### THE TESTS
    test_input = '''467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..'''.split('\n')

    assert part1(test_input) == 4361
    assert part2(test_input) == 467835

    ### THE REAL THING
    puzzle_input = helper.read_input_lines()
    print(f'Part 1: {part1(puzzle_input)}')
    print(f'Part 2: {part2(puzzle_input)}')

# 92594595 too low
