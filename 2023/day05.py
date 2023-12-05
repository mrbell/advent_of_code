from typing import List, Tuple, Dict
from dataclasses import dataclass
import helper


@dataclass
class AlmanacMap:
    source_target_maps: List[Tuple[int, int, int]]
    
    def target(self, source_val: int) -> int:
        target_val = None
        for the_map in self.source_target_maps:
            if the_map[1] <= source_val < the_map[1] + the_map[2]:
                target_val = the_map[0] + source_val - the_map[1]
                break 

        return target_val if target_val is not None else source_val


@dataclass
class Almanac:
    seeds: List[int]
    maps: Dict[str, Tuple[str, AlmanacMap]]

    def from_to(self, source_type, target_type, source_val):
        t, m = self.maps[source_type]
        v = source_val

        while t != target_type:
            v = m.target(v)
            t, m = self.maps[t]

        return  m.target(v)


def parse_almanac(puzzle_input: str) -> Almanac:
    parts = puzzle_input.strip().split('\n\n')

    seeds = [int(s) for s in parts[0].split(': ')[1].split()]

    maps = {}
    for part in parts[1:]:
        source_type, target_type = part.split(':')[0].replace(' map', '').split('-to-')
        source_target_maps = []
        for line in part.splitlines()[1:]:
            source, target, size = [int(s) for s in line.split()]
            source_target_maps.append((source, target, size))
        maps[source_type] = (target_type, AlmanacMap(source_target_maps))
    
    return Almanac(seeds, maps)


def parse_seeds(seed_input: List[int]) -> List[int]:
    seeds = []
    for i, s in enumerate(seed_input):
        if i % 2 == 0:
            seeds.extend(list(range(s, s + seed_input[i + 1])))
    return seeds


def part1(puzzle_input: str) -> int:
    almanac = parse_almanac(puzzle_input)
    locations = []
    for seed in almanac.seeds:
        locations.append(almanac.from_to('seed', 'location', seed))
    return min(locations)


def part2(puzzle_input: str) -> int:
    almanac = parse_almanac(puzzle_input)
    locations = []
    seeds = parse_seeds(almanac.seeds)
    for seed in seeds:
        locations.append(almanac.from_to('seed', 'location', seed))
    return min(locations)


if __name__ == '__main__':
    ### THE TESTS
    test_input = '''seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4'''

    assert part1(test_input) == 35
    assert part2(test_input) == 46


    ### THE REAL THING
    puzzle_input = helper.read_input()
    print(f'Part 1: {part1(puzzle_input)}')
    print(f'Part 2: {part2(puzzle_input)}')
