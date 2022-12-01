from typing import List, Tuple
import helper


def parse_elf_inventories(inventory: str) -> List[List[int]]:
    per_elf_inventory = inventory.strip('\n').split('\n\n')
    elf_inventories = [
        [int(item) for item in elf_inventory.split('\n')]
        for elf_inventory in per_elf_inventory
    ]
    return elf_inventories


def sum_calories(elf_inventories: List[List[int]]) -> List[int]:
    return [sum(ei) for ei in elf_inventories]


def get_max_calories(elf_calorie_totals: List[int]) -> Tuple[int, int]:
    return max([(i, s) for i, s in enumerate(elf_calorie_totals, 1)], key=lambda x: x[1])


if __name__ == '__main__':
    ### THE TESTS
    test_calorie_inventory = '''1000
2000
3000

4000

5000
6000

7000
8000
9000

10000
'''
    elf_inventories = parse_elf_inventories(test_calorie_inventory)
    elf_calorie_totals = sum_calories(elf_inventories)
    elf_with_most, most_calories = get_max_calories(elf_calorie_totals)
    assert most_calories == 24000
    assert elf_with_most == 4


    ### THE REAL THING
    puzzle_input = helper.read_input()
    elf_inventories = parse_elf_inventories(puzzle_input)
    elf_calorie_totals = sum_calories(elf_inventories)
    elf_with_most, most_calories = get_max_calories(elf_calorie_totals)
    print(f'Part 1: {most_calories} from elf # {elf_with_most}')

    sorted_calorie_totals = sorted(elf_calorie_totals, reverse=True)
    print(f'Part 2: {sum(sorted_calorie_totals[:3])}')
