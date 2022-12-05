from typing import List, Tuple
import helper


def parse_input(puzzle_input: str) -> Tuple[List['Command'], List[List[str]]]:
    stack_def, cmd_def = puzzle_input.split('\n\n')

    commands = [Command(c) for c in cmd_def.strip().split('\n')]

    stack_def = stack_def.split('\n')
    stack_number_def, stack_item_def = stack_def[-1], stack_def[:-1]

    n_stacks = int(stack_number_def.split()[-1])
    stack_item_positions = {}
    for n in range(n_stacks):
        pos = stack_number_def.find(f'{n + 1}')
        stack_item_positions[n] = pos

    stacks = [list() for _ in range(n_stacks)]
    for stack_line in stack_item_def[::-1]:
        for stack_num in range(n_stacks):
            try:
                item = stack_line[stack_item_positions[stack_num]]
            except IndexError:
                item = ' '

            if item != ' ':
                stacks[stack_num].append(
                    item
                )

    return commands, stacks


class Command(object):
    def __init__(self, command_str: str):
        temp = command_str.replace('move', '').replace('from', '').replace('to', '').split()   

        (
            self.number,
            self.start_position,
            self.end_position
        ) = (int(t) for t in temp)

    def one_at_a_time(self, stacks: List[List[str]]):
        for n in range(self.number):
            item = stacks[self.start_position - 1].pop()            
            stacks[self.end_position - 1].append(item)
    
    def all_at_once(self, stacks: List[List[str]]):
        items = stacks[self.start_position - 1][-self.number:]
        stacks[self.end_position - 1].extend(items)
        stacks[self.start_position - 1] = stacks[self.start_position - 1][:-self.number]

    def __repr__(self) -> str:
        return f'Command("move {self.number} from {self.start_position} to {self.end_position}")'


def execute_commands(stacks: List[List[str]], commands: List['Command'], crane_version: int=9000):
    for c in commands:
        if crane_version == 9000:
            c.one_at_a_time(stacks)
        else:
            c.all_at_once(stacks)


def top_of_stacks(stacks: List[List[str]]) -> str:
    top_str = ''
    for stack in stacks:
        top_str += stack[-1]
    return top_str


if __name__ == '__main__':
    ### THE TESTS
    test_input = '''    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
'''
    commands, stacks = parse_input(test_input)
    execute_commands(stacks, commands)
    assert top_of_stacks(stacks) == 'CMZ'

    _, stacks = parse_input(test_input)
    execute_commands(stacks, commands, crane_version=9001)
    assert top_of_stacks(stacks) == 'MCD'

    ### THE REAL THING
    puzzle_input = helper.read_input()
    
    commands, stacks = parse_input(puzzle_input)
    execute_commands(stacks, commands)

    print(f'Part 1: {top_of_stacks(stacks)}')

    _, stacks = parse_input(puzzle_input)
    execute_commands(stacks, commands, crane_version=9001)
    print(f'Part 2: {top_of_stacks(stacks)}')
