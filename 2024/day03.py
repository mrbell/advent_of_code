import helper


def index_of(expression: str, start: int, end: str) -> int:
    try:
        return expression.index(end, start)
    except ValueError:
        return len(expression)


def sum_multiplications(expression: str, use_conditions: bool=False) -> int:
    the_sum = 0
    start = 0
    allowed_chars = '0123456789,'
    mul_on = True
    while start < len(expression) and ('mul(' in expression[start:]):
        next_mul_candidate = expression.index('mul(', start)    
        next_do = index_of(expression, start, 'do()')
        next_dont = index_of(expression, start, "don't()")
        
        if use_conditions and next_do < next_mul_candidate and next_do < next_dont:
            # do() is the next instruction, parse it and move on
            mul_on = True
            start = next_do + 4
            continue
        elif use_conditions and next_dont < next_mul_candidate and next_dont < next_do:
            # don't() is the next instruction, parse it and move on
            mul_on = False
            start = next_dont + 7
            continue
        else:
            # there is a potential mul() instruction... parse it unless we encounter an invalid parameter
            start = next_mul_candidate + 4
                    
            end = start
            while expression[end] != ')' and expression[end] in allowed_chars:
                end += 1
            if expression[end] == ')':
                numbers = expression[start:end].split(',')
                n1, n2 = int(numbers[0]), int(numbers[1])
                if mul_on:
                    the_sum += n1 * n2
            start = end + 1

    return the_sum


if __name__ == '__main__':
    ### THE TESTS
    example_input = 'xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))'
    assert sum_multiplications(example_input) == 161
    example_input_2 = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"
    assert sum_multiplications(example_input_2, True) == 48

    ### THE REAL THING
    puzzle_input = helper.read_input()
    puzzle_input = puzzle_input.replace('\n', '')
    print(f'Part 1: {sum_multiplications(puzzle_input)}')
    print(f'Part 2: {sum_multiplications(puzzle_input, True)}')
