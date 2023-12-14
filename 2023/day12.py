from typing import List, Tuple
import functools
import helper


def fill_broken(spring_map: str) -> List[str]:
    if '?' not in spring_map:
        return [spring_map]
    
    possibilities = []
    for i, char in enumerate(spring_map):
        if char == '?':
            for c in '#.':
                new_possibilities = fill_broken(spring_map[:i] + c + spring_map[i+1:])
                possibilities.extend(new_possibilities)
            break
    return possibilities

# @functools.cache
def fill_broken_faster(spring_map: str, broken_spring_pattern: Tuple[int]) -> List[str]:
    if '?' not in spring_map:
        if matches_pattern(spring_map, broken_spring_pattern):
            return [spring_map]
        else:
            return []
    
    possibilities = []
    pattern_number = 0
    found_group = False
    group_count = 0

    for i, char in enumerate(spring_map):
        if char == '#':
            found_group = True
            group_count += 1
        elif char == '.' and found_group:
            if pattern_number >= len(broken_spring_pattern) or group_count != broken_spring_pattern[pattern_number]:
                break
            pattern_number += 1
            found_group = False
            group_count = 0
        elif char == '?':
            for c in '#.':
                new_possibilities = fill_broken_faster(spring_map[:i] + c + spring_map[i+1:], broken_spring_pattern)
                possibilities.extend(new_possibilities)
            break
    return possibilities


def parse_line(line: str) -> Tuple[str, Tuple[int]]:
    spring_map, broken_spring_pattern = line.split()
    broken_spring_pattern = [int(x) for x in broken_spring_pattern.split(',')]
    return spring_map, tuple(broken_spring_pattern)


def possible_arrangements_faster(spring_map: str, broken_spring_pattern: Tuple[int]) -> List[str]:
    possibilities = fill_broken_faster(spring_map, broken_spring_pattern)
    return possibilities


def matches_pattern(spring_map: str, broken_spring_pattern: List[int]) -> bool:
    map_pattern = []
    group_found = False
    group_count = 0
    for i, char in enumerate(spring_map):
        if char == '#':
            group_found = True
            group_count += 1
        elif char == '.' and group_found:
            map_pattern.append(group_count)
            group_found = False
            group_count = 0
    if group_found:
        map_pattern.append(group_count)
    return len(map_pattern) == len(broken_spring_pattern) and all([x == y for x, y in zip(map_pattern, broken_spring_pattern)])


def possible_arrangements(damaged_record: str) -> List[str]:
    spring_map, broken_spring_pattern = damaged_record.split()
    broken_spring_pattern = tuple(int(x) for x in broken_spring_pattern.split(','))

    possibilities = fill_broken(spring_map)
    possibilities = [x for x in possibilities if matches_pattern(x, broken_spring_pattern)]    

    return possibilities


def part1(input: List[str]) -> int:
    arrangements = []
    for i, record in enumerate(input):
        if (i+1) % 100 == 0:
            print(f'{i+1}/{len(input)}')
        spring_map, broken_spring_pattern = parse_line(record)
        arrangements.extend(possible_arrangements_faster(spring_map, broken_spring_pattern))

    return len(arrangements)


def unfold(spring_map: str) -> str:
    return '?'.join([spring_map] * 5)


def part2(input: List[str]) -> int:
    total_arrangements = 0
    for i, record in enumerate(input):
        if (i+1) % 10 == 0:
            print(f'{i+1}/{len(input)}')
        spring_map, broken_spring_pattern = parse_line(record)
        orig_arrangements = possible_arrangements_faster(spring_map, tuple(broken_spring_pattern))
        if all(arr[-1] == '#' for arr in orig_arrangements) and all(arr[0] == '#' for arr in orig_arrangements):
            post_arrangements = orig_arrangements
            pre_arrangements = orig_arrangements
        else:
            post_arrangements = possible_arrangements_faster(spring_map + '?', broken_spring_pattern)
            pre_arrangements = possible_arrangements_faster('?' + spring_map, broken_spring_pattern)
        
        if len(pre_arrangements) == len(orig_arrangements) == len(post_arrangements):
            to_add = len(pre_arrangements) ** 5
        elif len(pre_arrangements) == len(orig_arrangements):
            to_add = len(post_arrangements) ** 4 * len(orig_arrangements)
        elif len(post_arrangements) == len(orig_arrangements):
            to_add = len(pre_arrangements) ** 4 * len(orig_arrangements)
        else:
            spring_map = unfold(spring_map)
            broken_spring_pattern = broken_spring_pattern * 5
            to_add = len(possible_arrangements_faster(spring_map, broken_spring_pattern))

        total_arrangements += to_add

    return total_arrangements


import multiprocessing

def inner_part(record): 

    spring_map, broken_spring_pattern = parse_line(record)
    orig_arrangements = possible_arrangements_faster(spring_map, tuple(broken_spring_pattern))
    if all(arr[-1] == '#' for arr in orig_arrangements) and all(arr[0] == '#' for arr in orig_arrangements):
        post_arrangements = orig_arrangements
        pre_arrangements = orig_arrangements
    else:
        post_arrangements = possible_arrangements_faster(spring_map + '?', broken_spring_pattern)
        pre_arrangements = possible_arrangements_faster('?' + spring_map, broken_spring_pattern)
    
    if len(pre_arrangements) == len(orig_arrangements) == len(post_arrangements):
        to_add = len(pre_arrangements) ** 5
    elif len(pre_arrangements) == len(orig_arrangements):
        to_add = len(post_arrangements) ** 4 * len(orig_arrangements)
    elif len(post_arrangements) == len(orig_arrangements):
        to_add = len(pre_arrangements) ** 4 * len(orig_arrangements)
    else:
        spring_map = unfold(spring_map)
        broken_spring_pattern = broken_spring_pattern * 5
        to_add = len(possible_arrangements_faster(spring_map, broken_spring_pattern))

    return to_add


def part2_parallel(input: List[str]) -> int:
    total_arrangements = 0
    with multiprocessing.Pool() as pool:
        total_arrangements = sum(pool.map(inner_part, input))
    return total_arrangements

# ?#?#?#????????.  8,1

# 20583051291590026 is too high
# 767250159265 is too low



if __name__ == '__main__':
    ### THE TESTS
    test_input = '''???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1'''.splitlines()
    assert len(possible_arrangements(test_input[0])) == 1
    assert len(possible_arrangements(test_input[1])) == 4
    assert len(possible_arrangements_faster(*parse_line(test_input[1]))) == 4
    assert len(possible_arrangements_faster('?.??..??...?##.', (1,1,3))) == 8
    assert len(possible_arrangements(test_input[-1])) == 10
    assert part1(test_input) == 21
    assert part2(test_input) == 525152
    assert part2_parallel(test_input) == 525152

    ### THE REAL THING
    puzzle_input = helper.read_input_lines()
    print(f'Part 1: {part1(puzzle_input)}')
    print(f'Part 2: {part2_parallel(puzzle_input)}')
