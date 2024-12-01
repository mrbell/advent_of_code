import helper


def parse_lists(lines):

    l1 = []
    l2 = []
    for line in lines:
        l1.append(int(line.split()[0]))
        l2.append(int(line.split()[1]))
    
    return l1, l2


def diff_lists(l1, l2):
    l1_sorted, l2_sorted = sorted(l1), sorted(l2)

    distances = [abs(a - b) for a, b in zip(l1_sorted, l2_sorted)]

    return sum(distances)


def similarity_score(l1, l2):
    score = 0
    for n in l1:
        multiplier = sum([1 for m in l2 if m == n])
        score += n * multiplier
    return score


if __name__ == '__main__':
    ### THE TESTS
    example_input = '''3   4
4   3
2   5
1   3
3   9
3   3'''.split('\n')

    l1, l2 = parse_lists(example_input)
    assert diff_lists(l1, l2) == 11
    assert similarity_score(l1, l2) == 31


    ### THE REAL THING
    puzzle_input = helper.read_input_lines()
    l1, l2 = parse_lists(puzzle_input)
    print(f'Part 1: {diff_lists(l1, l2)}')
    print(f'Part 2: {similarity_score(l1, l2)}')
