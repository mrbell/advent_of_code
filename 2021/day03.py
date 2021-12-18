from typing import List, Callable
from helper import read_input_lines


def get_value_counts(report: List[str]) -> List[List[int]]:
    '''
    Given a list of binary numbers encoded as strings, each with equal number of digits, 
    return a count of occurrences of each value in each of the digits.
    '''
    digit_count = len(report[0])

    # For each place in the provided binary numbers, this will store counts of each value
    value_counts = [[0, 0] for _ in range(digit_count)]
    
    for i in range(digit_count):
        for report_line in report:
            value_counts[i][int(report_line[i])] += 1
    
    return value_counts


def bin2dec(binary_num: str) -> int:
    '''
    Convert a binary number to decimal e.g. bin2dec("101") -> 5
    '''
    dec_num = 0

    for i, v in enumerate(binary_num[::-1]):
        dec_num += int(v) * 2 ** i
    
    return dec_num


def calculate_rate(report: List[str], rate_type: str='gamma') -> int:

    eval_func = max if rate_type == 'gamma' else min
    
    value_counts = get_value_counts(report)

    the_rate = ['0' for _ in range(len(value_counts))]

    for i, counts in enumerate(value_counts):
        the_value = counts.index(eval_func(counts))
        the_rate[i] = str(the_value)

    return bin2dec(the_rate)


def get_power_consumption(report):
    return calculate_rate(report, 'gamma') * calculate_rate(report, 'epsilon')


def bit_criteria(digit_counts: List[str], default_value: str='1', eval_func: Callable=max) -> str:
    if digit_counts[0] == digit_counts[1]:
        the_value = default_value
    else:
        the_value = str(digit_counts.index(eval_func(digit_counts)))
    return the_value


def report_filter(report: List[str], criteria: Callable) -> str:
    digit_count = len(report[0])

    filtered_report = report.copy()

    for i in range(digit_count):
        value_counts = get_value_counts(filtered_report)
        this_digit_counts = value_counts[i]
        the_value = criteria(this_digit_counts)
        new_filtered_report = []
        for report_line in filtered_report:
            if report_line[i] == the_value:
                new_filtered_report.append(report_line)
        if len(new_filtered_report) == 1:
            break
        filtered_report = new_filtered_report.copy()

    return new_filtered_report[0]


def get_oxygen_generator_rating(report: List[str]) -> int:
    return bin2dec(report_filter(report, lambda x: bit_criteria(x)))


def get_co2_scrubber_rating(report: List[str]) -> int:
    return bin2dec(report_filter(report, lambda x: bit_criteria(x, '0', min)))


def get_life_support_rating(report: List[str]) -> int:
    return get_oxygen_generator_rating(report) * get_co2_scrubber_rating(report)


if __name__ == '__main__':
    ##### TESTS
    assert bin2dec('101') == 5
    assert bin2dec('10110') == 22

    test_report = '''00100
    11110
    10110
    10111
    10101
    01111
    00111
    11100
    10000
    11001
    00010
    01010'''.split('\n')

    assert calculate_rate(test_report, 'gamma') == 22
    assert calculate_rate(test_report, 'epsilon') == 9

    print(get_oxygen_generator_rating(test_report))
    print(get_co2_scrubber_rating(test_report))
    assert get_oxygen_generator_rating(test_report) == 23
    assert get_co2_scrubber_rating(test_report) == 10

    ##### THE REAL THING
    report = read_input_lines(3)

    power_consumption = get_power_consumption(report)
    print(f'Part 1: {power_consumption}')
    life_support_rating = get_life_support_rating(report)
    print(f'Part 2: {life_support_rating}')
