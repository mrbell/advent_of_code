from typing import List, Tuple, Dict
import helper

# Solve part 1 assuming part 2 asks to sort the updates
# Then if the sorted update is the same as the original, then we know the original was sorted already

# Store the rules in a dictionary, keyed on the first number and the value is a list of the second numbers
# To sort, create a recursive function that takes a list of numbers and the rules and finds the number that has all other numbers after it
# Then remove that number from the list and call the function again with the remaining list of numbers

def parse_input(input: str) -> Tuple[Dict[int, List[int]], List[int]]:
    rules = {}
    updates = []
    for line in input.split('\n'):
        if line == '':
            continue
        if '|' in line:
            a, b = line.split('|')
            a, b = int(a), int(b)
            if a not in rules:
                rules[a] = []
            if b not in rules:
                rules[b] = []
            rules[a].append(b)
        else:
            updates.append([int(x) for x in line.split(',')])
    return rules, updates


def sort_updates(rules: Dict[int, List[int]], updates: List[int]) -> List[int]:

    for u in updates:
        other_numbers_in_update = set([x for x in updates if x != u])
        if len(other_numbers_in_update) == 0:
            return updates
        numbers_after_this_number = set(rules[u])
        if other_numbers_in_update.issubset(numbers_after_this_number):
            return [u] + sort_updates(rules, [x for x in updates if x != u])
    return updates


def part1(input: str) -> int:
    rules, updates = parse_input(input)
    
    the_sum = 0

    for update in updates:
        if sort_updates(rules, update) == update:
            # get middle number
            n = update[len(update) // 2]
            the_sum += n    
    
    return the_sum


def part2(input: str) -> int:
    rules, updates = parse_input(input)

    the_sum = 0
    
    for update in updates:
        sorted_update = sort_updates(rules, update)
        if sorted_update != update:
            n = sorted_update[len(sorted_update) // 2]
            the_sum += n
    
    return the_sum


if __name__ == '__main__':
    ### THE TESTS
    example_input = '''47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47'''
    p1 = part1(example_input)
    assert p1 == 143, f'Expected 143 but got {p1}'
    p2 = part2(example_input)
    assert p2 == 123, f'Expected 123 but got {p2}'

    ### THE REAL THING
    puzzle_input = helper.read_input()
    print(f'Part 1: {part1(puzzle_input)}')
    print(f'Part 2: {part2(puzzle_input)}')  # 6232 is too low
