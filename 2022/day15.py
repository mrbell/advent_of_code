from typing import List, Tuple
import time
import helper


def distance(pos1: Tuple[int, int], pos2: Tuple[int, int]) -> int:
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])


class Sensor(object):
    def __init__(self, sensor_def: str):
        sensor_part, beacon_part = sensor_def.split(':')
        x_part, y_part = sensor_part.split(', y=')
        self.pos = (int(x_part.split('x=')[1]), int(y_part))

        x_part, y_part = beacon_part.split(', y=')
        self.beacon = (int(x_part.split('x=')[1]), int(y_part))       

        self.distance = distance(self.pos, self.beacon)

    def __repr__(self):
        return (
            f'Sensor at x={self.pos[0]}, y={self.pos[1]}:'
            f' closest beacon is at x={self.beacon[0]}, y={self.beacon[1]}'
        )
    
    def no_beacon(self, test_point: Tuple[int, int]) -> bool:
        return distance(self.pos, test_point) <= self.distance and test_point != self.beacon

    def xrange_at_y(self, y: int) -> Tuple[int, int]:
        y_diff = abs(self.pos[1] - y)
        x_diff = self.distance - y_diff
        x_min, x_max = self.pos[0] - x_diff, self.pos[0] + x_diff
        return x_min, x_max


def positions_without_beacon(
    sensors: List['Sensor'],
    test_row: int
) -> int:
    
    these_sensors = [
        sensor for sensor in sensors
        if sensor.pos[1] - sensor.distance <= test_row <= sensor.pos[1] + sensor.distance
    ]

    points_with_no_beacon = 0  #  []
    min_x = min([sensor.pos[0] - sensor.distance for sensor in these_sensors])
    max_x = max([sensor.pos[0] + sensor.distance for sensor in these_sensors])

    for x in range(min_x, max_x + 1):
        for sensor in these_sensors:
            if sensor.no_beacon((x, test_row)):
                points_with_no_beacon += 1  # .append((x, test_row))
                break

    return points_with_no_beacon 


def positions_without_beacon_faster(
    sensors: List['Sensor'],
    test_row: int
) -> int:
    
    these_sensors = [
        sensor for sensor in sensors
        if sensor.pos[1] - sensor.distance <= test_row <= sensor.pos[1] + sensor.distance
    ]

    beacons_in_row = set([sensor.beacon for sensor in these_sensors if sensor.beacon[1] == test_row])

    points_with_no_beacon = 0

    x_ranges = sorted([
        sensor.xrange_at_y(test_row) for sensor in these_sensors
    ], key=lambda x: x[0])

    current_x = -1000000
    for (x_left, x_right) in x_ranges:
        if x_right < current_x:
            continue
        if x_left < current_x:
            x_min = current_x
        else:
            x_min = x_left
        
        points_with_no_beacon += (x_right - x_min + 1)
        
        points_with_no_beacon -= sum(
            [
                1 for b in beacons_in_row 
                if x_min <= b[0] <= x_right
            ] 
        )
        current_x = (x_right + 1)

    return points_with_no_beacon 


def find_beacon(sensors: List['Sensor'], max_point: Tuple[int, int]) -> Tuple[int, int]:
    min_point = (0, 0)

    for test_row in range(min_point[1], max_point[1] + 1):
        if (test_row + 1) % 40_000 == 0:
            print('.', end='')

        these_sensors = [
            sensor for sensor in sensors
            if sensor.pos[1] - sensor.distance <= test_row <= sensor.pos[1] + sensor.distance
        ]

        for test_col in range(min_point[0], max_point[0] + 1):
            if all([
                not sensor.no_beacon((test_col, test_row))
                and (test_col, test_row) != sensor.beacon 
                for sensor in these_sensors
            ]):
                return (test_col, test_row)
    
    raise ValueError('No beacon found')


def find_beacon_faster(sensors: List['Sensor'], max_point: Tuple[int, int]) -> Tuple[int, int]:
    min_point = (0, 0)

    for test_row in range(min_point[1], max_point[1] + 1):

        these_sensors = [
            sensor for sensor in sensors
            if sensor.pos[1] - sensor.distance <= test_row <= sensor.pos[1] + sensor.distance
        ]

        x_ranges = sorted([
            sensor.xrange_at_y(test_row) for sensor in these_sensors
        ], key=lambda x: x[0])

        current_x = min_point[0]

        for x_left, x_right in x_ranges:
            if x_right < current_x:
                continue
            elif x_left > current_x:
                return (current_x, test_row)
            elif x_right >= max_point[0]:
                break
            elif x_left <= current_x:
                current_x = x_right + 1
            else:
                raise ValueError("Something went wrong")

    raise ValueError('No beacon found')


def tuning_frequency(point: Tuple[int, int]) -> int:
    return point[0] * 4_000_000 + point[1]


if __name__ == '__main__':

    # TODO: Idea for improvement... at each row, find the sensors that are in y range
    # then sort the sensors by the x position they cover for the test row. Then
    # as you iterate, you can skip columns covered by each sensor in one go.


    ### THE TESTS
    test_input = '''Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3'''.split('\n')

    test_sensors = [Sensor(sensor_def) for sensor_def in test_input]
    test_sensor = test_sensors[6]
    assert test_sensor.distance == 9
    assert not test_sensor.no_beacon((2, 10))
    assert not test_sensor.no_beacon((2, 11))
    assert test_sensor.no_beacon((2, 9))
    assert test_sensor.no_beacon((8, -2))
    assert not test_sensor.no_beacon((8, -3))
    assert test_sensor.no_beacon((8, 16))
    assert not test_sensor.no_beacon((8, 17))
    assert test_sensor.no_beacon((-1, 7))
    assert not test_sensor.no_beacon((-2, 7))
    assert test_sensor.no_beacon((17, 7))
    assert not test_sensor.no_beacon((18, 7))
    assert test_sensor.no_beacon((3, 3))
    assert not test_sensor.no_beacon((3, 2))
    assert not test_sensor.no_beacon((2, 3))
    assert test_sensor.no_beacon(test_sensor.pos)
    assert test_sensor.xrange_at_y(10) == (2, 14)

    test = positions_without_beacon(test_sensors, 10) 
    assert test == 26
    test = positions_without_beacon_faster(test_sensors, 10)
    assert test == 26

    assert all(
        [not sensor.no_beacon((14, 11)) for sensor in test_sensors]
    )
    test = find_beacon(test_sensors, (20, 20))
    assert test == (14, 11)
    assert tuning_frequency(test) == 56_000_011
    test = find_beacon_faster(test_sensors, (20, 20))
    assert test == (14, 11)
    assert tuning_frequency(test) == 56_000_011

    ### THE REAL THING
    puzzle_input = helper.read_input_lines()
    sensors = [Sensor(sensor_def) for sensor_def in puzzle_input]
    t0 = time.time()
    print(f'Part 1: {positions_without_beacon_faster(sensors, 2_000_000)}')
    print(f'Elapsed: {time.time() - t0:.2f} seconds')
    beacon = find_beacon_faster(sensors, (4_000_000, 4_000_000))
    print(f'Part 2: {tuning_frequency(beacon)}')
