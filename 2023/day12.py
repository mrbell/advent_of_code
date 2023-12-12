from typing import List, Tuple
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
    broken_spring_pattern = [int(x) for x in broken_spring_pattern.split(',')]

    possibilities = fill_broken(spring_map)
    possibilities = [x for x in possibilities if matches_pattern(x, broken_spring_pattern)]    

    return possibilities


def part1(input: List[str]) -> int:
    arrangements = []
    for i, record in enumerate(input):
        if (i+1) % 100 == 0:
            print(f'{i+1}/{len(input)}')
        arrangements.extend(possible_arrangements(record))

    return len(arrangements)


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
    assert len(possible_arrangements(test_input[-1])) == 10
    assert part1(test_input) == 21


    ### THE REAL THING
    puzzle_input = helper.read_input_lines()
    print(f'Part 1: {part1(puzzle_input)}')
    print(f'Part 2: {""}')
