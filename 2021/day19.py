from __future__ import annotations
from dataclasses import dataclass
from typing import List, Tuple
import helper


SCAN_DIST = 1000
OVERLAP_MIN = 12


def make_rotations():    
    rotations = []
    for xi in range(3):
        for xval in [-1, 1]:
            for yi in range(3):
                if xi == yi:
                    continue
                for yval in [-1, 1]:
                    xvec = [0] * 3
                    yvec = [0] * 3
                    xvec[xi] = xval
                    yvec[yi] = yval
                    rotations.append(
                        Rotation(
                            Vector(*xvec),
                            Vector(*yvec)
                        )
                    )

    return rotations


@dataclass
class Rotation:
    x: Vector 
    y: Vector
    
    def __post_init__(self):
        self.z = self.x.cross(self.y)

    def __matmul__(self, vec: Vector):
        return Vector(
            self.x.dot(vec),
            self.y.dot(vec),
            self.z.dot(vec)
        )


@dataclass
class ScannerMap:
    id: int
    beacons: List[Vector]
        
    def from_str(map_def: str) ->  ScannerMap:
        map_def_lines = map_def.split('\n')
        id = int(
            map_def_lines[0].replace('---', '').replace('scanner', '').strip()
        )
        beacons = []
        for row in map_def_lines[1:]:
            beacons.append(
                Vector(*[int(v) for v in row.split(',')])
            )
        return ScannerMap(id, beacons)

    def rotate(self, rotation: Rotation) -> ScannerMap:
        rotated_beacons = [
            rotation @ beacon
            for beacon in self.beacons
        ]    
        return ScannerMap(self.id, rotated_beacons) 
    
    def translate(self, vec: Vector) -> ScannerMap:
        translated_beacons = [
            beacon + vec
            for beacon in self.beacons
        ]
        return ScannerMap(self.id, translated_beacons)
    
    def append(self, other_map: ScannerMap):
        beacons_to_add = list(
            set(self.beacons).difference(set(other_map.beacons))
        )
        self.beacons.extend(beacons_to_add)


@dataclass
class Vector:
    x: int
    y: int
    z: int

    def dot(self, vec: Vector) -> int:
        return self.x * vec.x + self.y * vec.y + self.z * vec.z
    
    def cross(self, vec: Vector) -> Vector:
        return Vector(
            self.y * vec.z - self.z * vec.y,
            self.z * vec.x - self.x * vec.z,
            self.x * vec.y - self.y * vec.x
        )

    def __add__(self, vec: Vector) -> Vector:
        return Vector(self.x + vec.x, self.y + vec.y, self.z + vec.z)

    def __eq__(self, vec: Vector) -> Vector:
        return self.x == vec.x and self.y == vec.y and self.z == vec.z
    
    def __repr__(self):
        return f'Vector(x={self.x}, y={self.y}, z={self.z})'

    def __hash__(self):
        return hash(repr(self))


def register_maps(scan_maps: List[str]) -> ScannerMap:
    rotations = make_rotations()

    the_map = ScannerMap.from_str(scan_maps[0])

    other_scan_maps = [ScannerMap.from_str(sm) for sm in scan_maps[1:]]

    while len(other_scan_maps) > 0:
        the_map_vals = {
            'x': set([
                beacon.x for beacon in the_map.beacons
            ]),
            'y': set([
                beacon.y for beacon in the_map.beacons
            ]),
            'z': set([
                beacon.z for beacon in the_map.beacons
            ])
        }
        for osm in other_scan_maps:
            added = False
            for rotation in rotations:
                rotated_map = osm.rotate(rotation)
                shift_vector = Vector(0, 0, 0)
                aint_it = False
                for axs in ['x', 'y', 'z']:
                    max_overlap = 0
                    max_shift = None
                    for to_shift in range(-SCAN_DIST, SCAN_DIST + 1):
                        setattr(shift_vector, axs, to_shift)
                        translated_map = rotated_map.translate(shift_vector)
                        translated_map_vals = set(
                            [getattr(beacon, axs) for beacon in translated_map.beacons]
                        )
                        this_overlap = translated_map_vals.intersection(the_map_vals[axs])
                        if len(this_overlap) > max_overlap:
                            max_overlap = len(this_overlap)
                            max_shift = to_shift
                    if max_overlap < OVERLAP_MIN:
                        aint_it = True
                        break
                    else:
                        setattr(shift_vector, axs, max_shift)
                
                if aint_it:
                    continue
                else:
                    map_to_add = osm.rotate(rotation).translate(shift_vector)
                    the_map.append(map_to_add)
                    added = True
                    break
            if added:
                break
        other_scan_maps.remove(osm)
    
    return the_map


if __name__ == '__main__':

    r = Rotation(Vector(-1, 0, 0), Vector(0, -1, 0))
    v = Vector(-1, -1, 1)
    new_v = r @ v


    test_scan_map = ScannerMap.from_str('''--- scanner 0 ---
-1,-1,1
-2,-2,2
-3,-3,3
-2,-3,1
5,6,-4
8,0,7''')
    
    rotations = make_rotations()
    for r in rotations:
        temp = test_scan_map.rotate(r)

    ### THE TESTS
    test_reports = '''--- scanner 0 ---
404,-588,-901
528,-643,409
-838,591,734
390,-675,-793
-537,-823,-458
-485,-357,347
-345,-311,381
-661,-816,-575
-876,649,763
-618,-824,-621
553,345,-567
474,580,667
-447,-329,318
-584,868,-557
544,-627,-890
564,392,-477
455,729,728
-892,524,684
-689,845,-530
423,-701,434
7,-33,-71
630,319,-379
443,580,662
-789,900,-551
459,-707,401

--- scanner 1 ---
686,422,578
605,423,415
515,917,-361
-336,658,858
95,138,22
-476,619,847
-340,-569,-846
567,-361,727
-460,603,-452
669,-402,600
729,430,532
-500,-761,534
-322,571,750
-466,-666,-811
-429,-592,574
-355,545,-477
703,-491,-529
-328,-685,520
413,935,-424
-391,539,-444
586,-435,557
-364,-763,-893
807,-499,-711
755,-354,-619
553,889,-390

--- scanner 2 ---
649,640,665
682,-795,504
-784,533,-524
-644,584,-595
-588,-843,648
-30,6,44
-674,560,763
500,723,-460
609,671,-379
-555,-800,653
-675,-892,-343
697,-426,-610
578,704,681
493,664,-388
-671,-858,530
-667,343,800
571,-461,-707
-138,-166,112
-889,563,-600
646,-828,498
640,759,510
-630,509,768
-681,-892,-333
673,-379,-804
-742,-814,-386
577,-820,562

--- scanner 3 ---
-589,542,597
605,-692,669
-500,565,-823
-660,373,557
-458,-679,-417
-488,449,543
-626,468,-788
338,-750,-386
528,-832,-391
562,-778,733
-938,-730,414
543,643,-506
-524,371,-870
407,773,750
-104,29,83
378,-903,-323
-778,-728,485
426,699,580
-438,-605,-362
-469,-447,-387
509,732,623
647,635,-688
-868,-804,481
614,-800,639
595,780,-596

--- scanner 4 ---
727,592,562
-293,-554,779
441,611,-461
-714,465,-776
-743,427,-804
-660,-479,-426
832,-632,460
927,-485,-438
408,393,-506
466,436,-512
110,16,151
-258,-428,682
-393,719,612
-211,-452,876
808,-476,-593
-575,615,604
-485,667,467
-680,325,-822
-627,-443,-432
872,-547,-609
833,512,582
807,604,487
839,-516,451
891,-625,532
-652,-548,-490
30,-46,-14'''.split('\n\n')
    test_full_map = register_maps(test_reports)
    assert len(test_full_map.beacons) == 79

    ### THE REAL THING
    puzzle_input = helper.read_input()
    scan_maps = puzzle_input.split('\n\n')
    full_map = register_maps(scan_maps)
    print(f'Part 1: {len(full_map.beacons)}')
    print(f'Part 2: {""}')
