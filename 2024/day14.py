from typing import List, Tuple
from dataclasses import dataclass
import helper


@dataclass
class Robot():
    position: Tuple[int, int]
    velocity: Tuple[int, int]
    room_size: Tuple[int, int]

    def move(self, n_steps=1):
        for _ in range(n_steps):
            self.position = (self.position[0] + self.velocity[0], self.position[1] + self.velocity[1])
            self.position = (self.position[0] % self.room_size[0], self.position[1] % self.room_size[1])


def parse_input(lines: List[str], room_size=None) -> List[Robot]:
    if room_size is None:
        room_size = (101, 103)
    robots = []
    for line in lines:
        p, v = line.split(' v=')
        p = tuple(map(int, p[2:].split(',')))
        v = tuple(map(int, v.split(',')))
        robots.append(Robot(p, v, room_size))
    return robots


def safety_factor(robots: List[Robot]) -> int:
    room_size = robots[0].room_size
    x_mid, y_mid = room_size[0] // 2, room_size[1] // 2

    q1, q2, q3, q4 = 0, 0, 0, 0

    for robot in robots:
        x, y = robot.position
        if x < x_mid and y < y_mid:
            q1 += 1
        elif x > x_mid and y < y_mid:
            q2 += 1
        elif x < x_mid and y > y_mid:
            q3 += 1
        elif x > x_mid and y > y_mid:
            q4 += 1

    return q1 * q2 * q3 * q4


def part1(lines: List[str], room_size=None) -> int:
    robots = parse_input(lines, room_size)
    for robot in robots:
        robot.move(100)
    return safety_factor(robots)


def make_map(robots: List[Robot]) -> List[List[str]]:
    room_size = robots[0].room_size
    room = [['.' for _ in range(room_size[0])] for _ in range(room_size[1])]

    for robot in robots:
        x, y = robot.position
        room[y][x] = '1' if room[y][x] == '.' else str(int(room[y][x]) + 1)

    return room


def plot_robots(robots: List[Robot], n_steps=None):
    room = make_map(robots)

    for row in room:
        print(''.join(row))
    if n_steps:
        print(f"n_steps: {n_steps}")    


def stdv(robots: List[Robot]) -> Tuple[float, float]:
    x_positions = [robot.position[0] for robot in robots]
    y_positions = [robot.position[1] for robot in robots]
    x_mean = sum(x_positions) / len(x_positions)
    y_mean = sum(y_positions) / len(y_positions)
    x_stdv = (sum([(x - x_mean) ** 2 for x in x_positions]) / len(x_positions)) ** 0.5
    y_stdv = (sum([(y - y_mean) ** 2 for y in y_positions]) / len(y_positions)) ** 0.5
    return x_stdv, y_stdv


def is_xmas_tree(robots: List[Robot]) -> bool:
    xsd, ysd = stdv(robots)

    if xsd < 25 and ysd < 25:
        plot_robots(robots)
        print(xsd, ysd)
        return True
    return False


def part2(lines: List[str], room_size=None) -> int:
    robots = parse_input(lines, room_size)
    n_steps = 0
    while not is_xmas_tree(robots):
        for robot in robots:
            robot.move()
        n_steps += 1
    return n_steps


if __name__ == '__main__':
    ### THE TESTS
    example_input = '''p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3'''.split('\n')
    result = part1(example_input, (11, 7))
    assert result == 12, f"Expected 12, but got {result}"

    ### THE REAL THING
    puzzle_input = helper.read_input_lines()
    print(f'Part 1: {part1(puzzle_input)}')
    print(f'Part 2: {part2(puzzle_input)}')
