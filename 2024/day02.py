from typing import List, Tuple
import helper


def parse_reports(report: List[str]) -> List[List[int]]:
    return [parse_report(x) for x in report]


def parse_report(report: str) -> List[int]:
    return [int(x) for x in report.split()]    


def report_is_safe(report: List[int]) -> bool:
    previous_diff = None
    for item1, item2 in zip(report, report[1:]):
        diff = item2 - item1
        if (
            abs(diff) > 3 
            or diff == 0 
            or (previous_diff is not None and diff * previous_diff < 0)
        ):
            return False
        previous_diff = diff
    return True


def is_report_safe_with_problem_dampener(report: List[int]) -> bool:
    if report_is_safe(report):
        return True
    for i, _ in enumerate(report):
        test_report = report[:i] + report[i+1:]
        if report_is_safe(test_report):
            return True
    return False


def count_safe_reports(reports: List[List[int]], dampener=False) -> int:
    func = is_report_safe_with_problem_dampener if dampener else report_is_safe
    return sum(1 if func(x) else 0 for x in reports)


if __name__ == '__main__':
    ### THE TESTS
    example_input = '''7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9'''.split('\n')
    example = parse_reports(example_input)
    assert count_safe_reports(example) == 2
    assert count_safe_reports(example, True) == 4

    ### THE REAL THING
    puzzle_input = helper.read_input_lines()
    reports = parse_reports(puzzle_input)
    print(f'Part 1: {count_safe_reports(reports)}')
    print(f'Part 2: {count_safe_reports(reports, True)}')
