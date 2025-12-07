from typing import List, Tuple, Optional
import helper
from textwrap import dedent
from collections import defaultdict


type Coordinate = Tuple[int, int]


class TachyonManifold:
    START_CHAR = 'S'
    SPLITTER_CHAR = '^'

    def __init__(self, manifold: List[str]):
        self.manifold = manifold
        self.n_rows = len(manifold)
        self.n_cols = len(manifold[0])

    def find_start(self):
        for row_index, row in enumerate(self.manifold):
            for col_index, col in enumerate(row):
                if col == self.START_CHAR:
                    return (row_index, col_index)
    
    def is_oob(self, coordinate: Coordinate) -> bool:
        if (
            (0 <= coordinate[0] < self.n_rows) and 
            (0 <= coordinate[1] < self.n_cols)
        ):
            return False
        return True

    def __getitem__(self, coordinate: Coordinate) -> Optional[str]: 
        if self.is_oob(coordinate):
            return None
        else:
            return self.manifold[coordinate[0]][coordinate[1]]


class TachyonBeam:
    def __init__(self, manifold: TachyonManifold, start_coordinates: Optional[Coordinate]=None):
        self.current_location = start_coordinates if start_coordinates else manifold.find_start()
        self.path = [self.current_location]
        self.manifold = manifold
    
    def step(self):
        self.current_location = (self.current_location[0] + 1, self.current_location[1])
        self.path.append(self.current_location)
    
    def side_step(self, dir: int):
        self.current_location = (self.current_location[0], self.current_location[1] + dir)
        self.path.append(self.current_location)

    def copy(self):
        new_beam = TachyonBeam(self.manifold, self.current_location)
        new_beam.path = self.path
        return new_beam

    def split(self) -> List[TachyonBeam]:

        split_beams = []

        for d_col in [-1, 1]:
            new_beam = self.copy()
            new_beam.side_step(d_col)
            split_beams.append(new_beam)
        
        return split_beams

    def propagate(self) -> bool:

        while True:
            self.step()
            current_location = self.manifold[self.current_location]

            if current_location is None:
                # Off the board, stop, return that we've reached the end
                return True
            elif current_location == TachyonManifold.SPLITTER_CHAR:
                # We hit a splitter, stop, return that we've hit a splitter
                return False
            else:
                continue


def consolidate_beams(beams: List[TachyonBeam]) -> List[TachyonBeam]:
    reduced_beams = {}
    for beam in beams:
        if beam.path[0] not in reduced_beams:
            reduced_beams[beam.path[0]] = beam
    return list(reduced_beams.values())


def count_splits(manifold: TachyonManifold) -> int:

    row = 0
    beam_cols = [manifold.find_start()[1]]
    splits = 0

    for row in manifold.manifold:
        new_beam_cols = []
        for beam_col in beam_cols:
            if row[beam_col] == manifold.SPLITTER_CHAR:
                splits += 1
                new_beam_cols.append(beam_col + 1)
                new_beam_cols.append(beam_col - 1)
            else:
                new_beam_cols.append(beam_col)
        beam_cols = list(set(new_beam_cols))

    return splits


def trace_paths(beam: TachyonBeam) -> List[TachyonBeam]:
    hit_the_end = beam.propagate()

    if hit_the_end:
        return [beam]
    
    # hit a split
    paths = []
    new_beams = beam.split() 
    for b in new_beams:
        paths.extend(trace_paths(b))
    return paths


def count_paths(manifold: TachyonManifold) -> int:
    
    beam_cols = defaultdict(int)
    beam_cols[manifold.find_start()[1]] = 1

    for row in manifold.manifold:
        new_beam_cols = defaultdict(int)
        for beam_col in beam_cols:
            if row[beam_col] == manifold.SPLITTER_CHAR:
                new_beam_cols[beam_col + 1] += beam_cols[beam_col]
                new_beam_cols[beam_col - 1] += beam_cols[beam_col]
            else:
                new_beam_cols[beam_col] += beam_cols[beam_col]
        beam_cols = new_beam_cols
    return sum(beam_cols.values())


def part1(puzzle_input: List[str]) -> int:
    manifold = TachyonManifold(puzzle_input)
    return count_splits(manifold)


def part2(puzzle_input: List[str]) -> int:
    manifold = TachyonManifold(puzzle_input)
    return count_paths(manifold)


if __name__ == '__main__':
    ### THE TESTS
    test_input = dedent("""
        .......S.......
        ...............
        .......^.......
        ...............
        ......^.^......
        ...............
        .....^.^.^.....
        ...............
        ....^.^...^....
        ...............
        ...^.^...^.^...
        ...............
        ..^...^.....^..
        ...............
        .^.^.^.^.^...^.
        ...............
    """).strip().split('\n')
    assert part1(test_input) == 21
    assert part2(test_input) == 40

    ### THE REAL THING
    puzzle_input = helper.read_input_lines()
    print(f'Part 1: {part1(puzzle_input)}')
    print(f'Part 2: {part2(puzzle_input)}')
