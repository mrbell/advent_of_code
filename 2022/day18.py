from typing import List, Tuple, Optional, Set
import helper


# For part 2, here is what I'm thinking
# An exterior surface is one for which you can find a path to the outside by moving between 
# adjacent "air" cubes (those not in the droplet, can't move diagonally)
# Find the extreme coordinates in each direction... once you are able to move beyond those 
# bounds you're "outside"
# For each cube in the droplet, search out from each side until you hit the outside or a dead end
# Count each side that leads to the outside as an exterior surface


Cube = Tuple[int, int, int]
directions = [(0,0,1), (0,0,-1), (0,1,0), (0,-1,0), (1,0,0), (-1,0,0)]


class Droplet(object):
    def __init__(self, cube_coords: List[str]):
        self.cubes: Set['Cube'] = set()
        self._surface_area = 0
        for cube_coord in cube_coords:
            x, y, z = cube_coord.split(',')
            self.cubes.add((int(x), int(y), int(z)))
        self._bounds = None

    @property 
    def surface_area(self) -> int:
        if self._surface_area == 0:
            for cube in self.cubes:
                for side in directions:
                    if (cube[0] + side[0], cube[1] + side[1], cube[2] + side[2]) not in self.cubes:
                        self._surface_area += 1
        return self._surface_area

    @property
    def bounds(self) -> Tuple[Tuple[int, int], Tuple[int, int], Tuple[int, int]]:
        if self._bounds is None:
            padding = 0
            x_min = min([cube[0] for cube in self.cubes]) - padding
            x_max = max([cube[0] for cube in self.cubes]) + padding
            y_min = min([cube[1] for cube in self.cubes]) - padding
            y_max = max([cube[1] for cube in self.cubes]) + padding
            z_min = min([cube[2] for cube in self.cubes]) - padding
            z_max = max([cube[2] for cube in self.cubes]) + padding

            self._bounds = ((x_min, x_max), (y_min, y_max), (z_min, z_max))
        return self._bounds

    def oob(self, cube: 'Cube') -> bool:
        x, y, z = cube
        x_min, x_max = self.bounds[0]
        y_min, y_max = self.bounds[1]
        z_min, z_max = self.bounds[2]
        return x < x_min or x > x_max or y < y_min or y > y_max or z < z_min or z > z_max


def seek_exterior(
    droplet: 'Droplet', 
    coord: 'Cube', 
    leads_out: Set['Cube'],
    leads_to_dead_end: Set['Cube'],
    visited_coords: Optional[List['Cube']]=None,
) -> bool:
    if visited_coords is None:
        visited_coords = []

    if droplet.oob(coord):
        return True
    if coord in droplet.cubes:
        return False
    if coord in leads_out:
        return True
    if coord in leads_to_dead_end:
        return False

    for side in directions:
        next_coord = (coord[0] + side[0], coord[1] + side[1], coord[2] + side[2])
        if next_coord in visited_coords:
            continue
        if next_coord in leads_to_dead_end:
            return False
        if next_coord in leads_out:
            return True
        if seek_exterior(droplet, next_coord, leads_out, leads_to_dead_end, visited_coords + [coord]):
            leads_out.add(coord)
            return True
    
    leads_to_dead_end.add(coord)
    return False


def exterior_surface_area(droplet: 'Droplet') -> int:
    
    surface_area = 0

    leads_out = set()
    leads_to_dead_end = set()

    for cube in droplet.cubes:
        for side in directions:
            current_position = (cube[0] + side[0], cube[1] + side[1], cube[2] + side[2]) 
            if seek_exterior(droplet, current_position, leads_out, leads_to_dead_end): 
                surface_area += 1
    
    return surface_area


if __name__ == '__main__':
    ### THE TESTS
    # Made some test cases with https://voxelator.com/#
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
2,3,5'''.split('\n')  # 64 total, 58 exterior

    test_droplet = Droplet(test_input)
    assert test_droplet.surface_area == 64
    assert exterior_surface_area(test_droplet) == 58 

    test_input += [
        '2,3,6',
        '3,3,5',
        '3,3,6',
        '2,2,7',
        '4,2,5',
        '3,2,7',
        '4,2,6',
        '3,1,5',
        '2,1,6',
        '3,1,6',
        '2,4,2',
        '3,4,2',
        '2,3,3',
        '3,3,3'
    ]  # 106 total, 94 exterior

    test_droplet = Droplet(test_input)
    assert test_droplet.surface_area == 106 
    assert exterior_surface_area(test_droplet) == 94 

    test_input = '''0,0,0
1,0,0
2,0,0
3,0,0
4,0,0
0,1,0
1,1,0
2,1,0
3,1,0
4,1,0
0,2,0
1,2,0
2,2,0
3,2,0
4,2,0
0,0,1
0,1,1
0,2,1
1,0,1
0,0,2
1,0,2
0,1,2
0,2,2
1,2,1
1,2,2
1,1,2
4,0,1
4,0,2
4,1,1
4,2,1
4,1,2
4,2,2
3,0,1
3,0,2
3,2,1
3,2,2
3,1,2
2,0,1
2,2,1'''.split('\n')  # 94 total and exterior

    test_droplet = Droplet(test_input)
    assert test_droplet.surface_area == 94 
    assert exterior_surface_area(test_droplet) == 94 

    test_input += ['2,1,2']  # 96 total, 82 exterior

    test_droplet = Droplet(test_input)
    assert test_droplet.surface_area == 96 
    assert exterior_surface_area(test_droplet) == 82 

    test_input = '''1,1,1
2,1,1
3,1,1
4,1,1
5,1,1
6,1,1
1,2,1
2,2,1
3,2,1
4,2,1
5,2,1
6,2,1
1,3,1
2,3,1
3,3,1
4,3,1
5,3,1
6,3,1
1,1,2
2,1,2
3,1,2
4,1,2
5,1,2
6,1,2
1,2,2
6,2,2
1,3,2
2,3,2
3,3,2
4,3,2
5,3,2
6,3,2
1,1,3
2,1,3
3,1,3
4,1,3
5,1,3
6,1,3
1,2,3
2,2,3
3,2,3
4,2,3
5,2,3
6,2,3
1,3,3
2,3,3
3,3,3
4,3,3
5,3,3
6,3,3'''.split('\n')  # 108 total, 90 exterior

    test_droplet = Droplet(test_input)
    assert test_droplet.surface_area == 108 
    assert exterior_surface_area(test_droplet) == 90 

    test_input = '''0,0,0
1,0,0
2,0,0
3,0,0
4,0,0
0,1,0
1,1,0
2,1,0
3,1,0
4,1,0
0,2,0
1,2,0
2,2,0
3,2,0
4,2,0
0,3,0
1,3,0
2,3,0
3,3,0
4,3,0
0,4,0
1,4,0
2,4,0
3,4,0
4,4,0
0,0,1
0,0,2
0,0,3
0,0,4
0,1,1
0,1,2
0,1,3
0,1,4
0,2,1
0,2,2
0,2,3
0,2,4
0,3,1
0,3,2
0,3,3
0,3,4
0,4,1
0,4,2
0,4,3
0,4,4
1,0,1
1,0,2
1,0,3
1,0,4
2,0,1
2,0,2
2,0,3
2,0,4
3,0,1
3,0,2
3,0,3
3,0,4
4,0,1
4,0,2
4,0,3
4,0,4
1,4,1
1,4,2
1,4,3
1,4,4
2,4,1
2,4,2
2,4,3
2,4,4
3,4,1
3,4,2
3,4,3
3,4,4
4,4,1
4,4,2
4,4,3
4,4,4
1,3,4
1,2,4
1,1,4
2,3,4
2,2,4
2,1,4
3,3,4
3,2,4
3,1,4
4,3,4
4,2,4
4,1,4
4,3,3
4,2,3
4,1,3
4,3,2
4,2,2
4,1,2
4,3,1
4,2,1
4,1,1'''.split('\n')  # 204 total, 150 exterior
    
    test_droplet = Droplet(test_input)
    assert test_droplet.surface_area == 204 
    assert exterior_surface_area(test_droplet) == 150 

    test_input += '''0,5,0
0,5,-1
-1,5,0
-1,5,-1
0,5,-2
-1,5,-2
-2,5,-1
-2,5,0
-1,4,0
0,4,-1
0,4,-2
-2,4,0
0,3,-1
-1,3,0
-1,3,-1
-1,4,-2
-2,4,-1'''.split('\n')  # 248 total, 188 exterior
    
    test_droplet = Droplet(test_input)
    assert test_droplet.surface_area == 248 
    assert exterior_surface_area(test_droplet) == 188 

    test2 = '''1,1,1
2,1,1
3,1,1
4,1,1
5,1,1
6,1,1
1,2,1
2,2,1
4,2,1
5,2,1
6,2,1
1,3,1
2,3,1
3,3,1
4,3,1
5,3,1
6,3,1
1,4,1
2,4,1
3,4,1
4,4,1
5,4,1
6,4,1
1,1,2
2,1,2
3,1,2
4,1,2
5,1,2
6,1,2
1,2,2
6,2,2
1,3,2
6,3,2
1,4,2
2,4,2
3,4,2
4,4,2
5,4,2
6,4,2
1,1,3
2,1,3
3,1,3
4,1,3
5,1,3
6,1,3
1,2,3
2,2,3
3,2,3
4,2,3
5,2,3
6,2,3
1,3,3
2,3,3
3,3,3
4,3,3
5,3,3
6,3,3
1,4,3
2,4,3
3,4,3
4,4,3
5,4,3
6,4,3
1,1,4
2,1,4
3,1,4
4,1,4
5,1,4
6,1,4
1,2,4
6,2,4
1,3,4
6,3,4
1,4,4
2,4,4
3,4,4
4,4,4
5,4,4
6,4,4
1,1,5
2,1,5
3,1,5
4,1,5
5,1,5
6,1,5
1,2,5
2,2,5
3,2,5
4,2,5
5,2,5
6,2,5
1,3,5
2,3,5
3,3,5
4,3,5
5,3,5
6,3,5
1,4,5
2,4,5
3,4,5
4,4,5
5,4,5
6,4,5'''.split('\n')  # 178 exterior

    test_droplet = Droplet(test2)
    assert exterior_surface_area(test_droplet) == 178 

    test_input = '''1,1,1
2,1,1
3,1,1
4,1,1
5,1,1
6,1,1
1,2,1
2,2,1
3,2,1
4,2,1
5,2,1
6,2,1
1,3,1
2,3,1
3,3,1
4,3,1
5,3,1
6,3,1
1,1,2
2,1,2
3,1,2
4,1,2
5,1,2
6,1,2
1,2,2
6,2,2
1,3,2
2,3,2
3,3,2
4,3,2
5,3,2
6,3,2
1,1,3
2,1,3
3,1,3
4,1,3
5,1,3
6,1,3
1,2,3
2,2,3
3,2,3
4,2,3
5,2,3
6,2,3
1,3,3
2,3,3
3,3,3
4,3,3
5,3,3
6,3,3'''.split('\n')  # 86, 80
    
    test_droplet = Droplet(test_input)
    assert test_droplet.surface_area == 108 
    assert exterior_surface_area(test_droplet) == 90 

    test_input = '''2,2,3
2,4,3
2,3,2
2,3,4
3,2,3
3,4,3
3,3,2
3,3,4
4,3,3'''.split('\n')  # 46 for both

    # This test is failing!
    test_droplet = Droplet(test_input)
    assert test_droplet.surface_area == 46
    assert exterior_surface_area(test_droplet) == 46


    ### THE REAL THING
    puzzle_input = helper.read_input_lines()
    droplet = Droplet(puzzle_input)
    print(f'Part 1: {droplet.surface_area}')  # 4400 is the answer
    surface_area = exterior_surface_area(droplet) 
    print(f'Part 2: {surface_area}')  # 2510 is too low
