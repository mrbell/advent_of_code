from typing import List, Tuple
import helper


class Scratchcard(object):
    def __init__(self, s: str):
        self.id = int(s.split(': ')[0].split()[1])
        temp = s.split(': ')[1].strip().split(' | ')
        self.winning_numbers = [int(x) for x in temp[0].strip().split()]
        self.your_numbers = [int(x) for x in temp[1].strip().split()]
        self.presumed_value = int(2 ** (
            sum(1 for x in self.your_numbers if x in self.winning_numbers) - 1
        ))


def part1(puzzle_input: str) -> int:
    cards = [Scratchcard(x) for x in puzzle_input]
    return sum(x.presumed_value for x in cards)


if __name__ == '__main__':
    ### THE TESTS
    test_input = '''Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11'''.split('\n')
    
    assert part1(test_input) == 13

    ### THE REAL THING
    puzzle_input = helper.read_input_lines()
    print(f'Part 1: {part1(puzzle_input)}')
    print(f'Part 2: {""}')
