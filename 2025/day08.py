from typing import List, Tuple, Dict, Optional
import helper
from textwrap import dedent
from math import sqrt
from collections import defaultdict


class Point:
    def __init__(self, coords: str):
        self.x, self.y, self.z = (
            int(v) for v in coords.split(',')
        )

    def __repr__(self) -> str:
        return f"Point({self.x}, {self.y}, {self.z})"

    def distance_to(self, other_point: 'Point') -> float: 
        return sqrt(
            (self.x - other_point.x) ** 2 + 
            (self.y - other_point.y) ** 2 + 
            (self.z - other_point.z) ** 2
        )


def nearest_neighbors(points: List[Point]) -> Dict[Point, Point]:

    nn = defaultdict(lambda: (None, float('inf')))

    for i, point in enumerate(points):
        for j, other_point in enumerate(points):
            if i == j:
                continue
            d = point.distance_to(other_point)
            if d < nn[point][1]:
                nn[point] = (other_point, d)

    return nn    


def distance_matrix(points: List[Point]) -> List[List[int]]:

    dmat = []
    for p in points:
        dmat.append([0 for p in points])

    for i, point in enumerate(points):
        for j, other_point in enumerate(points):
            if i == j:
                continue
            d = point.distance_to(other_point)
            dmat[i][j] = d 

    return dmat  


def parse_points(points: List[str]) -> List[Point]:
    return [Point(line) for line in points]


def build_circuits(points: List[Point], n_connections: int = 1000) -> List[List[Point]]:
    
    dmat = distance_matrix(points)

    flat_dmat = []
    for i, row in enumerate(dmat[:-1]):
        for j, col in enumerate(row[i+1:]):
            flat_dmat.append((points[i], points[j + i + 1], col))

    flat_dmat = sorted(flat_dmat, key=lambda x: x[2])

    circuits = [[flat_dmat[0][0], flat_dmat[0][1]]]

    connections = 1

    for n in flat_dmat[1:]:
        p1, p2, d = n
        
        circuits_added_to = []
        already_in_a_circuit = False
        for i, circuit in enumerate(circuits):
            if p1 in circuit and p2 in circuit:
                connections += 1
                already_in_a_circuit = True
                break
            elif p1 in circuit:
                connections += 1
                circuit.append(p2)
                circuits_added_to.append(i)
            elif p2 in circuit:
                connections += 1
                circuit.append(p1)
                circuits_added_to.append(i)

        if already_in_a_circuit:
            continue

        if len(circuits_added_to) == 0:
            connections += 1
            circuits.append([p1, p2])
        elif len(circuits_added_to) > 1:
            connections -= 1
            new_circuits = [list(set(
                circuits[circuits_added_to[0]] + circuits[circuits_added_to[1]]
            ))]
            for i, c in enumerate(circuits):
                if i in circuits_added_to:
                    continue
                new_circuits.append(c)
            circuits = new_circuits
        
        if connections >= n_connections:
            break
    
    return circuits


def build_circuit(points: List[Point]) -> Tuple[Point, Point]:
    
    dmat = distance_matrix(points)

    flat_dmat = []
    for i, row in enumerate(dmat[:-1]):
        for j, col in enumerate(row[i+1:]):
            flat_dmat.append((points[i], points[j + i + 1], col))

    flat_dmat = sorted(flat_dmat, key=lambda x: x[2])

    circuits = [[flat_dmat[0][0], flat_dmat[0][1]]]
    for p in points:
        if p not in circuits[0]:
            circuits.append([p])

    for n in flat_dmat[1:]:
        p1, p2, d = n
        
        circuits_added_to = []
        already_in_a_circuit = False
        for i, circuit in enumerate(circuits):
            if p1 in circuit and p2 in circuit:
                already_in_a_circuit = True
                break
            elif p1 in circuit:
                circuit.append(p2)
                circuits_added_to.append(i)
            elif p2 in circuit:
                circuit.append(p1)
                circuits_added_to.append(i)

        if already_in_a_circuit:
            continue

        if len(circuits) == 2:
            # We're about to connect the last two circuits into one big circuit
            return p1, p2

        if len(circuits_added_to) == 0:
            circuits.append([p1, p2])
        elif len(circuits_added_to) > 1:
            new_circuits = [list(set(
                circuits[circuits_added_to[0]] + circuits[circuits_added_to[1]]
            ))]
            for i, c in enumerate(circuits):
                if i in circuits_added_to:
                    continue
                new_circuits.append(c)
            circuits = new_circuits
        
    raise Exception("Shouldn't get here.")
        

def part1(puzzle_input: str, n_connections: int=1000) -> int:
    points = parse_points(puzzle_input)
    circuits = build_circuits(points, n_connections)
    circuits = sorted(circuits, key=lambda x: len(x), reverse=True)

    boxes_per_circuit = [len(c) for c in circuits]

    return boxes_per_circuit[0] * boxes_per_circuit[1] * boxes_per_circuit[2]


def part2(puzzle_input: str) -> int:
    points = parse_points(puzzle_input)
    p1, p2 = build_circuit(points)
    return p1.x * p2.x


if __name__ == '__main__':
    ### THE TESTS
    test_input = dedent('''\
        162,817,812
        57,618,57
        906,360,560
        592,479,940
        352,342,300
        466,668,158
        542,29,236
        431,825,988
        739,650,466
        52,470,668
        216,146,977
        819,987,18
        117,168,530
        805,96,715
        346,949,466
        970,615,88
        941,993,340
        862,61,35
        984,92,344
        425,690,689
    ''').strip().split('\n')

    assert part1(test_input, 10) == 40
    assert part2(test_input) == 25272

    ### THE REAL THING
    puzzle_input = helper.read_input_lines()
    print(f'Part 1: {part1(puzzle_input)}')
    print(f'Part 2: {part2(puzzle_input)}')
