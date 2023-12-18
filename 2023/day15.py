from typing import List, Tuple
from dataclasses import dataclass
import helper


@dataclass
class Lens:
    label: str
    focal_length: int


def focusing_power(box_number: int, slot_number: int, focal_length: int) -> int:
    return (1 + box_number) * (1 + slot_number) * focal_length


def hasher(the_string: str) -> int:
    hash = 0

    for char in the_string:
        hash += ord(char)
        hash *= 17
        hash %= 256

    return hash


def part1(input: str) -> int:
    lines = input.splitlines()
    total = 0
    for line in lines:
        commands = line.split(',')
        for command in commands:
            total += hasher(command)
    return total


def part2(input: str) -> int:
    lines = input.splitlines()
    commands = []
    for line in lines:
        commands.extend(line.split(','))
    
    boxes = {n: [] for n in range(256)}

    for command in commands:
        cmd_parts = command.split('=')
        label = cmd_parts[0].replace('-', '')
        if len(cmd_parts) == 2:
            focal_length = int(cmd_parts[1])
        else:
            focal_length = None
        box_number = hasher(label)

        if focal_length is None:
            new_lenses = []
            for lens in boxes[box_number]:
                if lens.label != label:
                    new_lenses.append(lens)
        else:
            new_lenses = []
            lens_replaced = False
            for lens in boxes[box_number]:
                if lens.label == label:
                    new_lenses.append(Lens(label, focal_length))
                    lens_replaced = True
                else:
                    new_lenses.append(lens)
            if not lens_replaced:
                new_lenses.append(Lens(label, focal_length))
        boxes[box_number] = new_lenses
    
    total_power = 0
    for box_number in boxes:
        for i, lens in enumerate(boxes[box_number]):
            total_power += focusing_power(box_number, i, lens.focal_length)
    
    return total_power


if __name__ == '__main__':
    ### THE TESTS
    assert hasher('HASH') == 52

    test_input = '''rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7'''
    assert part1(test_input) == 1320
    assert hasher('rn') == 0
    assert hasher('cm') == 0
    assert part2(test_input) == 145


    ### THE REAL THING
    puzzle_input = helper.read_input()
    print(f'Part 1: {part1(puzzle_input)}')
    print(f'Part 2: {part2(puzzle_input)}')
