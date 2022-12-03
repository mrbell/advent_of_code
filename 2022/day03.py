from typing import List, Tuple, Optional
import helper


class Rucksack(object):
    def __init__(self, items: str):
        n = len(items)
        self.compartment1 = items[:n // 2]
        self.compartment2 = items[n // 2:]

    @property
    def items(self) -> str:
        return self.compartment1 + self.compartment2

    def shared_item(self) -> str:
        compartment_overlap = set(
            self.compartment1
        ).intersection(
            self.compartment2
        )
        assert len(compartment_overlap) == 1, "More than one shared item found!"
        return list(compartment_overlap)[0]


a_ord = ord('a')
A_ord = ord('A')


def item_priority(item: str) -> int:
    item_ord = ord(item)
    priority = 1 + item_ord - a_ord
    if priority < 0:
        priority = 27 + item_ord - A_ord
    return priority


def sum_shared_item_priority(rucksacks: List[Rucksack]) -> int:
    return sum([item_priority(r.shared_item()) for r in rucksacks])


def find_badges(rucksacks: List[Rucksack]) -> List[str]:
    group_badges = []
    for i in range(0, len(rucksacks), 3):
        group = rucksacks[i:i+3]
        group_badge = set(group[0].items).intersection(
            group[1].items
        ).intersection(
            group[2].items
        )
        group_badges.append(group_badge.pop())
    return group_badges


if __name__ == '__main__':
    ### THE TESTS
    test_inventories = '''vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw'''.split('\n')

    rucksacks = [Rucksack(inv) for inv in test_inventories]
    assert item_priority('p') == 16
    assert item_priority('L')
    assert sum_shared_item_priority(rucksacks) == 157

    group_badges = find_badges(rucksacks)
    assert sum(item_priority(b) for b in group_badges) == 70

    ### THE REAL THING
    puzzle_input = helper.read_input_lines()
    rucksacks = [Rucksack(inv) for inv in puzzle_input]
    sum_of_priorities = sum_shared_item_priority(rucksacks)
    print(f'Part 1: {sum_of_priorities}')
    
    group_badges = find_badges(rucksacks)
    badge_priority_sum = sum(item_priority(b) for b in group_badges)
    print(f'Part 2: {badge_priority_sum}')
