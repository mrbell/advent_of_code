from typing import List, Tuple
import helper


SAND_SOURCE = (500, 0)


def parse_input(inp: str) -> List[Tuple[int, int]]:
    to_return = []
    for vertex in inp.split(' -> '):
        to_return.append(tuple(map(int, vertex.split(','))))
    return to_return


def make_rock(inp: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    to_return = []

    for v1, v2 in zip(inp[:-1], inp[1:]):
        if v1[0] == v2[0]:
            step = -1 if v1[1] > v2[1] else 1
            for y in range(v1[1], v2[1], step):
                to_return.append((v1[0], y))
        else:
            step = -1 if v1[0] > v2[0] else 1
            
            for x in range(v1[0], v2[0], step):
                to_return.append((x, v1[1]))

    to_return.append(inp[-1])

    return to_return


class RockStructure(object):
    def __init__(self, inp: str):
        vertices = parse_input(inp)
        self.rock_points = make_rock(vertices)

    def intersects(self, point: Tuple[int, int]) -> bool:
        return point in self.rock_points


def fill_sand(
    rock_structures: List['RockStructure'],
    is_floor: bool=False,
    verbose: bool=False
) -> List[Tuple[int, int]]:
    max_depth = max(
        [
            max(rock_structure.rock_points, key=lambda x: x[1])[1] 
            for rock_structure in rock_structures
        ]
    )

    if is_floor:
        max_depth += 2
        rock_structures = [
            RockStructure(f'-1000,{max_depth} -> 1500,{max_depth}')
        ] + rock_structures

    sand_falling = False
    settled_sand_points = set() 
    new_sand_location = (SAND_SOURCE[0], SAND_SOURCE[1])
    n_printed = 0

    while new_sand_location[1] < max_depth:
        if not sand_falling:
            new_sand_location = (SAND_SOURCE[0], SAND_SOURCE[1])
            sand_falling = True
            if verbose:
                print('.', end='')
                n_printed += 1
                if n_printed % 100 == 0:
                    print()
        else:
            test_points = [
                (new_sand_location[0], new_sand_location[1] + 1),
                (new_sand_location[0] - 1, new_sand_location[1] + 1),
                (new_sand_location[0] + 1, new_sand_location[1] + 1)
            ]
            for test_point in test_points:
                if test_point in settled_sand_points:
                    continue
                if any([rock_structure.intersects(test_point) for rock_structure in rock_structures]):
                    continue
                new_sand_location = test_point
                break
            else:
                sand_falling = False
                settled_sand_points.add(new_sand_location)
                if new_sand_location == SAND_SOURCE:
                    break
    
    return list(settled_sand_points)


if __name__ == '__main__':
    ### THE TESTS
    test_input = '''498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9'''.split('\n')

    test_rock_structures = [RockStructure(inp) for inp in test_input]
    test_settled_sand_points = fill_sand(test_rock_structures)
    assert len(test_settled_sand_points) == 24

    test_settled_sand_points = fill_sand(test_rock_structures, is_floor=True)
    assert len(test_settled_sand_points) == 93

    ### THE REAL THING
    puzzle_input = helper.read_input_lines()
    rock_structures = [RockStructure(inp) for inp in puzzle_input]
    settled_sand_points = fill_sand(rock_structures)
    print(f'Part 1: {len(settled_sand_points)}')
    settled_sand_points = fill_sand(rock_structures, is_floor=True, verbose=True)
    print(f'Part 2: {len(settled_sand_points)}')
