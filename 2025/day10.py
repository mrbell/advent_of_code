from typing import List, Tuple
from dataclasses import dataclass
from itertools import combinations
import helper
from textwrap import dedent


@dataclass
class Machine:
    light_diagram: List[bool]
    buttons: List[Tuple[int]]
    joltages: List[int]

    @property
    def light_diagram_binary(self) -> int:
        i = '0b' + ''.join('1' if v else '0' for v in self.light_diagram)
        return int(i, 2)

    @property
    def buttons_binary(self) -> List[int]:
        bb = []
        for button in self.buttons:
            i = '0b' + ''.join('1' if j in button else '0' for j, v in enumerate(self.light_diagram))
            bb.append(int(i, 2))
        return bb


def parse_machine(spec: str) -> Machine:
    temp1, temp2 = spec.split('] ')
    temp1 = temp1.replace('[', '')
    light_diagram = tuple(False if v == '.' else True for v in temp1)

    temp2, temp3 = temp2.split(' {')
    temp3 = temp3.replace('}', '')
    joltages = [int(v) for v in temp3.split(',')]

    parts = temp2.split(') (')
    buttons = []
    for part in parts:
        part = part.replace('(', '').replace(')', '')
        buttons.append(tuple(int(v) for v in part.split(',')))
    
    return Machine(light_diagram, buttons, joltages)


def toggle_lights(lights: Tuple[bool], button: Tuple[int]) -> Tuple[bool]:
    return tuple(not l if j in button else l for j, l in enumerate(lights))


def press_buttons(light_history: List[Tuple[bool]], button_history: List[Tuple[int]], machine: Machine) -> List[Tuple[bool]]:
    
    current_lights = light_history[-1] 

    if current_lights == machine.light_diagram:
        return light_history
    
    shortest_path = None
    shortest_path_length = 1e6
    
    for i, light in enumerate(current_lights):
        if light == machine.light_diagram[i]:
            # We don't need to toggle this light, it's already correct
            continue
        eligible_buttons = [button for button in machine.buttons if i in button and button not in button_history]
        for button in eligible_buttons:
            new_lights = toggle_lights(current_lights, button)
            if new_lights in light_history:
                continue
            this_path = press_buttons(light_history + [new_lights], button_history + [button], machine)
            if this_path is not None and len(this_path) < shortest_path_length:
                shortest_path_length = len(this_path)
                shortest_path = this_path
    
    return shortest_path


def parse_machines(specs: List[str]) -> List[Machine]:
    machines = []
    for spec in specs:
        machines.append(parse_machine(spec))
    return machines


def init_lights(machine: Machine) -> Tuple[bool]:
    return tuple(False for _ in machine.light_diagram)


def push_buttons_better(machine: Machine) -> int:

    i = 1
    buttons = machine.buttons_binary
    target = machine.light_diagram_binary

    while i < len(buttons):
        for button_subset in combinations(buttons, i):
            lights = 0
            for button in button_subset:
                lights ^= button
            if lights == target:
                return i
        i += 1

    raise Exception("Shouldn't get here")

def part1(puzzle_input: List[str]) -> int:
    machines = parse_machines(puzzle_input)

    path_sum = 0

    for machine in machines:
        shortest_path = push_buttons_better(machine)
        path_sum += shortest_path
    return path_sum


def part2(puzzle_input: List[str]) -> int:
    pass


if __name__ == '__main__':
    ### THE TESTS
    test_input = dedent("""\
        [.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
        [...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
        [.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}    
    """).strip().split('\n')

    assert part1(test_input) == 7

    print('Tests passed!')

    ### THE REAL THING
    puzzle_input = helper.read_input_lines()
    print(f'Part 1: {part1(puzzle_input)}')
    print(f'Part 2: {part2(puzzle_input)}')
