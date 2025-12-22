from typing import Any, List, Tuple
from dataclasses import dataclass
from itertools import combinations, combinations_with_replacement
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


def add_joltages(joltages: List[int], button: Tuple[int]) -> List[int]:
    for i in button:
        joltages[i] = joltages[i] + 1
    return joltages


def increment_joltages(machine: Machine) -> int:
    # This works technically but is way too slow for the real input
    # See `increment_joltages_better` for a more efficient solution

    min_presses = min(machine.joltages)
    max_presses = sum(machine.joltages) + 1

    for presses in range(min_presses, max_presses):
        for button_subset in combinations_with_replacement(machine.buttons, presses):
            joltages = [0 for _ in machine.joltages]
            for button in button_subset:
                joltages = add_joltages(joltages, button)
            if joltages == machine.joltages:
                return presses
    raise Exception("Shouldn't get here")


def lists_are_equal(l1: List[Any], l2: List[Any]):
    return len(l1) == len(l2) and all(j == t for j, t in zip(l1, l2))


def indices_of_smallest_gap(joltages: List[int], target_joltages: List[int]) -> List[int]:
    indices = []
    smallest_gap = 1e6
    for i in range(len(joltages)):
        joltage = joltages[i]
        target_joltage = target_joltages[i]
        difference = target_joltage - joltage
        if difference > 0 and difference < smallest_gap:
            smallest_gap = difference
            indices = [i]
        elif difference == smallest_gap:
            indices.append(i)
    
    return smallest_gap, indices


def find_buttons_to_press(buttons: List[Tuple[int]], indices: List[int]):
    buttons_to_press = []
    for i in indices:
        for b in buttons:
            if i in b:
                buttons_to_press.append(b)
    return sorted(list(set(buttons_to_press)), key=lambda x: len(x), reverse=True)


def increase_joltages(joltages: List[int], button: Tuple[int], number_of_presses: int) -> Tuple[int]:
    new_joltages = []
    for i, j in enumerate(joltages):
        if i in button:
            new_joltages.append(j + number_of_presses)
        else:
            new_joltages.append(j)
    return new_joltages


def find_remaining_buttons(machine: Machine, buttons: List[Tuple[int]], joltages: List[int]) -> List[Tuple[int]]:
    difference = [t - j for t, j in zip(machine.joltages, joltages)]
    remaining_buttons = []
    for button in buttons:
        if all(difference[b] > 0 for b in button):
            remaining_buttons.append(button)
    return remaining_buttons


def joltage_increment(machine: Machine, joltages: List[int], buttons: List[Tuple[int]], n_presses: int) -> int:

    if lists_are_equal(machine.joltages, joltages):
        return n_presses    
    
    number_of_presses, indices = indices_of_smallest_gap(joltages, machine.joltages)
    buttons_to_press = find_buttons_to_press(buttons, indices)

    if len(buttons_to_press) == 0:
        return -1

    for button in buttons_to_press:
        candidate_joltages = increase_joltages(joltages, button, number_of_presses)
        candidate_presses = n_presses + number_of_presses
        remaining_buttons = find_remaining_buttons(machine, buttons, candidate_joltages)
        total_button_presses = joltage_increment(machine, candidate_joltages, remaining_buttons, candidate_presses)
        if total_button_presses > 0:
            break
    
    return total_button_presses


def increment_joltages_better(machine: Machine) -> int:

    joltages = [0 for _ in machine.joltages]
    n_presses = joltage_increment(machine, joltages, machine.buttons, 0)
    return n_presses


def part1(puzzle_input: List[str]) -> int:
    machines = parse_machines(puzzle_input)

    path_sum = 0

    for machine in machines:
        shortest_path = push_buttons_better(machine)
        path_sum += shortest_path
    return path_sum


def part2(puzzle_input: List[str]) -> int:

    machines = parse_machines(puzzle_input)

    path_sum = 0

    for machine in machines:
        shortest_path = increment_joltages_better(machine)
        path_sum += shortest_path

    return path_sum


if __name__ == '__main__':
    ### THE TESTS
    test_input = dedent("""\
        [.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
        [...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
        [.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}    
    """).strip().split('\n')

    assert part1(test_input) == 7
    assert part2(test_input) == 33

    print('Tests passed!')

    ### THE REAL THING
    puzzle_input = helper.read_input_lines()
    print(f'Part 1: {part1(puzzle_input)}')
    print(f'Part 2: {part2(puzzle_input)}')
