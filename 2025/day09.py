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


def slope_intercept_from_points(lk: Tuple[Point, Point]) -> Tuple[float, float]:

    if lk[1].x == lk[0].x:
        return float('inf'), float('inf')

    mk = (lk[1].y - lk[0].y) / (lk[1].x - lk[0].x)
    bk = lk[0].y - mk * lk[0].x

    return mk, bk


def point_between(p: Point, ls: Tuple[Point, Point]) -> bool:

    px, py = p.x, p.y
    ls0x, ls0y = ls[0].x, ls[0].y
    ls1x, ls1y = ls[1].x, ls[1].y

    xs = sorted([ls0x, ls1x])
    ys = sorted([ls0y, ls1y])

    return xs[0] <= px <= xs[1] and ys[0] <= py <= ys[1]


def lines_intersect(lk: Tuple[Point, Point], ln: Tuple[Point, Point]) -> bool:

    mk, bk = slope_intercept_from_points(lk)
    mn, bn = slope_intercept_from_points(ln)

    if mk == float('inf') and mn == float('inf'):
        return False
    elif mk == float('inf'):
        x_int = lk[0].x
        y_int = mn * x_int + bn
    elif mn == float('inf'):
        x_int = ln[0].x
        y_int = mk * x_int + bk
    else:
        x_int = (bn - bk) / (mk - mn)
        y_int = int(mk * (bn - bk) / (mk - mn) + bk)

    p = Point((x_int, y_int))

    return point_between(p, lk) and point_between(p, ln)


def point_in_polygon(point: Point, polygon: List[Point]) -> bool:
    origin = Point((0, 0))
    intersection_count = 0

    # FIXME: Runs into problems when I hit a corner
    
    for i, p1 in enumerate(polygon):
        p2 = polygon[(i + 1) % len(polygon)]

        # If point is ON the edge, don't count it
        if ((p2.x == p1.x == point.x) or (p2.y == p1.y == point.y)) and point_between(point, (p1, p2)):
            return False

        if lines_intersect((point, origin), (p1, p2)):
            intersection_count += 1
        
    for poly_point in polygon:
        if poly_point.y == ((point.y / point.x) * poly_point.x):
            intersection_count -= 1
    
    return (intersection_count % 2) == 1


def area_filled(p1: Point, p2: Point, tiles: Set[Point], inside_function: Callable) -> bool:

    x_min, x_max = min(p1.x, p2.x), max(p1.x, p2.x)
    y_min, y_max = min(p1.y, p2.y), max(p1.y, p2.y)

    # FIXME: My assumption that corners and center are sufficient to test is wrong!

    corners = [
        Point((x_min, y_min)),
        Point((x_min, y_max)),
        Point((x_max, y_max)),
        Point((x_max, y_min)),
    ]

    center_point = Point(((x_min + x_max) // 2, ((y_min + y_max) // 2)))

    # All 4 corners must be on an edge tile and the central tile must 
    # be interior to the path
    for c in corners:
        if not c in tiles and not inside_function(c):
            return False
    
    if center_point in tiles:
        return True
    
    return inside_function(center_point)


def area_filled2(p1: Point, p2: Point, red_tiles: List[Point], green_tiles: List[Point], inside_function: Callable) -> bool:

    x_min, x_max = min(p1.x, p2.x), max(p1.x, p2.x)
    y_min, y_max = min(p1.y, p2.y), max(p1.y, p2.y)

    tiles = set(red_tiles + green_tiles)

    corners = [
        Point((x_min, y_min)),
        Point((x_min, y_max)),
        Point((x_max, y_max)),
        Point((x_max, y_min)),
    ]

    for c in corners:
        if not c in tiles and not inside_function(c):
            return False
    
    if any(point_in_polygon(t, corners) for t in red_tiles if t not in corners):
        return False
    
    return True # inside_function(center_point)


def find_largest_filled_area(red_tiles: List[Point], green_tiles: List[Point], inside_function: Callable) -> int:
    max_area = -1
    # tiles = set(red_tiles + green_tiles)
    for i, p1 in enumerate(red_tiles[:-1]):
        for p2 in red_tiles[i + 1:]:
            area = compute_area(p1, p2)
            if area <= max_area:
                continue
            # if area_filled(p1, p2, tiles, inside_function):
            if area_filled2(p1, p2, red_tiles, green_tiles, inside_function):
                max_area = area
    return max_area


def part1(puzzle_input: str) -> int:
    points = parse_points(puzzle_input)
    max_area = find_largest_area(points)
    return max_area


def part2(puzzle_input: str) -> int:
    red_tiles, green_tiles = parse_tiles(puzzle_input)

    cache: Dict[Tuple[int, int], bool] = {}
    def point_in_polygon_cached(point: Point):
        key = (point.x, point.y)
        if key in cache:
            return cache[key]
        result = point_in_polygon(point, red_tiles)
        cache[key] = result
        return result


    max_area = find_largest_filled_area(red_tiles, green_tiles, inside_function=point_in_polygon_cached)
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
            is_filled_row.append(point_in_polygon(test_point, red_tiles))

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

    assert lines_intersect(
        (Point((7, 3)), Point((7, 1))), 
        (Point((8, 3)), Point((0, 0)))
    )

    assert lines_intersect(
        (Point((8, 3)), Point((0, 0))),
        (Point((7, 3)), Point((7, 1))), 
    )
    
    assert lines_intersect(
        (Point((2, 3)), Point((7, 3))), 
        (Point((5, 4)), Point((0, 0))),
    )
    assert lines_intersect(
        (Point((5, 4)), Point((0, 0))),
        (Point((2, 3)), Point((7, 3))), 
    )

    points = parse_points(test_input)
    assert point_in_polygon(Point((8, 3)), points)
    assert point_in_polygon(Point((5, 4)), points)
    assert point_in_polygon(Point((9, 3)), points)

    assert not point_in_polygon(Point((10, 6)), [
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
    assert part2(test_input) == 20

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

    # 4730385534 is too high
