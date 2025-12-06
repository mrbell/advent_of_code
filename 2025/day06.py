from typing import List, Tuple, Any, Callable
import helper
from textwrap import dedent


def prod(values: List[int]) -> int:
    product = 1
    for val in values:
        product *= val
    return product


def transpose(grid: List[List[Any]]) -> List[List[Any]]:
    tgrid = []
    for col_num in range(len(grid[0])):
        col = []
        for row_num in range(len(grid)):
            col.append(grid[row_num][col_num])
        tgrid.append(col)
    return tgrid


def count_max_spaces(line: str) -> int:
    max_spaces = -1
    in_spaces = False
    current_space_count = 0
    
    for val in line:
        if not in_spaces and val != ' ':
            # In a number
            continue
        elif not in_spaces and val == ' ':
            # Transition from number to space
            in_spaces = True
            current_space_count = 1
        elif in_spaces and val == ' ':
            # In spaces
            current_space_count += 1
        else:
            # Transition from spaces to number
            if current_space_count > max_spaces:
                max_spaces = current_space_count
            in_spaces = False
            current_space_count = 0
    
    return max_spaces 


def reduce_spaces(line: str) -> str:
    max_spaces = count_max_spaces(line)
    for n_spaces in range(max_spaces, 1, -1):
        line = line.replace(' ' * n_spaces, ' ')
    return line


class Problem:
    def __init__(self, values: List[int], operation: str):
        self.values = [int(v) for v in values]
        self.operation = sum if operation == '+' else prod
    
    def result(self) -> int:
        return self.operation(self.values)


def parse_problems(worksheet: List[str]) -> List[Problem]:
    grid = []
    for raw_line in worksheet:
        line = raw_line.strip()
        line = reduce_spaces(line)
        grid.append(line.split(' '))
    
    grid = transpose(grid)

    problems = []
    for prob_def in grid:
        values = prob_def[:-1]
        op = prob_def[-1]
        problems.append(Problem(values, op))
    
    return problems


def parse_problem_values(worksheet: List[str], start_col: int, end_col: int) -> List[int]:
    values = []
    for col in range(end_col - 1, start_col - 1, -1):
        digits = []
        for line in worksheet:
            if line[col] == ' ':
                continue
            else:
                digits.append(line[col])
        digits = int(''.join(digits))
        values.append(digits)
    return values


def parse_problems_correctly(worksheet: List[str]) -> List[Problem]:
    problems = []
    start_col = 0
    current_col = start_col + 1
    in_problem = True
    n_cols = len(worksheet[0])

    while current_col <= n_cols:
        if current_col == n_cols: 
            this_col = [' ' for line in worksheet]
        else:
            this_col = [line[current_col] if current_col < len(line) else ' ' for line in worksheet]

        if not in_problem and all(v == ' ' for v in this_col):
            # In spaces between problems
            current_col += 1
            continue
        elif not in_problem:
            # Transition from spaces to problem
            in_problem = True 
            start_col = current_col
            current_col += 1
            continue
        elif in_problem and not all(v == ' ' for v in this_col):
            # Within problem
            current_col += 1
            continue
        else:
            # Found the end of the problem
            end_col = current_col
            op = worksheet[-1][start_col:end_col].strip()
            values = parse_problem_values(worksheet[:-1], start_col, end_col)
            problems.append(Problem(values, op))
            
            in_problem = False
            current_col += 1
            continue
    
    return problems


def solve_problems(worksheet: List[str], parser: Callable) -> int:
    problems = parser(worksheet)
    return sum(p.result() for p in problems)


def part1(puzzle_input: List[str]) -> int:
    return solve_problems(puzzle_input, parse_problems)


def part2(puzzle_input: str) -> int:
    return solve_problems(puzzle_input, parse_problems_correctly)


if __name__ == '__main__':
    ### THE TESTS
    test_input = dedent("""
        123 328  51 64 
         45 64  387 23 
          6 98  215 314
        *   +   *   +
    """).strip().split('\n')

    assert part1(test_input) == 4277556
    assert part2(test_input) == 3263827

    ### THE REAL THING
    puzzle_input = helper.read_input_lines()
    print(f'Part 1: {part1(puzzle_input)}')
    print(f'Part 2: {part2(puzzle_input)}')
