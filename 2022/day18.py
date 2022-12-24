from typing import List, Tuple
import helper


class Droplet(object):
    def __init__(self, cube_coords: List[str]):
        self.cubes: List[Tuple[int, int, int]] = []
        self._surface_area = 0
        for cube_coord in cube_coords:
            x, y, z = cube_coord.split(',')
            self.cubes.append((int(x), int(y), int(z)))


    @property 
    def surface_area(self) -> int:
        if self._surface_area == 0:
            for cube in self.cubes:
                for side in [(0,0,1), (0,0,-1), (0,1,0), (0,-1,0), (1,0,0), (-1,0,0)]:
                    if (cube[0] + side[0], cube[1] + side[1], cube[2] + side[2]) not in self.cubes:
                        self._surface_area += 1
        return self._surface_area
    

if __name__ == '__main__':
    ### THE TESTS
    test_input = '''2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5'''.split('\n')

    test_droplet = Droplet(test_input)
    assert test_droplet.surface_area == 64

    ### THE REAL THING
    puzzle_input = helper.read_input_lines()
    droplet = Droplet(puzzle_input)
    print(f'Part 1: {droplet.surface_area}')
    print(f'Part 2: {""}')
