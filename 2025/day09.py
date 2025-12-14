from typing import List, Tuple, Union, Set, Dict, Callable
import helper
from textwrap import dedent
from math import sqrt


class Point:
    def __init__(self, coords: Union[str, Tuple[int, int]]):
        if isinstance(coords, str):
            self.x, self.y = (
                int(v) for v in coords.split(',')
            )
        else:
            self.x, self.y = coords

    def __repr__(self) -> str:
        return f"Point('{self.x},{self.y}')"
    
    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def distance_to(self, other_point: 'Point') -> float: 
        return sqrt(
            (self.x - other_point.x) ** 2 + 
            (self.y - other_point.y) ** 2 
        )
    
    def __eq__(self, other_point: 'Point') -> bool:
        return self.x == other_point.x and self.y == other_point.y


def compute_area(p1: Point, p2: Point) -> int:
    return (abs(p2.x - p1.x) + 1) * (abs(p2.y - p1.y) + 1)


def parse_points(points: List[str]) -> List[Point]:
    return [Point(line) for line in points]


def parse_tiles(points: List[str]) -> Tuple[List[Point], List[Point]]:
    red_tiles = parse_points(points)
    green_tiles = []
    for i, t in enumerate(red_tiles):
        t2 = red_tiles[(i + 1) % len(red_tiles)]
        dx, dy = 0, 0
        if t2.x == t.x:
            dy = 1 if t2.y > t.y else -1
            n = abs(t2.y - t.y)
        elif t2.y == t.y:
            dx = 1 if t2.x > t.x else -1
            n = abs(t2.x - t.x)
        for i in range(1, n):
            green_tiles.append(Point(
                f'{t.x + i * dx},{t.y + i * dy}'
            ))
    
    return red_tiles, green_tiles


def find_largest_area(points: List[Point]) -> int:
    max_area = -1
    for i, p1 in enumerate(points[:-1]):
        for p2 in points[i + 1:]:
            area = compute_area(p1, p2)
            if area > max_area:
                max_area = area
    return max_area


def pip(point: Point, polygon: List[Point]) -> bool:
    intersection_count = 0
    for i, p1 in enumerate(polygon):
        p2 = polygon[(i + 1) % len(polygon)]

        # Check only vertical edges
        if p1.x != p2.x: 
            continue

        if ((p1.y < point.y < p2.y) or (p2.y < point.y < p1.y)) and p1.x > point.x:
            intersection_count += 1
    
    return (intersection_count % 2) == 1


def area_filled(p1: Point, p2: Point, grid_points: List[List[Point]], cell_filled: List[List[bool]]) -> bool:

    if p1.x == p2.x or p1.y == p2.y:
        return True

    x_min, x_max = min(p1.x, p2.x), max(p1.x, p2.x)
    y_min, y_max = min(p1.y, p2.y), max(p1.y, p2.y)

    for i, row in enumerate(grid_points[:-1]):
        for j, cell in enumerate(row[:-1]):
            if cell.x < x_min or cell.y < y_min or cell.x >= x_max or cell.y >= y_max:
                # Outside of the rectangle made by p1 and p2
                continue

            if not cell_filled[i][j]:
                return False
    
    return True


def part1(puzzle_input: str) -> int:
    points = parse_points(puzzle_input)
    max_area = find_largest_area(points)
    return max_area


def part2(puzzle_input: str) -> int:
    red_tiles = parse_points(puzzle_input)

    max_area = -1
    grid_corners = make_grid(red_tiles)
    cells_filled = infill(red_tiles, grid_corners)

    for i, p1 in enumerate(red_tiles[:-1]):
        for p2 in red_tiles[i + 1:]:
            area = compute_area(p1, p2)
            if area <= max_area:
                continue
            if area_filled(p1, p2, grid_corners, cells_filled):
                max_area = area

    return max_area


def make_grid(red_tiles: List[Point]) -> List[List[Point]]:

    xs = sorted(set([t.x for t in red_tiles]))
    ys = sorted(set([t.y for t in red_tiles]))

    grid_points = []
    for y in ys:
        row = []
        for x in xs:
            row.append(Point((x, y)))
        grid_points.append(row)
    
    return grid_points


def infill(red_tiles: List[Point], grid: List[List[Point]]) -> List[List[bool]]:
    
    is_filled = []
    for i, row in enumerate(grid[:-1]):
        is_filled_row = []
        for j, tlc_coords in enumerate(row[:-1]):
            test_point = Point((
                (tlc_coords.x + grid[i+1][j+1].x) / 2,
                (tlc_coords.y + grid[i+1][j+1].y) / 2
            ))
            is_filled_row.append(pip(test_point, red_tiles))

        is_filled.append(is_filled_row)
    
    return is_filled


if __name__ == '__main__':
    
    ### THE TESTS
    test_input = dedent("""
        7,1
        11,1
        11,7
        9,7
        9,5
        2,5
        2,3
        7,3
    """).strip().split('\n')


    points = parse_points(test_input)
    assert pip(Point((8, 3)), points)
    assert pip(Point((5, 4)), points)
    assert pip(Point((9, 3)), points)

    assert not pip(Point((10, 6)), [
        Point((1, 1)),
        Point((1, 3)),
        Point((5, 3)),
        Point((5, 1))
    ])

    assert part1(test_input) == 50
    assert part2(test_input) == 24


    test_input = dedent("""
        1,1
        5,1
        5,3
        7,3
        7,1
        10,1
        10,6
        1,6             
    """).strip().split('\n')
    assert part2(test_input) == 30

    '''
    ............
    .x...x.x..x.
    ............
    .....x.x....
    ............
    ............
    .x........x.
    ............
    '''

    print("Tests passed!")

    ### THE REAL THING
    puzzle_input = helper.read_input_lines()
    r, g = parse_tiles(puzzle_input)
    print(f'Part 1: {part1(puzzle_input)}')
    print(f'Part 2: {part2(puzzle_input)}')
