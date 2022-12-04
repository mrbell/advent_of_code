from typing import List, Tuple
import helper


class Assignment(object):
    def __init__(self, assign_def: str):
        elves = assign_def.split(',')
        self.elves = [
            tuple(int(v) for v in elf.split('-'))
            for elf in elves
        ]
    
    def fully_contained(self) -> bool:
        return (
            (
                (self.elves[0][0] >= self.elves[1][0]) and 
                (self.elves[0][1] <= self.elves[1][1])
            ) or (
                (self.elves[1][0] >= self.elves[0][0]) and 
                (self.elves[1][1] <= self.elves[0][1])
            )
        )
    
    def no_overlap(self) -> bool:
        return (
            (self.elves[0][0] > self.elves[1][1]) or
            (self.elves[1][0] > self.elves[0][1])
        )


if __name__ == '__main__':
    ### THE TESTS
    test_assignments = '''2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8'''.split('\n')

    assignments = [Assignment(ta) for ta in test_assignments]
    assert sum(a.fully_contained() for a in assignments) == 2
    n_pairs = len(assignments)
    n_no_overlap = sum(a.no_overlap() for a in assignments)
    assert n_pairs - n_no_overlap == 4

    ### THE REAL THING
    puzzle_input = helper.read_input_lines()
    assignments = [Assignment(i) for i in puzzle_input]
    n_contained = sum(a.fully_contained() for a in assignments)
    print(f'Part 1: {n_contained}')
    n_pairs = len(assignments)
    n_no_overlap = sum(a.no_overlap() for a in assignments)
    print(f'Part 2: {n_pairs - n_no_overlap}')
