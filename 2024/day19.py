from typing import List, Tuple
import helper


def parse_input(input_string: str) -> Tuple[List[str], List[str]]:
    towels, arrangements = input_string.split('\n\n')
    return towels.split(', '), arrangements.split('\n')


def is_possible(towels: List[str], arrangement: str) -> bool:
    
    it_is_possible = False

    for towel in towels:
        if arrangement == towel:
            return True
        if arrangement.find(towel) == 0:
            if is_possible(towels, arrangement[len(towel):]):
                return True
    return it_is_possible


class ArrangementFinder(object):

    def __init__(self, towels: List[str]):
        self.arrangement_cache = {}
        self.towels = towels


    def get_possible_arrangements(self, arrangement: str) -> int:

        if arrangement in self.arrangement_cache:
            return self.arrangement_cache[arrangement]

        possible_arrangements = 0
        for towel in self.towels:
            if arrangement == towel:
                possible_arrangements += 1
            if arrangement.find(towel) == 0:
                possible_arrangements += self.get_possible_arrangements(arrangement[len(towel):])

        self.arrangement_cache[arrangement] = possible_arrangements

        return possible_arrangements


def count_possible(towels: List[str], arrangements: List[str]) -> int:
    # print(f'Towels: {towels}')
    arrangement_is_possible = [is_possible(towels, arrangement) for arrangement in arrangements]
    # for arrangement, arrangement_possible in zip(arrangements, arrangement_is_possible):
    #     print(f'{arrangement}: {arrangement_possible}')

    return sum(arrangement_is_possible)


def part1(puzzle_input: str) -> int:
    towels, arrangements = parse_input(puzzle_input)
    return count_possible(towels, arrangements)


def part2(puzzle_input: str) -> int:
    towels, arrangements = parse_input(puzzle_input)
    arrangement_finder = ArrangementFinder(towels)
    total_arrangements = 0
    for arrangement in arrangements:
        possible_arrangements = arrangement_finder.get_possible_arrangements(arrangement)
        print(f'{arrangement}: {possible_arrangements}')
        total_arrangements += possible_arrangements
    return total_arrangements


if __name__ == '__main__':
    ### THE TESTS
    example_input = '''r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb'''
    result = part1(example_input)
    helper.check(result, 6)
    result = part2(example_input)
    helper.check(result, 16)



    ### THE REAL THING
    puzzle_input = helper.read_input()
    print(f'Part 1: {part1(puzzle_input)}')
    print(f'Part 2: {part2(puzzle_input)}')
