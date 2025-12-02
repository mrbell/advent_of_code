from typing import List, Tuple, Callable
import helper


type RangeSpec = Tuple[int, int]


def parse_range(r: str) -> RangeSpec:
    range_start, range_stop = r.split('-')
    return int(range_start), int(range_stop)


def parse_ranges(range_list: str) -> List[RangeSpec]:
    ranges = range_list.split(',')
    ranges = [parse_range(r) for r in ranges]
    return ranges


def invalid_id(id: int) -> bool:
    id_str = str(id)

    if len(id_str) % 2 == 1:
        return False
    else:
        if id_str[:len(id_str) // 2] == id_str[len(id_str) // 2:]:
            return True


def invalid_id_v2(id: int) -> bool:
    id_str = str(id)
    n_digits = len(id_str)

    for part_length in range(n_digits // 2, 0, -1):
        if n_digits % part_length != 0:
            continue

        parts = [id_str[n*part_length:(n+1)*part_length] for n in range(n_digits // part_length)]

        unique_parts = set(parts)

        if len(unique_parts) == 1:
            return True
    
    return False


def sum_invalid_ids_in_range(id_range: RangeSpec, validation_func: Callable = invalid_id) -> int:
    
    invalid_id_sum = 0

    for id in range(id_range[0], id_range[1] + 1):
        if validation_func(id):
            invalid_id_sum += id
    
    return invalid_id_sum


def sum_invalid_ids(id_ranges: List[RangeSpec], validation_func: Callable = invalid_id) -> int:

    invalid_id_sum = 0
    for id_range in id_ranges:
        invalid_id_sum += sum_invalid_ids_in_range(id_range, validation_func)
    
    return invalid_id_sum


def part1(puzzle_input: str) -> int:
    id_ranges = parse_ranges(puzzle_input)
    return sum_invalid_ids(id_ranges)


def part2(puzzle_input: str) -> int:
    id_ranges = parse_ranges(puzzle_input)
    return sum_invalid_ids(id_ranges, invalid_id_v2)


if __name__ == '__main__':
    ### THE TESTS
    test_input = '''11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124'''

    assert invalid_id(22)
    assert not invalid_id(23)
    assert invalid_id(543543)
    assert not invalid_id(110111)

    assert invalid_id_v2(22)
    assert invalid_id_v2(111)
    assert invalid_id_v2(543543)
    assert invalid_id_v2(123123123)
    assert invalid_id_v2(8989898989898989)
    assert not invalid_id_v2(23)
    assert not invalid_id_v2(1101111)

    ### THE REAL THING
    puzzle_input = helper.read_input()
    print(f'Part 1: {part1(puzzle_input)}')
    print(f'Part 2: {part2(puzzle_input)}')
