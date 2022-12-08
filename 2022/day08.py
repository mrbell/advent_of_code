from typing import List
import helper


def parse_tree_grid(grid: List[str]) -> List[List[int]]:
    return [[int(height) for height in line] for line in grid]


def count_visible_trees(tree_grid: List[List[int]]) -> int:

    visible_trees = []
    # Add the outside trees
    visible_trees.extend(
        [(0, col) for col in range(len(tree_grid[0]))] 
    )
    visible_trees.extend(
        [(len(tree_grid) - 1, col) for col in range(len(tree_grid[-1]))]
    )
    visible_trees.extend(
        [(row, 0) for row in range(1, len(tree_grid) - 1)]
    )
    visible_trees.extend(
        [(row, len(tree_grid[-1]) - 1) for row in range(1, len(tree_grid) - 1)]
    )

    for i in range(1, len(tree_grid) - 1):
        # Add interior trees visibile from the left 
        if tree_grid[i][0] < 9:
            for j in range(1, len(tree_grid[i]) - 1):
                if tree_grid[i][j] > max(tree_grid[i][:j]):
                    visible_trees.append((i, j))
                if tree_grid[i][j] == 9:
                    break
        
        # Add interior trees visibile from the right 
        if tree_grid[i][-1] < 9:    
            for j in range(len(tree_grid[i]) - 2, 0, -1):
                if tree_grid[i][j] > max(tree_grid[i][(j + 1):]):
                    visible_trees.append((i, j))
                if tree_grid[i][j] == 9:
                    break

    for j in range(1, len(tree_grid[0]) - 1):
        # Add interior trees visibile from the top 
        if tree_grid[0][j] < 9:
            for i in range(1, len(tree_grid) - 1):
                if tree_grid[i][j] > max([row[j] for row in tree_grid[:i]]):
                    visible_trees.append((i, j))
                if tree_grid[i][j] == 9:
                    break
        
        # Add interior trees visibile from the bottom 
        if tree_grid[-1][j] < 9:    
            for i in range(len(tree_grid) - 2, 0, -1):
                if tree_grid[i][j] > max([row[j] for row in tree_grid[(i + 1):]]):
                    visible_trees.append((i, j))
                if tree_grid[i][j] == 9:
                    break

    visible_trees = set(visible_trees)

    return len(visible_trees)


def scenic_score(row: int, col: int, tree_grid: List[List[int]]) -> int:
    
    if row == 0 or row == len(tree_grid) - 1 or col == 0 or col == len(tree_grid[0]) - 1:
        return 0

    score = 1

    # Check down
    this_score = 0 
    for i in range(row + 1, len(tree_grid)):
        this_score += 1
        if tree_grid[i][col] >= tree_grid[row][col]:
            break
    score *= this_score

    # Check up
    this_score = 0 
    for i in range(row - 1, -1, -1):
        this_score += 1
        if tree_grid[i][col] >= tree_grid[row][col]:
            break
    score *= this_score

    # Check right
    this_score = 0 
    for j in range(col + 1, len(tree_grid[0])):
        this_score += 1
        if tree_grid[row][j] >= tree_grid[row][col]:
            break
    score *= this_score

    # Check left
    this_score = 0 
    for j in range(col - 1, -1, -1):
        this_score += 1
        if tree_grid[row][j] >= tree_grid[row][col]:
            break
    score *= this_score

    return score


def max_scenic_score(tree_grid: List[List[int]]) -> int:
    max_score = 0
    for row in range(1, len(tree_grid) - 1):
        for col in range(1, len(tree_grid[0]) - 1):
            this_score = scenic_score(row, col, tree_grid)
            if this_score > max_score:
                max_score = this_score
    return max_score


if __name__ == '__main__':
    ### THE TESTS
    test_input = '''30373
25512
65332
33549
35390'''.split('\n')

    test_grid = parse_tree_grid(test_input)
    assert count_visible_trees(test_grid) == 21
    assert scenic_score(1, 2, test_grid) == 4
    assert scenic_score(3, 2, test_grid) == 8
    assert max_scenic_score(test_grid) == 8

    ### THE REAL THING
    puzzle_input = helper.read_input_lines()
    tree_grid = parse_tree_grid(puzzle_input)
    print(f'Part 1: {count_visible_trees(tree_grid)}')
    print(f'Part 2: {max_scenic_score(tree_grid)}')
