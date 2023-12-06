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
    
    def target_ranges(self, source_start_val: int, source_end_val: int) -> List[Tuple[int, int]]:
        '''Given a source range, return a list of target ranges that are mapped to by the source range'''

        target_ranges = []

        maps = sorted(self.source_target_maps, key=lambda x: x[1])

        if source_start_val >= (maps[-1][1] + maps[-1][2]) or source_end_val < maps[0][1]:
            # no overlap with the map source ranges
            target_ranges.append((source_start_val, source_end_val))
            return target_ranges

        if source_start_val < maps[0][1]:
            # source range starts before the first map source range
            target_ranges.append((source_start_val, min(source_end_val, maps[0][1] - 1)))
            source_start_val = maps[0][1]

        if source_end_val >= (maps[-1][1] + maps[-1][2]):
            # source range ends after the last map source range
            target_ranges.append((max(source_start_val, maps[-1][1] + maps[-1][2]), source_end_val))
            source_end_val = maps[-1][1] + maps[-1][2] - 1

        # At this point the source range is guaranteed to overlap with the map source ranges
        for i, the_map in enumerate(maps):
            
            if source_start_val >= (the_map[1] + the_map[2]):
                # source range starts after this map source range
                continue
            
            if source_start_val < the_map[1]:
                # source range starts before this map source range
                target_ranges.append((source_start_val, min(source_end_val, the_map[1] + the_map[2] - 1)))
                source_start_val = the_map[1]

            if source_end_val < the_map[1]:
                # source range ends before this map source range
                break

            target_val_start = self.target(source_start_val)
            if source_end_val < (the_map[1] + the_map[2]):
                # source range ends before this map source range
                target_ranges.append((target_val_start, self.target(source_end_val)))
                break
            else:
                # source range ends after this map source range
                target_val_end = self.target(the_map[1] + the_map[2] - 1)
                target_ranges.append((target_val_start, target_val_end))
                source_start_val = the_map[1] + the_map[2]

        return target_ranges


@dataclass
class Almanac:
    seeds: List[int]
    maps: Dict[str, Tuple[str, AlmanacMap]]

    def from_to(self, source_type, target_type, source_val):
        t, m = self.maps[source_type]
        v = source_val

        v = m.target(v)
        while t != target_type:
            t, m = self.maps[t]
            v = m.target(v)

        return v

    def range_from_to(self, source_type, target_type, source_start_val, source_end_val):
        t, m = self.maps[source_type]
        vs = [(source_start_val, source_end_val)]

        while t != target_type:
            new_vs = []
            for v in vs:
                new_v = m.target_ranges(*v)
                new_vs.extend(new_v)
            vs = new_vs
            t, m = self.maps[t]

        new_vs = []
        for v in vs:
            new_v = m.target_ranges(*v)
            new_vs.extend(new_v)
        vs = new_vs
        
        return vs


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
            seeds.append((s, s + seed_input[i + 1] - 1))
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
        locations.extend(almanac.range_from_to('seed', 'location', *seed))
    expanded_locations = []
    for location in locations:
        expanded_locations.extend(list(location))
    return min(expanded_locations)


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
