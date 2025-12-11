from typing import List, Tuple, Union, Set, Dict, Callable
import helper
from textwrap import dedent
from math import sqrt
from functools import lru_cache


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


def point_in_polygon(point: Point, polygon: Set[Point]) -> bool:

    x_max = max(polygon, key=lambda x: x.x).x + 1

    crossing_count = 0
    on_edge = False
    current_position = point
    edge_above = False
    edge_below = False

    while current_position.x <= x_max:
        
        current_point_on_edge = current_position in polygon

        # Off to on edge
        if not on_edge and current_point_on_edge:
            on_edge = True
            point_above = Point((current_position.x, current_position.y + 1))
            point_below = Point((current_position.x, current_position.y - 1))
            edge_above = point_above in polygon
            edge_below = point_below in polygon

        # On to off edge
        elif on_edge and not current_point_on_edge:
            on_edge = False
            point_above = Point((current_position.x-1, current_position.y + 1))
            point_below = Point((current_position.x-1, current_position.y - 1))
            edge_above_2 = point_above in polygon
            edge_below_2 = point_below in polygon
            
            if (edge_above and edge_below) or (edge_above and edge_below_2) or (edge_above_2 and edge_below):
                crossing_count += 1
        # On edge

        current_position = Point((current_position.x + 1, current_position.y))

    return (crossing_count % 2) == 1


def lines_intersect(l1: Tuple[Point, Point], l2: Tuple[Point, Point]) -> bool:

    t = (l1[0].x - l2[0].x) * (l2[0].y - l2[1].y) - (l1[0].y - l2[0].y) * (l2[0].x - l2[1].x) / (
        (l1[0].x - l1[1].x) * (l2[0].y - l2[1].y) - (l1[0].y - l1[1].y) * (l2[0].x - l2[1].x)
    )

    u = (l1[0].x - l1[1].x) * (l1[0].y - l2[0].y) - (l1[0].y - l1[1].y) * (l1[0].x - l2[0].x) / (
        (l1[0].x - l1[1].x) * (l2[0].y - l2[1].y) - (l1[0].y - l1[1].y) * (l2[0].x - l2[1].x)
    )

    return 0 <= t <= 1 and 0 <= u <= 1


def slope_intercept_from_points(lk: Tuple[Point, Point]) -> Tuple[float, float]:

    mk = (lk[1].y - lk[0].y) / (lk[1].x - lk[0].x)
    bk = lk[0].y - mk * lk[0].x

    return mk, bk


def point_between(p: Point, ls: Tuple[Point, Point]) -> bool:

    px, py = p.x, p.y
    ls0x, ls0y = ls[0].x, ls[0].y
    ls1x, ls1y = ls[1].x, ls[1].y

    xs = sorted([ls0x, ls1x])
    ys = sorted([ls0x, ls1x])

    return xs[0] <= px <= xs[1] and ys[0] <= py <= ys[1]


def lines_intersect2(lk: Tuple[Point, Point], ln: Tuple[Point, Point]) -> bool:

    mk, bk = slope_intercept_from_points(lk)
    mn, bn = slope_intercept_from_points(ln)

    x_int = (bn - bk) / (mk - mn)
    y_int = mk * (bn - bk) / (mk - mn) + bk

    p = Point((x_int, y_int))

    return point_between(p, lk) and point_between(p, ln)


def point_in_polygon_faster(point: Point, polygon: List[Point]) -> bool:
    # Define ray
    # Loop over polygon edges and count intersections with the ray
    # Return true if intersections is odd

    origin = Point((0, 0))
    intersection_count = 0

    for i, p1 in enumerate(polygon):
        p2 = polygon[(i + 1) % len(polygon)]

        if lines_intersect((point, origin), (p1, p2)):
            intersection_count += 1
    
    return (intersection_count % 2) == 1


def area_filled(p1: Point, p2: Point, tiles: Set[Point], inside_function: Callable) -> bool:

    x_min, x_max = min(p1.x, p2.x), max(p1.x, p2.x)
    y_min, y_max = min(p1.y, p2.y), max(p1.y, p2.y)

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


def find_largest_filled_area(red_tiles: List[Point], green_tiles: List[Point], inside_function: Callable) -> int:
    max_area = -1
    tiles = set(red_tiles + green_tiles)
    for i, p1 in enumerate(red_tiles[:-1]):
        for p2 in red_tiles[i + 1:]:
            area = compute_area(p1, p2)
            if area <= max_area:
                continue
            if area_filled(p1, p2, tiles, inside_function):
                if area > max_area:
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
        result = point_in_polygon_faster(point, red_tiles)
        cache[key] = result
        return result


    max_area = find_largest_filled_area(red_tiles, green_tiles, inside_function=point_in_polygon_cached)
    return max_area


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

    assert lines_intersect2(
        (Point((7, 3)), Point((7, 1))), 
        (Point((8, 3)), Point((0, 0)))
    )

    points = parse_points(test_input)
    assert point_in_polygon_faster(Point((8, 3)), points)

    assert part1(test_input) == 50
    assert part2(test_input) == 24

    print("Tests passed!")

    ### THE REAL THING
    puzzle_input = helper.read_input_lines()
    print(f'Part 1: {part1(puzzle_input)}')
    print(f'Part 2: {part2(puzzle_input)}')


    # (7, 3) -> (7, 1)
    # should intersect 
    # (8, 3) -> (0, 0)