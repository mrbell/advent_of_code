from typing import List, Tuple
from time import time
import helper


operators = {'add': lambda x, y: x + y, 'mul': lambda x, y: x * y, 'concat': lambda x, y: int(str(x) + str(y))}
simple_operators = {'add': lambda x, y: x + y, 'mul': lambda x, y: x * y}


def possible_operations(n: int, full=False) -> List[str]:

    these_operators = operators if full else simple_operators

    if n == 1:
        return [[o] for o in list(these_operators.keys())]
    
    op_list = []
    for op in these_operators:
        sub_ops = possible_operations(n-1, full=full)

        for sub_op in sub_ops:
            op_list.append([op] + sub_op)
    
    return op_list


def parse_input(lines: List[str]) -> List[Tuple[int, List[int]]]:
    return [(int(line.split(':')[0]), list(map(int, line.split(':')[1].split()))) for line in lines]


def get_calibration(data: List[Tuple[int, List[int]]], full=False) -> int:
    result = 0

    for i, test in enumerate(data):
        test_val = test[0]
        test_input = test[1]

        n_ops = len(test_input) - 1

        for perm in possible_operations(n_ops, full):
            this_result = test_input[0]
            
            for i, inp in enumerate(test_input[:-1]):
                this_result = operators[perm[i]](this_result, test_input[i+1])

            if this_result == test_val:
                result += test_val
                break

    return result    

# (((A op1 B) op2 C) op3 D)

def part1(data: List[str]) -> int:
    tests = parse_input(data)
    t0 = time()
    result = get_calibration(tests, full=False)
    print(f'Part 1 took {time() - t0} seconds')
    return result


def part2(data: List[str]) -> int:
    tests = parse_input(data)
    t0 = time()
    result = get_calibration(tests, full=True)
    print(f'Part 2 took {time() - t0} seconds')
    return result


if __name__ == '__main__':
    ### THE TESTS
    example_input = '''190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20'''.split('\n')

    ops = possible_operations(2)
    assert len(ops) == 4, f"Expected 4, but got {len(ops)}"
    ops = possible_operations(3)
    assert len(ops) == 8, f"Expected 8, but got {len(ops)}"
    ops = possible_operations(2, full=True)
    assert len(ops) == 9, f"Expected 9, but got {len(ops)}"

    example = part1(example_input)
    assert example == 3749, f"Expected 3749, but got {example}"

    example2 = part2(example_input)
    assert example2 == 11387, f"Expected 11387, but got {example2}"

    ### THE REAL THING
    puzzle_input = helper.read_input_lines()
    print(f'Part 1: {part1(puzzle_input)}')
    print(f'Part 2: {part2(puzzle_input)}')
