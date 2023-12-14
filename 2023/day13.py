from typing import List, Tuple
import helper


flip_char = {'#': '.', '.': '#'}


def parse_patterns(puzzle_input: str) -> List[List[str]]:
    patterns = []
    for pattern in puzzle_input.split('\n\n'):
        patterns.append(pattern.splitlines())
    return patterns


def test_mirror(pattern: List[str], split: int) -> bool:
    if split < 0 or split >= len(pattern) - 1:
        return True
    if pattern[split] == pattern[split + 1]:
        return test_mirror(pattern[:split] + pattern[split + 2:], split - 1)
    else:
        return False


def transpose(pattern: List[str]) -> List[str]:
    return [''.join([line[i] for line in pattern]) for i in range(len(pattern[0]))]


def find_mirror_horizontal(pattern: List[str]) -> int:
    for i, line in enumerate(pattern[:-1]):
        if test_mirror(pattern, i):
            return i + 1
    return -1


def find_mirror(pattern: List[str]) -> Tuple[int, int]:
    split = find_mirror_horizontal(pattern)
    if split >= 0:
        return split, 0
    tpattern = transpose(pattern)
    split = find_mirror_horizontal(tpattern)
    if split >= 0:
        return split, 1
    return -1, -1


def part1(puzzle_input: str) -> int:
    patterns = parse_patterns(puzzle_input)
    total = 0
    for pattern in patterns:
        split, direction = find_mirror(pattern)
        total += split * (100 - direction * 99)  # direction = 0 if mirror is horizontal, 1 if vertical

    return total


def find_other_mirror(pattern: List[str]) -> int:

    original_split, original_direction = find_mirror(pattern)
    for i, line in enumerate(pattern):
        for j, char in enumerate(line):
            new_char = flip_char[char]
            pattern_copy = pattern.copy()
            pattern_copy[i] = pattern_copy[i][:j] + new_char + pattern_copy[i][j+1:]
            split, direction = find_mirror(pattern_copy)
            if split > 0 and (split != original_split or direction != original_direction):
                if (direction == 0 and split == len(pattern)) or (direction == 1 and split == len(pattern[0])):
                    raise IndexError('Unexpected split')
                return split, direction
    
    print('\n'.join(pattern))
    print(f'Split: {original_split}, Direction: {original_direction}')
    raise ValueError('No other mirror found')
    # return -1, -1


def part2(puzzle_input: str) -> int:
    patterns = parse_patterns(puzzle_input)
    total = 0
    missing_count = 0
    for pattern in patterns:
        try:
            split, direction = find_other_mirror(pattern)
        except ValueError:
            missing_count += 1
            continue
        total += split * (100 - direction * 99)
    print(f'Missing: {missing_count} / {len(patterns)}')
    return total 


if __name__ == '__main__':
    ### THE TESTS
    test_input = '''#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#'''

    assert part1(test_input) == 405
    assert part2(test_input) == 400


    test_pattern = '''.##......
###.####.
##.##...#
..###..##
...##..##
#..#.##.#
..#......
.##..##..
.##..##..'''.splitlines()
    assert find_mirror(test_pattern) == (8, 0)
    assert find_other_mirror(test_pattern) == (6, 1)

    ### THE REAL THING
    puzzle_input = helper.read_input()
    print(f'Part 1: {part1(puzzle_input)}')
    print(f'Part 2: {part2(puzzle_input)}')  # 23500 is too low
