from typing import List, Tuple
import helper


def parse_line(line: str, is_button=True) -> Tuple[int, int]:

    separator = '+' if is_button else '='

    coord_part = line.split(': ')[1]
    parts = coord_part.split(', ')
    for part in parts:
        if part.startswith('X'):
            x = int(part.replace(f'X{separator}', ''))
        elif part.startswith('Y'):
            y = int(part.replace(f'Y{separator}', ''))
    return x, y


def parse_machine_spec(spec: str) -> Tuple[Tuple[int, int], Tuple[int, int], Tuple[int, int]]:
    lines = spec.split('\n')
    for line in lines:
        if line.startswith('Button A:'):
            button_a = parse_line(line)
        elif line.startswith('Button B:'):
            button_b = parse_line(line)
        elif line.startswith('Prize:'):
            prize = parse_line(line, is_button=False)
    return button_a, button_b, prize


class ClawMachine(object):
    def __init__(self, button_a: Tuple[int, int], button_b: Tuple[int, int], prize: Tuple[int, int]):
        self.button_a = button_a
        self.button_b = button_b
        self.prize = prize

    def solve(self) -> Tuple[int, int]:
        a_x, a_y = self.button_a
        b_x, b_y = self.button_b
        p_x, p_y = self.prize

        n_b = (p_y * a_x - p_y * a_y) / (b_y * a_x - b_y * a_y)
        n_a = (p_x - n_b * b_x) / a_x

        if n_a.is_integer() and n_b.is_integer():
            return int(n_a), int(n_b)
        else:
            return None, None


def part1(input: str) -> int:
    machine_specs = input.split('\n\n')

    token_count = 0

    for machine_spec in machine_specs:
        button_a, button_b, prize = parse_machine_spec(machine_spec)
        machine = ClawMachine(button_a, button_b, prize)
        a, b = machine.solve()
        if a is not None:
            token_count += a + b

    return token_count


if __name__ == '__main__':
    ### THE TESTS
    example_input = '''Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279'''

    result = part1(example_input)
    assert result == 480, f'Expected 480 but got {result}'

    ### THE REAL THING
    puzzle_input = helper.read_input()
    print(f'Part 1: {part1(puzzle_input)}')
    print(f'Part 2: {""}')
