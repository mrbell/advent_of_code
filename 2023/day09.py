from typing import List, Tuple, Callable
import helper


def parse_input(lines: List[str]) -> List[List[int]]:
    histories = []
    for line in lines:
        histories.append([int(x) for x in line.split()])
    return histories


def diff(history: List[int]) -> List[int]:
    return [v1 - v0 for v1, v0 in zip(history[1:], history[:-1])]


def next_number(hist: List[int], diffs: List[List[int]]) -> int:
    if len(diffs) == 1:
        return hist[-1]
    else:
        return hist[-1] + next_number(diffs[0], diffs[1:])


def previous_number(hist: List[int], diffs: List[List[int]]) -> int:
    if len(diffs) == 1:
        return hist[0]
    else:
        return hist[0] - previous_number(diffs[0], diffs[1:])


def get_diff_stack(history: List[int]) -> List[List[int]]:
    this_diff = diff(history)
    diffs = [this_diff]
    while not all(d == 0 for d in this_diff):
        this_diff = diff(this_diff)
        diffs.append(this_diff)
    return diffs


def predict_next_number(history: List[int]) -> int:
    diffs = get_diff_stack(history)
    return next_number(history, diffs)


def predict_previous_number(history: List[int]) -> int:
    diffs = get_diff_stack(history)
    return previous_number(history, diffs)


def predict_and_sum(puzzle_input: List[str], prediction: Callable=predict_next_number) -> int:
    histories = parse_input(puzzle_input)
    return sum([prediction(history) for history in histories])


def part1(puzzle_input: List[str]) -> int:
    return predict_and_sum(puzzle_input, predict_next_number)


def part2(puzzle_input: List[str]) -> int:
    return predict_and_sum(puzzle_input, predict_previous_number)


if __name__ == '__main__':
    ### THE TESTS
    test_input = '''0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45'''.splitlines()

    assert part1(test_input) == 114
    assert part2(test_input) == 2

    ### THE REAL THING
    puzzle_input = helper.read_input_lines()
    print(f'Part 1: {part1(puzzle_input)}')
    print(f'Part 2: {part2(puzzle_input)}')
