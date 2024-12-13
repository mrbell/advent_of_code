from typing import List, Tuple
import helper


def find_region(grid, row, col):
    val = grid[row][col]
    region = [(row, col)]
    visited = [(row, col)]
    while visited:
        r, c = visited.pop()
        for i, j in [(r+1, c), (r-1, c), (r, c+1), (r, c-1)]:
            if i < 0 or j < 0 or i >= len(grid) or j >= len(grid[0]):
                continue
            if (i, j) in region:
                continue
            if grid[i][j] != val:
                continue
            region.append((i, j))
            visited.append((i, j))
    return region


def find_regions(grid):

    visited = []
    regions = []

    for row, line in enumerate(grid):
        for col, cell in enumerate(line):
            if (row, col) in visited:
                continue
            region = find_region(grid, row, col)
            regions.append(region)
            visited += region
    
    return regions


def find_fence(region, row, col, direction):
    fence = []
    if direction == 'up':
        next_col = col
        while (row, next_col) in region and (row + 1, next_col) not in region:
            fence.append((row, next_col, 'up'))
            next_col += 1

        next_col = col - 1
        while (row, next_col) in region and (row + 1, next_col) not in region:
            fence.append((row, next_col, 'up'))
            next_col -= 1
    elif direction == 'down':
        next_col = col
        while (row, next_col) in region and (row - 1, next_col) not in region:
            fence.append((row, next_col, 'down'))
            next_col += 1

        next_col = col - 1
        while (row, next_col) in region and (row - 1, next_col) not in region:
            fence.append((row, next_col, 'down'))
            next_col -= 1
    elif direction == 'right':
        next_row = row
        while (next_row, col) in region and (next_row, col + 1) not in region:
            fence.append((next_row, col, 'right'))
            next_row += 1

        next_row = row - 1
        while (next_row, col) in region and (next_row, col + 1) not in region:
            fence.append((next_row, col, 'right'))
            next_row -= 1
    elif direction == 'left':
        next_row = row
        while (next_row, col) in region and (next_row, col - 1) not in region:
            fence.append((next_row, col, 'left'))
            next_row += 1

        next_row = row - 1
        while (next_row, col) in region and (next_row, col - 1) not in region:
            fence.append((next_row, col, 'left'))
            next_row -= 1
    return fence


def find_fences(region):
    fences = []
    visited = []

    for r, c in region:
        for i, j, d in [(r+1, c, 'up'), (r-1, c, 'down'), (r, c+1, 'right'), (r, c-1, 'left')]:
            if (r, c, d) in visited:
                # An edge, but already visited as a part of a known fence
                continue
            if (i, j) in region:
                # Not an edge
                continue
            # Find the rest of the fence from this edge
            fence = find_fence(region, r, c, d)
            fences.append(fence)
            visited += fence
    return fences


def region_fence_cost(region, discounted=False):
    area = len(region)
    if not discounted:
        perimeter = 0
        for r, c in region:
            for i, j in [(r+1, c), (r-1, c), (r, c+1), (r, c-1)]:
                if (i, j) not in region:
                    perimeter += 1
    else:
        fences = find_fences(region)
        perimeter = len(fences)
    return perimeter * area


def part1(grid):
    regions = find_regions(grid)
    return sum(region_fence_cost(region) for region in regions)


def part2(grid):
    regions = find_regions(grid)
    return sum(region_fence_cost(region, True) for region in regions)


if __name__ == '__main__':
    ### THE TESTS
    example_input = '''RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE'''.split('\n')

    result = part1(example_input)
    assert result == 1930, f'Expected 1930 but got {result}'
    result = part2(example_input)
    assert result == 1206, f'Expected 1206 but got {result}'

    ### THE REAL THING
    puzzle_input = helper.read_input_lines()
    print(f'Part 1: {part1(puzzle_input)}')
    print(f'Part 2: {part2(puzzle_input)}')
