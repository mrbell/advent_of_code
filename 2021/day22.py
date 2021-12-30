from itertools import product
from dataclasses import dataclass
from typing import List, Tuple, Set
import helper


@dataclass
class Cuboid:
    action: int
    x_range: Tuple[int, int]
    y_range: Tuple[int, int]
    z_range: Tuple[int, int]

    def is_init(self) -> bool:
        for dim in 'xyz':
            if (
                min(getattr(self, f'{dim}_range')) < -50 or 
                max(getattr(self, f'{dim}_range')) > 50
            ):
                return False
        return True
    
    def get_coords(self) -> Set[Tuple[int, int, int]]:
        coords = set(
            product(
                range(self.x_range[0], self.x_range[1] + 1),
                range(self.y_range[0], self.y_range[1] + 1),
                range(self.z_range[0], self.z_range[1] + 1)
            )
        )
        return coords


def parse_line(the_line: str) -> Cuboid:
    action = 1 if 'on' in the_line else 0
    limits = the_line.replace('on ', '').replace('off ', '')
    split_limits = limits.split(',')
    limit_tuples = []
    for sl in split_limits:
        limit_tuples.append(tuple(int(v) for v in sl.split('=')[1].split('..')))
    return Cuboid(action, *limit_tuples)


def reboot(steps: List[Cuboid]) -> Set[Tuple[int, int, int]]:
    on_cubes = set() 
    for step in steps:
        if not step.is_init():
            continue
        coords = step.get_coords()
        if step.action == 1:
            on_cubes = on_cubes.union(coords)
        else:
            on_cubes = on_cubes.difference(coords)
    return on_cubes 


if __name__ == '__main__':
    ### THE TESTS
    small_test = '''on x=10..12,y=10..12,z=10..12
on x=11..13,y=11..13,z=11..13
off x=9..11,y=9..11,z=9..11
on x=10..10,y=10..10,z=10..10'''.split('\n')

    small_test_cuboids = [parse_line(l) for l in small_test]
    on_cubes = reboot(small_test_cuboids)
    assert len(on_cubes) == 39

    larger_test = '''on x=-20..26,y=-36..17,z=-47..7
on x=-20..33,y=-21..23,z=-26..28
on x=-22..28,y=-29..23,z=-38..16
on x=-46..7,y=-6..46,z=-50..-1
on x=-49..1,y=-3..46,z=-24..28
on x=2..47,y=-22..22,z=-23..27
on x=-27..23,y=-28..26,z=-21..29
on x=-39..5,y=-6..47,z=-3..44
on x=-30..21,y=-8..43,z=-13..34
on x=-22..26,y=-27..20,z=-29..19
off x=-48..-32,y=26..41,z=-47..-37
on x=-12..35,y=6..50,z=-50..-2
off x=-48..-32,y=-32..-16,z=-15..-5
on x=-18..26,y=-33..15,z=-7..46
off x=-40..-22,y=-38..-28,z=23..41
on x=-16..35,y=-41..10,z=-47..6
off x=-32..-23,y=11..30,z=-14..3
on x=-49..-5,y=-3..45,z=-29..18
off x=18..30,y=-20..-8,z=-3..13
on x=-41..9,y=-7..43,z=-33..15
on x=-54112..-39298,y=-85059..-49293,z=-27449..7877
on x=967..23432,y=45373..81175,z=27513..53682'''.split('\n')

    test_cuboids = [parse_line(l) for l in larger_test]
    on_cubes = reboot(test_cuboids)
    assert len(on_cubes) == 590784

    ### THE REAL THING
    puzzle_input = helper.read_input_lines()

    cuboids = [parse_line(l) for l in puzzle_input]
    on_cubes = reboot(cuboids)

    print(f'Part 1: {len(on_cubes)}')
    print(f'Part 2: {""}')
