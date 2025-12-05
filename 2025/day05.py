from typing import List, Tuple
import helper
from textwrap import dedent

type Range = Tuple[int, int]
type Ranges = List[Range]


def parse_range(the_range: str) -> Range:
    s, e = the_range.split('-')
    return int(s), int(e)


def parse_db(db: List[str]) -> Tuple[Ranges, List[int]]:
    fresh_ranges = []
    ids = []

    for line in db:
        if line == '':
            continue
        elif '-' in line:
            fresh_ranges.append(parse_range(line))
        else:
            ids.append(int(line))
    return fresh_ranges, ids


class IngredientDB:

    def __init__(self, db: List[str]):
        self.fresh_id_ranges, self.ids = parse_db(db)

    def is_id_fresh(self, id: int) -> bool:
        for range_start, range_end in self.fresh_id_ranges:
            if id >= range_start and id <= range_end:
                return True
        return False
    
    def get_fresh_ids(self) -> List[int]:
        fresh_ids = []
        for id in self.ids:
            if self.is_id_fresh(id):
                fresh_ids.append(id)
        return fresh_ids

    def count_all_fresh_ids(self) -> int:
        fresh_id_count = 0

        nonoverlapping_ranges = normalize_ranges(self.fresh_id_ranges)

        for nr in nonoverlapping_ranges:
            fresh_id_count += (nr[1] - nr[0] + 1)
        
        return fresh_id_count


def is_overlapping(range1: Range, range2: Range) -> bool:
    range1, range2 = sorted([range1, range2])
    
    if range2[0] > range1[1]:
        return False
    else:
        return True


def combine(range1: Range, range2: Range) -> Range:
    return min(range1[0], range2[0]), max(range1[1], range2[1])


def normalize_ranges(fresh_id_ranges: Ranges) -> Ranges:

    nonoverlapping_ranges = [r for r in fresh_id_ranges]

    while True:
        ranges_combined = False
        for i, r1 in enumerate(nonoverlapping_ranges[:-1]):
            for _j, r2 in enumerate(nonoverlapping_ranges[i+1:]):
                j = i + _j + 1
                if is_overlapping(r1, r2):
                    r = combine(r1, r2)
                    new_ranges = [r]
                    for k, _r in enumerate(nonoverlapping_ranges):
                        if k == i or k == j:
                            continue
                        new_ranges.append(_r)
                    nonoverlapping_ranges = new_ranges
                    ranges_combined = True
                    break
            if ranges_combined:
                break
        if not ranges_combined:
            break

    return nonoverlapping_ranges


def part1(puzzle_input: List[str]) -> int:
    idb = IngredientDB(puzzle_input)
    return len(idb.get_fresh_ids())


def part2(puzzle_input: str) -> int:
    idb = IngredientDB(puzzle_input)
    return idb.count_all_fresh_ids()


if __name__ == '__main__':
    ### THE TESTS
    test_input = dedent("""
        3-5
        10-14
        16-20
        12-18

        1
        5
        8
        11
        17
        32                    
    """).strip().split('\n')
    idb = IngredientDB(test_input)

    assert idb.is_id_fresh(5)
    assert not idb.is_id_fresh(1)

    assert part1(test_input) == 3

    assert is_overlapping((1, 5), (3, 7))
    assert is_overlapping((1, 5), (1, 5))
    assert is_overlapping((1, 5), (2, 4))
    assert is_overlapping((1, 5), (1, 3))
    assert not is_overlapping((1, 5), (7, 9))
    assert not is_overlapping((7, 9), (1, 5))

    assert part2(test_input) == 14

    ### THE REAL THING
    puzzle_input = helper.read_input_lines()
    print(f'Part 1: {part1(puzzle_input)}')
    print(f'Part 2: {part2(puzzle_input)}')
