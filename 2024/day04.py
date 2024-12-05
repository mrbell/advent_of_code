from typing import List
import helper


directions = [
    (-1, 0),  # up
    (1, 0),   # down
    (0, -1),  # left
    (0, 1),   # right
    (1, 1),   # down-right
    (-1, -1), # up-left
    (1, -1),  # down-left
    (-1, 1)   # up-right
]

word_to_match = 'XMAS'


def count_xmas(grid: List[str]) -> int:
    count = 0
    for i, row in enumerate(grid):
        for j, c in enumerate(row):
            
            if c != word_to_match[0]:
                continue

            for d in directions:
                found = True
                for k in range(1, len(word_to_match)):
                    next_i = i + d[0] * k
                    next_j = j + d[1] * k
                    if next_i < 0 or next_i >= len(grid) or next_j < 0 or next_j >= len(grid[0]):
                        found = False
                        break
                    next_char = grid[i + d[0] * k][j + d[1] * k]
                    if next_char != word_to_match[k]:
                        found = False
                        break
                if found:
                    count += 1
                    
    return count


def count_x_mas(grid: List[str]) -> int:
    count = 0 

    for i, row in enumerate(grid[1:-1], 1):
        for j, c in enumerate(row[1:-1], 1):
            if c != 'A':
                continue
            if (
                (grid[i-1][j-1] == 'M' and grid[i+1][j+1] == 'S') or (grid[i-1][j-1] == 'S' and grid[i+1][j+1] == 'M')
            ) and (
                (grid[i-1][j+1] == 'M' and grid[i+1][j-1] == 'S') or (grid[i-1][j+1] == 'S' and grid[i+1][j-1] == 'M')
            ):
                count += 1
    
    return count
            

if __name__ == '__main__':
    ### THE TESTS
    test_input = '''MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX'''.split('\n')

    val = count_xmas(test_input)
    assert val == 18, f'Expected 18 but got {val}'
    val2 = count_x_mas(test_input)
    assert val2 == 9, f'Expected 9 but got {val2}'

    ### THE REAL THING
    puzzle_input = helper.read_input_lines()
    print(f'Part 1: {count_xmas(puzzle_input)}')
    print(f'Part 2: {count_x_mas(puzzle_input)}')


